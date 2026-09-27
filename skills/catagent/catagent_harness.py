"""CatAgent fixed harness: vetted building blocks for catalyst adsorption workflows.

Generated/served by the CatAgent server; user scripts import from it and must not
modify it. Every physics decision an LLM tends to get wrong (calculator setup,
gas-phase references, slab constraints, site placement, oxide terminations) is
hard-coded here so that generated scripts only COMPOSE these functions.

MLIP backend is selected by the server through the __MLIP_KEY__ placeholder:
  mace-small   -> MACE-MP-0 small (CPU, float32)            [mace-agent env]
  mace-medium  -> MACE-MP-0b3 medium (CPU, float32)         [mace-agent env]
  uma-s        -> Meta UMA-s-1p1, task oc20 (CPU)           [uma env]
"""
from __future__ import annotations

import math as _math
import os as _os

import numpy as _np
from ase import Atoms as _Atoms
from ase.io import write as _ase_write

_MLIP_KEY = "mace-small"  # mace-small | mace-medium | uma-s

# Preview mode: read once from the environment inside the harness only (the
# generated user script is never allowed to touch os). When set, get_calculator()
# returns a free null calculator, relax() takes at most one step, and the first
# clean slab / slab+adsorbate structures are snapshotted for the chat preview.
_PREVIEW = _os.environ.get("CATAGENT_PREVIEW") == "1"
_PREVIEW_MAX = 6
_PREVIEW_SLAB_KEYS = []  # (formula, sorted composition tuple) already saved
_PREVIEW_ADS_KEYS = []

_MLIP_LABELS = {
    "mace-small": "MACE-MP-0 small",
    "mace-medium": "MACE-MP-0b3 medium",
    "uma-s": "UMA-s-1p1 (oc20)",
}

_CALC = None


def mlip_label():
    return _MLIP_LABELS.get(_MLIP_KEY, _MLIP_KEY)


def get_calculator():
    """Shared MLIP calculator on CPU. Scripts must never build their own."""
    global _CALC
    if _CALC is not None:
        return _CALC
    if _PREVIEW:
        from ase.calculators.calculator import Calculator as _Calculator
        from ase.calculators.calculator import all_changes as _all_changes

        class _NullCalculator(_Calculator):
            """Free calculator for structure previews: always E=0, F=0."""

            implemented_properties = ["energy", "forces"]

            def calculate(self, atoms=None, properties=("energy",), system_changes=_all_changes):
                _Calculator.calculate(self, atoms, properties, system_changes)
                n = len(self.atoms)
                self.results = {"energy": 0.0, "forces": _np.zeros((n, 3))}

        _CALC = _NullCalculator()
        print("[harness] calculator: PREVIEW (null, no MLIP)")
        return _CALC
    if _MLIP_KEY == "uma-s":
        import logging as _logging
        import warnings as _warnings
        _warnings.filterwarnings("ignore")
        _logging.disable(_logging.WARNING)
        from fairchem.core import FAIRChemCalculator as _FC
        from fairchem.core import pretrained_mlip as _pm
        unit = _pm.get_predict_unit("uma-s-1p1", device="cpu")
        _CALC = _FC(unit, task_name="oc20")
    else:
        from mace.calculators import mace_mp as _mace_mp
        model = "medium-0b3" if _MLIP_KEY == "mace-medium" else "small"
        _CALC = _mace_mp(model=model, device="cpu", default_dtype="float32")
    print(f"[harness] calculator: {mlip_label()} (CPU)")
    return _CALC


# ---------------------------------------------------------------------------
# lattice tables (experimental, Angstrom). fcc-equivalent a for hcp/bcc metals
# comes from the atomic volume so random alloys can use Vegard's law on an fcc
# lattice regardless of the pure-element ground state.
# ---------------------------------------------------------------------------
_FCC_A = {
    "Pt": 3.92, "Pd": 3.89, "Au": 4.08, "Ag": 4.09, "Cu": 3.61, "Ni": 3.52,
    "Rh": 3.80, "Ir": 3.84, "Al": 4.05, "Pb": 4.95, "Ca": 5.59, "Sr": 6.08,
}
_HCP = {
    "Ru": (2.71, 4.28), "Os": (2.73, 4.32), "Re": (2.76, 4.46), "Co": (2.51, 4.07),
    "Zn": (2.66, 4.95), "Ti": (2.95, 4.68), "Zr": (3.23, 5.15), "Hf": (3.19, 5.05),
    "Mg": (3.21, 5.21), "Cd": (2.98, 5.62), "Sc": (3.31, 5.27), "Y": (3.65, 5.73),
}
_BCC = {
    "Fe": 2.87, "W": 3.16, "Mo": 3.15, "V": 3.03, "Cr": 2.88, "Nb": 3.30,
    "Ta": 3.31, "Mn": 2.89, "Na": 4.29, "K": 5.33,
}


def fcc_equivalent_a(symbol):
    """fcc lattice constant with the same atomic volume as the element's
    ground-state structure (used for alloy/HEA lattices via Vegard's law)."""
    if symbol in _FCC_A:
        return _FCC_A[symbol]
    if symbol in _HCP:
        a, c = _HCP[symbol]
        v_atom = (_math.sqrt(3) / 2 * a * a * c) / 2
        return (4 * v_atom) ** (1 / 3)
    if symbol in _BCC:
        a = _BCC[symbol]
        v_atom = a ** 3 / 2
        return (4 * v_atom) ** (1 / 3)
    raise ValueError(f"no lattice data for {symbol}; supported: "
                     f"{sorted(list(_FCC_A) + list(_HCP) + list(_BCC))}")


def _vegard(counts):
    tot = float(sum(counts.values()))
    return sum(fcc_equivalent_a(el) * n / tot for el, n in counts.items())


# ---------------------------------------------------------------------------
# slab builders
# ---------------------------------------------------------------------------
_MAX_SLAB_ATOMS = 64


def _check_size(size, layers_max=5):
    nx, ny, nz = size
    if nx > 4 or ny > 4 or nz > layers_max:
        raise ValueError(f"slab size {size} too large: in-plane <= 4x4, layers <= {layers_max}")


def _composition_key(atoms):
    """(formula, sorted element-count tuple): identifies a structure for dedup
    regardless of atom ordering, so re-running the same slab builder twice
    does not produce two "distinct" preview images."""
    counts = {}
    for s in atoms.get_chemical_symbols():
        counts[s] = counts.get(s, 0) + 1
    return (atoms.get_chemical_formula(), tuple(sorted(counts.items())))


def _maybe_save_preview_slab(slab):
    """Preview mode only: snapshot every distinct clean slab a builder
    returns (keyed by formula + composition so identical slabs are not
    repeated), up to _PREVIEW_MAX."""
    if not _PREVIEW or len(_PREVIEW_SLAB_KEYS) >= _PREVIEW_MAX:
        return
    key = _composition_key(slab)
    if key in _PREVIEW_SLAB_KEYS:
        return
    _PREVIEW_SLAB_KEYS.append(key)
    try:
        save_structure(slab.copy(), f"preview_slab_{len(_PREVIEW_SLAB_KEYS)}.extxyz")
    except Exception:
        pass


def _finish_slab(slab, note):
    slab.pbc = True  # UMA requires full pbc; vacuum keeps z decoupled
    slab.center(axis=2)
    if len(slab) > _MAX_SLAB_ATOMS:
        raise ValueError(f"slab has {len(slab)} atoms (> {_MAX_SLAB_ATOMS}); use a smaller size")
    print(f"[harness] {note}: {len(slab)} atoms, cell {[round(float(x), 2) for x in slab.cell.lengths()]}")
    return slab


def build_slab(element="Pt", facet="111", size=(3, 3, 4), vacuum=10.0, a=None, structure=None):
    """Clean single-element slab with adsorption-site metadata.
    facet: fcc '111'|'100'|'110'|'211', hcp '0001'|'10m10', bcc '110'|'100'|'111'.
    size=(nx, ny, layers). Returns Atoms with tags (1 = top layer)."""
    from ase.build import (bcc100, bcc110, bcc111, fcc100, fcc110, fcc111, fcc211,
                           hcp0001, hcp10m10)
    _check_size(size)
    facet = str(facet).replace("(", "").replace(")", "")
    if structure is None:
        structure = "fcc" if element in _FCC_A else "hcp" if element in _HCP else "bcc" if element in _BCC else "fcc"
    if structure == "fcc":
        a0 = a or _FCC_A.get(element) or fcc_equivalent_a(element)
        fn = {"111": fcc111, "100": fcc100, "110": fcc110, "211": fcc211}.get(facet)
        if fn is None:
            raise ValueError(f"fcc facet {facet} unsupported (111/100/110/211)")
        slab = fn(element, size=size, a=a0, vacuum=vacuum)
    elif structure == "hcp":
        a0, c0 = _HCP.get(element, (a or 2.7, 4.3))
        fn = {"0001": hcp0001, "10m10": hcp10m10, "1010": hcp10m10}.get(facet)
        if fn is None:
            raise ValueError(f"hcp facet {facet} unsupported (0001/10m10)")
        slab = fn(element, size=size, a=a0, c=c0, vacuum=vacuum)
    else:
        a0 = a or _BCC.get(element, 3.0)
        fn = {"110": bcc110, "100": bcc100, "111": bcc111}.get(facet)
        if fn is None:
            raise ValueError(f"bcc facet {facet} unsupported (110/100/111)")
        slab = fn(element, size=size, a=a0, vacuum=vacuum)
    slab = _finish_slab(slab, f"{element}({facet}) {structure} slab {size}")
    _maybe_save_preview_slab(slab)
    return slab


def build_alloy_slab(host="Pt", dopant="Ni", fraction=0.25, facet="111", size=(3, 3, 4),
                     vacuum=10.0, mode="random", seed=0):
    """Bimetallic fcc slab. mode:
      'random'     -> dopant distributed randomly through all layers (solid solution)
      'surface'    -> dopant only in the top layer (skin/overlayer alloy)
      'subsurface' -> dopant only in the second layer (Pt-skin on dopant sublayer)
      'core_shell' -> host top layer, dopant everywhere below
    fraction = dopant atomic fraction of the affected layers (0..1).
    Lattice constant follows Vegard's law of the overall composition."""
    _check_size(size)
    rng = _np.random.default_rng(seed)
    slab = build_slab(host, facet=facet, size=size, vacuum=vacuum, structure="fcc")
    tags = slab.get_tags()
    if mode == "random":
        pool = list(range(len(slab)))
    elif mode == "surface":
        pool = [i for i in range(len(slab)) if tags[i] == 1]
    elif mode == "subsurface":
        pool = [i for i in range(len(slab)) if tags[i] == 2]
    elif mode == "core_shell":
        pool = [i for i in range(len(slab)) if tags[i] != 1]
        fraction = 1.0
    else:
        raise ValueError("mode must be random|surface|subsurface|core_shell")
    n = int(round(fraction * len(pool)))
    for i in rng.choice(pool, size=n, replace=False):
        slab[int(i)].symbol = dopant
    syms = slab.get_chemical_symbols()
    counts = {s: syms.count(s) for s in set(syms)}
    a_new = _vegard(counts)
    a_old = _FCC_A.get(host) or fcc_equivalent_a(host)
    cell = slab.get_cell().copy()
    cell[0] *= a_new / a_old
    cell[1] *= a_new / a_old
    pos = slab.get_positions()
    pos[:, :2] *= a_new / a_old
    pos[:, 2] = (pos[:, 2] - pos[:, 2].min()) * (a_new / a_old) + pos[:, 2].min()
    slab.set_cell(cell)
    slab.set_positions(pos)
    formula = "".join(f"{k}{v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
    print(f"[harness] alloy {formula} ({mode}, seed={seed}) a_Vegard={a_new:.3f} A")
    _INITIAL_SAVED[0] = False
    _maybe_save_preview_slab(slab)
    return slab


def build_hea_slab(elements=("Ir", "Pd", "Pt", "Rh", "Ru"), fractions=None, facet="111",
                   size=(3, 3, 4), vacuum=10.0, seed=0):
    """Random-solid-solution high-entropy-alloy fcc slab with exact atom counts
    matching `fractions` (default equimolar). Lattice from Vegard's law.
    Different seeds give different random configurations of the same composition."""
    _check_size(size)
    elements = list(elements)
    if fractions is None:
        fractions = [1.0 / len(elements)] * len(elements)
    fractions = _np.array(fractions, dtype=float)
    fractions = fractions / fractions.sum()
    n_atoms = size[0] * size[1] * size[2]
    counts = _np.floor(fractions * n_atoms).astype(int)
    while counts.sum() < n_atoms:  # hand remaining atoms to the largest fractional parts
        rem = fractions * n_atoms - counts
        counts[int(_np.argmax(rem))] += 1
    a_new = _vegard({el: int(c) for el, c in zip(elements, counts)})
    from ase.build import fcc100, fcc110, fcc111
    fn = {"111": fcc111, "100": fcc100, "110": fcc110}[str(facet).strip("()")]
    slab = fn(elements[0], size=size, a=a_new, vacuum=vacuum)
    symbols = []
    for el, c in zip(elements, counts):
        symbols += [el] * int(c)
    rng = _np.random.default_rng(seed)
    rng.shuffle(symbols)
    slab.set_chemical_symbols(symbols)
    comp = " ".join(f"{el}{int(c)}" for el, c in zip(elements, counts))
    _INITIAL_SAVED[0] = False
    slab = _finish_slab(slab, f"HEA {comp} ({facet}) seed={seed} a={a_new:.3f}")
    _maybe_save_preview_slab(slab)
    return slab


_RUTILE = {  # a, c, u (oxygen internal coordinate), experimental
    "Ti": (4.594, 2.959, 0.305), "Ru": (4.492, 3.106, 0.306), "Ir": (4.498, 3.154, 0.307),
    "Sn": (4.737, 3.186, 0.307), "Mn": (4.398, 2.873, 0.302), "Ge": (4.395, 2.860, 0.307),
    "Pb": (4.955, 3.383, 0.307), "V": (4.554, 2.851, 0.300), "Cr": (4.421, 2.916, 0.300),
    "Os": (4.500, 3.180, 0.310), "Rh": (4.490, 3.090, 0.310), "Nb": (4.770, 3.030, 0.300),
    "Ta": (4.709, 3.065, 0.300), "Mo": (4.860, 2.790, 0.300), "W": (4.860, 2.780, 0.300),
}


def build_rutile_bulk(M="Ru"):
    """Rutile MO2 conventional 6-atom cell (P4_2/mnm, #136)."""
    from ase.spacegroup import crystal as _crystal
    if M not in _RUTILE:
        raise ValueError(f"no rutile data for {M}O2; supported: {sorted(_RUTILE)}")
    a, c, u = _RUTILE[M]
    bulk = _crystal([M, "O"], basis=[(0, 0, 0), (u, u, 0)], spacegroup=136,
                    cellpar=[a, a, c, 90, 90, 90])
    return bulk


def build_rutile_slab(M="Ru", facet="110", layers=3, size=(2, 1), vacuum=10.0):
    """Stoichiometric rutile MO2 (110) slab (RuO2, IrO2, TiO2, SnO2 ...), the
    standard OER/ORR oxide model surface. Termination = bridging-O rows on top,
    with 5-fold coordinated metal (cus) sites exposed.
    layers = number of O-M2O2-O trilayers (3 recommended, 4 max).
    size = in-plane repeat (nx along the short [001] axis, ny along [1-10])."""
    from ase.build import surface as _surface
    if str(facet).strip("()") != "110":
        raise ValueError("only the rutile (110) facet is supported")
    if layers > 4:
        raise ValueError("rutile slabs: at most 4 trilayers")
    bulk = build_rutile_bulk(M)
    slab = _rutile_reslice(bulk, layers, vacuum)
    lengths = slab.cell.lengths()
    nx, ny = size
    rep = [1, 1, 1]
    # the short axis (~c, 3 A) is the one that should be doubled by default
    short_axis = int(_np.argmin(lengths[:2]))
    rep[short_axis] = nx
    rep[1 - short_axis] = ny
    slab = slab.repeat(tuple(rep))
    slab.set_tags(0)
    _INITIAL_SAVED[0] = False
    slab = _finish_slab(slab, f"rutile {M}O2(110) {layers} trilayers x{rep[:2]}")
    _maybe_save_preview_slab(slab)
    return slab


def _rutile_reslice(bulk, layers, vacuum):
    """(110) slab with the bridging-O termination on BOTH faces.
    Stacking along [110] (M-plane spacing d = a/sqrt2 ~ 3.2 A): each trilayer is
    O(-1.24) | M2O2(0) | O(+1.24) with a 0.7 A gap to the next one. ase.build.surface
    cuts through an M2O2 plane, so we build a thicker slab and keep exactly
    `layers` complete trilayers below the top bridging-O plane."""
    from ase.build import surface as _surface
    big = _surface(bulk, (1, 1, 0), layers=layers + 3, vacuum=0.0, periodic=True)
    z = big.get_positions()[:, 2]
    sym = _np.array(big.get_chemical_symbols())
    m_planes = sorted(set(_np.round(z[sym != "O"], 2).tolist()), reverse=True)
    d = m_planes[0] - m_planes[1]
    o_z = z[sym == "O"]
    chosen = None
    for zm in m_planes:
        above = o_z[(o_z > zm + 0.9) & (o_z < zm + 1.6)]
        if len(above) == 0:
            continue
        ztop = float(above.max())
        zbot = zm - (layers - 1) * d - 1.6  # between the bottom bridging O and the next trilayer
        if zbot < z.min() - 0.05:
            continue
        chosen = (ztop, zbot)
        break
    if chosen is None:
        raise ValueError("could not find a bridging-O terminated rutile (110) slab")
    ztop, zbot = chosen
    keep = (z <= ztop + 0.05) & (z > zbot)
    slab = big[keep]
    n_m = int(_np.sum(_np.array(slab.get_chemical_symbols()) != "O"))
    n_o = len(slab) - n_m
    if n_o != 2 * n_m:
        raise ValueError(f"rutile slab not stoichiometric: M{n_m}O{n_o}")
    cell = slab.get_cell()
    zspan = float(_np.ptp(slab.get_positions()[:, 2]))
    slab.set_cell([cell[0], cell[1], [0.0, 0.0, zspan + 2 * vacuum]])
    slab.center(axis=2)
    slab.pbc = True
    return slab


def cus_sites(slab):
    """Indices of coordinatively unsaturated (5-fold) top-layer metal atoms of a
    rutile (110) slab (the active sites for OER intermediates)."""
    sym = _np.array(slab.get_chemical_symbols())
    z = slab.get_positions()[:, 2]
    metal = [i for i in range(len(slab)) if sym[i] != "O"]
    zmax_m = max(z[i] for i in metal)
    top_m = [i for i in metal if z[i] > zmax_m - 0.5]
    out = []
    for i in top_m:
        d = slab.get_distances(i, [j for j in range(len(slab)) if sym[j] == "O"], mic=True)
        n_o = int(_np.sum(d < 2.35))
        if n_o <= 5:
            out.append(i)
    return out


def bridge_o_sites(slab):
    """Indices of the top bridging O atoms of a rutile (110) slab."""
    sym = _np.array(slab.get_chemical_symbols())
    z = slab.get_positions()[:, 2]
    zmax = z.max()
    return [i for i in range(len(slab)) if sym[i] == "O" and z[i] > zmax - 0.3]


def ontop_sites(slab):
    """Indices of all top-layer atoms (for site-resolved ontop scans, e.g. on HEAs)."""
    tags = slab.get_tags()
    if tags.max() > 0:
        return [i for i in range(len(slab)) if tags[i] == 1]
    z = slab.get_positions()[:, 2]
    return [i for i in range(len(slab)) if z[i] > z.max() - 0.5]


def surface_symbols(slab):
    """Chemical symbols of the top layer (index-aligned with ontop_sites)."""
    return [slab[i].symbol for i in ontop_sites(slab)]


# ---------------------------------------------------------------------------
# adsorbates and references
# ---------------------------------------------------------------------------
_ADSORBATES = {  # binding atom at origin, molecule pointing +z
    "O": ("O", [[0, 0, 0]]),
    "H": ("H", [[0, 0, 0]]),
    "N": ("N", [[0, 0, 0]]),
    "C": ("C", [[0, 0, 0]]),
    "S": ("S", [[0, 0, 0]]),
    "CO": ("CO", [[0, 0, 0], [0, 0, 1.15]]),
    "NO": ("NO", [[0, 0, 0], [0, 0, 1.16]]),
    "N2": ("NN", [[0, 0, 0], [0, 0, 1.10]]),
    "OH": ("OH", [[0, 0, 0], [0.55, 0, 0.80]]),
    "OOH": ("OOH", [[0, 0, 0], [0.95, 0, 1.10], [1.55, 0, 1.85]]),
    "H2O": ("OHH", [[0, 0, 0], [0.76, 0, 0.59], [-0.76, 0, 0.59]]),
    "NH": ("NH", [[0, 0, 0], [0, 0, 1.02]]),
    "NH2": ("NHH", [[0, 0, 0], [0.82, 0, 0.60], [-0.82, 0, 0.60]]),
    "NH3": ("NHHH", [[0, 0, 0], [0.94, 0, 0.38], [-0.47, 0.81, 0.38], [-0.47, -0.81, 0.38]]),
    "CH3": ("CHHH", [[0, 0, 0], [1.03, 0, 0.36], [-0.52, 0.89, 0.36], [-0.52, -0.89, 0.36]]),
    "CHO": ("CHO", [[0, 0, 0], [-0.95, 0, 0.55], [1.05, 0, 0.65]]),
    "CO2": ("COO", [[0, 0, 0], [1.16, 0, 0.0], [-1.16, 0, 0.0]]),
    "OCHO": ("OCOH", [[0, 0, 0], [0.75, 0, 1.10], [1.95, 0, 0.75], [0.75, 0, 2.20]]),
}
_GAS_MOLECULES = {"H2", "H2O", "CO", "NO", "N2", "O2", "NH3", "CH4", "CO2"}

# free-energy corrections (ZPE - TS + integrated Cp, eV) at 298 K, standard values
_FREE_ENERGY_CORR = {"OH": 0.35, "O": 0.05, "OOH": 0.40, "H": 0.24, "N": 0.10, "NH": 0.30,
                     "NH2": 0.60, "NH3": 0.90, "CO": 0.15, "NO": 0.12}


def make_adsorbate(name):
    """Atoms for a supported adsorbate with the binding atom at the origin."""
    if name not in _ADSORBATES:
        raise ValueError(f"unsupported adsorbate {name}; supported: {sorted(_ADSORBATES)}")
    syms, pos = _ADSORBATES[name]
    return _Atoms(syms, positions=pos)


_GAS_CACHE = {}


def gas_energy(formula, fmax=0.05, steps=100):
    """Gas-phase molecule energy (eV) in a fixed 15 A box, positions-only relax.
    Cached. NEVER build gas references yourself."""
    if _PREVIEW:
        return 0.0
    if formula in _GAS_CACHE:
        return _GAS_CACHE[formula]
    if formula not in _GAS_MOLECULES:
        raise ValueError(f"gas reference {formula} unsupported; use {sorted(_GAS_MOLECULES)}")
    from ase.build import molecule as _molecule
    from ase.optimize import FIRE as _FIRE
    mol = _molecule(formula)
    mol.set_cell([15.0, 15.0, 15.0])
    mol.center()
    mol.pbc = True
    mol.calc = get_calculator()
    _FIRE(mol, logfile=None).run(fmax=fmax, steps=steps)
    e = float(mol.get_potential_energy())
    _GAS_CACHE[formula] = e
    print(f"[harness] gas {formula}: {e:.3f} eV")
    return e


def default_scheme(adsorbate):
    """'che' (computational-hydrogen-electrode references H2/H2O/N2/CO) for open-shell
    fragments, 'gas' (the molecule itself) for closed-shell molecules."""
    return "gas" if adsorbate in _GAS_MOLECULES or adsorbate in ("CO", "NO", "NH3", "H2O", "CO2", "N2") else "che"


def reference_energy(adsorbate, scheme=None):
    """Reference energy (eV) subtracted in E_ads = E(slab+ads) - E(slab) - E_ref.
    che: O = H2O - H2, OH = H2O - 1/2 H2, OOH = 2 H2O - 3/2 H2, H = 1/2 H2,
         N = 1/2 N2, NH = 1/2 N2 + 1/2 H2, NH2 = 1/2 N2 + H2, CH3 = CH4 - 1/2 H2,
         CHO = CO + 1/2 H2, OCHO = CO2 + 1/2 H2, C = CO - 1/2 O2 (avoid), S unsupported
    gas: E(molecule) — CO, NO, NH3, H2O, CO2, N2. 'gas' for O/H/N uses 1/2 O2, 1/2 H2, 1/2 N2."""
    scheme = scheme or default_scheme(adsorbate)
    g = gas_energy
    che = {
        "O": lambda: g("H2O") - g("H2"), "OH": lambda: g("H2O") - 0.5 * g("H2"),
        "OOH": lambda: 2 * g("H2O") - 1.5 * g("H2"), "H": lambda: 0.5 * g("H2"),
        "N": lambda: 0.5 * g("N2"), "NH": lambda: 0.5 * g("N2") + 0.5 * g("H2"),
        "NH2": lambda: 0.5 * g("N2") + g("H2"), "NH3": lambda: g("NH3"),
        "CH3": lambda: g("CH4") - 0.5 * g("H2"), "CHO": lambda: g("CO") + 0.5 * g("H2"),
        "OCHO": lambda: g("CO2") + 0.5 * g("H2"), "CO": lambda: g("CO"), "NO": lambda: g("NO"),
        "H2O": lambda: g("H2O"), "CO2": lambda: g("CO2"), "N2": lambda: g("N2"),
        "C": lambda: g("CO") - 0.5 * g("O2"),
    }
    gas = dict(che)
    gas.update({"O": lambda: 0.5 * g("O2"), "H": lambda: 0.5 * g("H2"), "N": lambda: 0.5 * g("N2")})
    table = che if scheme == "che" else gas
    if adsorbate not in table:
        raise ValueError(f"no reference for {adsorbate}")
    return float(table[adsorbate]())


def free_energy_correction(adsorbate):
    """Standard ZPE/entropy correction (eV) to turn E_ads into dG_ads at 298 K."""
    return _FREE_ENERGY_CORR.get(adsorbate, 0.0)


# ---------------------------------------------------------------------------
# placement
# ---------------------------------------------------------------------------
_DEFAULT_HEIGHT = {"ontop": 1.9, "bridge": 1.5, "fcc": 1.3, "hcp": 1.3, "hollow": 1.3,
                   "cus": 1.9, "bridge_O": 1.0}


def _host_ontop_site(slab):
    """Bare 'ontop' resolves here: on an alloy/HEA slab, first-cell metadata may
    land on a minority dopant atom. Pick the majority (host) element's top-layer
    atom nearest the cell's xy-centre instead; on a single-element slab this is
    just the ontop atom nearest the centre (same physical site every time)."""
    idx = ontop_sites(slab)
    if not idx:
        idx = list(range(len(slab)))
    syms = [slab[i].symbol for i in idx]
    counts = {}
    for sym in syms:
        counts[sym] = counts.get(sym, 0) + 1
    host = max(counts, key=counts.get)
    host_idx = [i for i in idx if slab[i].symbol == host] or idx
    pos = slab.get_positions()
    cell = slab.get_cell()
    center_xy = 0.5 * (cell[0][:2] + cell[1][:2])
    best = min(host_idx, key=lambda i: float(_np.hypot(pos[i, 0] - center_xy[0], pos[i, 1] - center_xy[1])))
    return best


def _site_position(slab, site):
    """Return (x, y, z_ref, ref_atom_index) for a site spec. site may be:
    'ontop'|'bridge'|'fcc'|'hcp'|'hollow' (first surface cell, ase metadata),
    'ontop:<atom index>' or an int (above that atom), 'cus' / 'cus:<k>' (k-th cus
    metal of a rutile slab), 'bridge_O' / 'bridge_O:<k>', or an (x, y) tuple.
    ref_atom_index is the single atom the site is anchored to (for later dz
    measurement), or None when the site is a multi-atom hollow/bridge average."""
    pos = slab.get_positions()
    ztop = pos[ontop_sites(slab), 2].max() if ontop_sites(slab) else pos[:, 2].max()
    if isinstance(site, (int, _np.integer)):
        return pos[int(site), 0], pos[int(site), 1], pos[int(site), 2], int(site)
    if isinstance(site, (tuple, list)) and len(site) == 2:
        return float(site[0]), float(site[1]), ztop, None
    s = str(site)
    if ":" in s:
        kind, k = s.split(":", 1)
        k = int(k)
        if kind == "ontop":
            return pos[k, 0], pos[k, 1], pos[k, 2], k
        if kind == "cus":
            i = cus_sites(slab)[k]
            return pos[i, 0], pos[i, 1], pos[i, 2], i
        if kind == "bridge_O":
            i = bridge_o_sites(slab)[k]
            return pos[i, 0], pos[i, 1], pos[i, 2], i
        raise ValueError(f"unknown site {site}")
    if s == "cus":
        i = cus_sites(slab)[0]
        return pos[i, 0], pos[i, 1], pos[i, 2], i
    if s == "bridge_O":
        i = bridge_o_sites(slab)[0]
        return pos[i, 0], pos[i, 1], pos[i, 2], i
    if s == "ontop":
        top_syms = set(slab[i].symbol for i in ontop_sites(slab))
        if len(top_syms) > 1:
            # alloy/HEA: the builder's adsorbate_info metadata is a single
            # first-cell fractional position with no atom identity — it can
            # land on a minority dopant. Anchor to an explicit host atom
            # instead, so the site is the same physical atom every rewrite.
            i = _host_ontop_site(slab)
            return pos[i, 0], pos[i, 1], pos[i, 2], i
    info = slab.info.get("adsorbate_info")
    if not info or "sites" not in info:
        if s == "ontop":
            i = _host_ontop_site(slab)
            return pos[i, 0], pos[i, 1], pos[i, 2], i
        raise ValueError(f"slab has no site metadata for '{s}'; use 'ontop:<index>' or (x, y)")
    name = "fcc" if s == "hollow" else s
    if name not in info["sites"]:
        if s == "ontop":
            # stepped facets (fcc211, bcc/hcp variants) carry an empty site
            # table in ase: anchor to the top-layer host atom nearest the centre
            i = _host_ontop_site(slab)
            return pos[i, 0], pos[i, 1], pos[i, 2], i
        raise ValueError(f"site '{s}' not defined for this facet; available: {sorted(info['sites'])}. "
                         "Use 'ontop:<atom index>' or an (x, y) tuple on stepped facets.")
    frac = _np.array(info["sites"][name])
    cell2d = _np.array(info["cell"])
    xy = frac @ cell2d
    return float(xy[0]), float(xy[1]), info.get("top layer", ztop), None


def add_adsorbate_at(slab, adsorbate="CO", site="ontop", height=None, tilt_deg=0.0):
    """Copy of slab with `adsorbate` placed at `site`, binding atom `height` A
    above the reference atom/plane. Returns the new Atoms (the slab is untouched)."""
    ads = make_adsorbate(adsorbate) if isinstance(adsorbate, str) else adsorbate.copy()
    name = adsorbate if isinstance(adsorbate, str) else ads.get_chemical_formula()
    x, y, zref, ref_idx = _site_position(slab, site)
    kind = str(site).split(":")[0] if isinstance(site, str) else "ontop"
    if height is None:
        height = _DEFAULT_HEIGHT.get(kind, 1.8)
        if name == "H" and kind in ("ontop", "cus"):
            height = 1.6
    if tilt_deg:
        ads.rotate(tilt_deg, "y")
    ads.translate([x, y, zref + height])
    out = slab.copy()
    out += ads
    out.pbc = True
    n_slab = len(slab)
    out.set_tags(list(slab.get_tags()) + [0] * len(ads))
    out.info["adsorbate_indices"] = list(range(n_slab, len(out)))
    out.info["ref_atom_index"] = int(ref_idx) if ref_idx is not None else None
    if _PREVIEW and len(_PREVIEW_ADS_KEYS) < _PREVIEW_MAX:
        key = _composition_key(out)
        if key not in _PREVIEW_ADS_KEYS:
            _PREVIEW_ADS_KEYS.append(key)
            try:
                save_structure(out.copy(), f"preview_ads_{len(_PREVIEW_ADS_KEYS)}.extxyz")
            except Exception:
                pass
    return out


# ---------------------------------------------------------------------------
# relaxation and energies
# ---------------------------------------------------------------------------
_INITIAL_SAVED = [False]


class _RelaxResult(float):
    """Final energy (eV) that also proxies the relaxed Atoms (iteration,
    indexing and attribute access), so both `e = relax(a)` and `a = relax(a)` work."""

    def __new__(cls, energy, atoms):
        obj = super().__new__(cls, energy)
        obj.atoms = atoms
        return obj

    def __iter__(self):
        return iter(self.atoms)

    def __len__(self):
        return len(self.atoms)

    def __getitem__(self, item):
        return self.atoms[item]

    def __getattr__(self, name):
        return getattr(self.atoms, name)


def _fix_bottom(atoms, n_fixed_layers):
    from ase.constraints import FixAtoms as _FixAtoms
    tags = atoms.get_tags()
    if n_fixed_layers is None:
        n_layers = int(tags.max()) if tags.max() > 0 else 4
        n_fixed_layers = max(1, n_layers // 2)
    if tags.max() > 0:
        n_layers = int(tags.max())
        fixed = [i for i in range(len(atoms)) if tags[i] > n_layers - n_fixed_layers]
    else:
        # oxide/other slab without tags: fix the bottom half by height (slab atoms only)
        ads = set(atoms.info.get("adsorbate_indices", []))
        z = atoms.get_positions()[:, 2]
        slab_idx = [i for i in range(len(atoms)) if i not in ads]
        zmin, zmax = z[slab_idx].min(), z[slab_idx].max()
        fixed = [i for i in slab_idx if z[i] < zmin + 0.5 * (zmax - zmin) - 0.01]
    atoms.set_constraint(_FixAtoms(indices=fixed))
    return len(fixed)


def relax(atoms, fmax=0.1, steps=60, fix_bottom=None, cell=False):
    """Relax in place with FIRE; bottom layers fixed (default: bottom half).
    Never relaxes the cell of a slab or molecule (vacuum present). Returns the
    final energy, usable as the relaxed Atoms too."""
    from ase.optimize import FIRE as _FIRE
    atoms.pbc = True
    if _PREVIEW:
        steps = min(steps, 1)
    if not _INITIAL_SAVED[0] and len(atoms) > 2:
        _INITIAL_SAVED[0] = True
        try:
            save_structure(atoms.copy(), "initial.extxyz")
        except Exception:
            pass
    atoms.calc = get_calculator()
    has_vacuum = atoms.get_volume() / max(1, len(atoms)) > 25.0
    if cell and not has_vacuum:
        from ase.filters import FrechetCellFilter as _FCF
        _FIRE(_FCF(atoms), logfile=None).run(fmax=fmax, steps=steps)
    else:
        if has_vacuum and len(atoms) > 4:
            _fix_bottom(atoms, fix_bottom)
        _FIRE(atoms, logfile=None).run(fmax=fmax, steps=steps)
    fmax_final = float(_np.abs(atoms.get_forces()).max()) if len(atoms) > 1 else 0.0
    e = float(atoms.get_potential_energy())
    print(f"[harness] relax {atoms.get_chemical_formula()}: E={e:.3f} eV, fmax={fmax_final:.3f}")
    return _RelaxResult(e, atoms)


def relax_bulk(atoms, fmax=0.05, steps=80):
    """Relax a periodic bulk cell (positions and cell). For lattice constants."""
    return relax(atoms, fmax=fmax, steps=steps, cell=True)


_CLEAN_CACHE = {}


def _slab_key(slab):
    return (slab.get_chemical_formula(), _np.round(slab.get_positions(), 2).tobytes())


def clean_slab_energy(slab, fmax=0.1, steps=60):
    """Relaxed clean-slab energy (eV), cached so site scans and sweeps do not
    re-relax the same slab. The passed slab is not modified."""
    # the smoke test (fmax=3, steps=3) must never feed its loosely relaxed
    # clean-slab energy into the production run: key on the convergence too
    key = (_slab_key(slab), round(float(fmax), 4), int(steps))
    if key in _CLEAN_CACHE:
        return _CLEAN_CACHE[key]
    s = slab.copy()
    e = float(relax(s, fmax=fmax, steps=steps))
    _CLEAN_CACHE[key] = e
    return e


def adsorption_energy(slab, adsorbate="CO", site="ontop", height=None, fmax=0.1, steps=60,
                      scheme=None, clean_energy=None):
    """E_ads = E(slab+ads) - E(clean slab) - E_ref(adsorbate). Negative = exothermic.
    Returns dict: E_ads_eV, E_slab_eV, E_slab_ads_eV, E_ref_eV, scheme, site,
    adsorbate, atoms (relaxed slab+adsorbate), dz_A (binding atom height after relax),
    converged (bool, fmax_final <= the requested fmax), fmax_final (eV/A).
    Put ONLY the numbers in RESULT_JSON, never the atoms."""
    scheme = scheme or default_scheme(adsorbate)
    e_slab = float(clean_energy) if clean_energy is not None else clean_slab_energy(slab, fmax, steps)
    sa = add_adsorbate_at(slab, adsorbate, site, height=height)
    e_sa = float(relax(sa, fmax=fmax, steps=steps))
    fmax_final = float(_np.abs(sa.get_forces()).max()) if len(sa) > 1 else 0.0
    # one cheap extra push when the step budget ran out short of the target
    # (avoids the codewriter re-implementing its own re-relax loop); only for
    # small cells so this stays within the runtime budget
    if fmax_final > 0.3 and len(sa) <= 48:
        e_sa = float(relax(sa, fmax=fmax, steps=40))
        fmax_final = float(_np.abs(sa.get_forces()).max()) if len(sa) > 1 else 0.0
    converged = bool(fmax_final <= fmax)
    e_ref = reference_energy(adsorbate, scheme)
    e_ads = e_sa - e_slab - e_ref
    ads_idx = sa.info.get("adsorbate_indices", [len(sa) - 1])
    z = sa.get_positions()[:, 2]
    ref_idx = sa.info.get("ref_atom_index")
    if ref_idx is not None:
        slab_top = float(z[ref_idx])
    else:
        slab_top = max(z[i] for i in range(len(sa)) if i not in set(ads_idx))
    dz = float(z[ads_idx[0]] - slab_top)
    # sanity: adsorbate that flew away or dove into the slab
    if dz > 3.5 or dz < 0.3:
        print(f"[harness] WARNING: binding atom {dz:.2f} A above the surface after relax (desorbed or buried?)")
    print(f"[harness] E_ads({adsorbate}@{site}) = {e_ads:.3f} eV  (fmax_final={fmax_final:.3f}, converged={converged})")
    return {"E_ads_eV": float(e_ads), "E_slab_eV": e_slab, "E_slab_ads_eV": e_sa,
            "E_ref_eV": e_ref, "scheme": scheme, "site": str(site), "adsorbate": adsorbate,
            "atoms": sa, "dz_A": dz, "converged": converged, "fmax_final": fmax_final}


def site_scan(slab, adsorbate="CO", sites=("ontop", "bridge", "fcc", "hcp"), fmax=0.1, steps=60,
              scheme=None):
    """Adsorption energy at each site. Returns {site: E_ads_eV}; the most stable
    site is min(). The clean slab is relaxed once and reused."""
    e_slab = clean_slab_energy(slab, fmax, steps)
    out = {}
    for s in sites:
        try:
            r = adsorption_energy(slab, adsorbate, s, fmax=fmax, steps=steps, scheme=scheme,
                                  clean_energy=e_slab)
            out[str(s)] = r["E_ads_eV"]
        except ValueError as err:
            print(f"[harness] site {s} skipped: {err}")
    return out


def ontop_scan(slab, adsorbate="OH", fmax=0.1, steps=60, scheme=None, max_sites=9):
    """Site-resolved ontop adsorption over every top-layer atom (HEA / alloy
    surfaces). Returns list of {index, symbol, E_ads_eV}."""
    idx = ontop_sites(slab)[:max_sites]
    e_slab = clean_slab_energy(slab, fmax, steps)
    rows = []
    for i in idx:
        r = adsorption_energy(slab, adsorbate, f"ontop:{i}", fmax=fmax, steps=steps,
                              scheme=scheme, clean_energy=e_slab)
        rows.append({"index": int(i), "symbol": slab[i].symbol, "E_ads_eV": r["E_ads_eV"]})
    return rows


def sabatier_activity(e_ads_list, e_ref, optimum=0.10, T=300.0):
    """HEAgent-style activity score: mean over sites of
    exp(-|dE_rel - optimum| / kT), with dE_rel = E_ads - e_ref (e.g. Pt(111) OH).
    Score for Pt(111) itself (all sites at dE_rel = 0) is exp(-optimum/kT)."""
    kT = 8.617333e-5 * T
    vals = [_math.exp(-abs((e - e_ref) - optimum) / kT) for e in e_ads_list]
    return float(sum(vals) / max(1, len(vals)))


def reaction_energy(products, reactants):
    """dE = sum(E_products) - sum(E_reactants) for lists of energies (eV)."""
    return float(sum(products) - sum(reactants))


def save_structure(atoms, filename="structure.extxyz"):
    """Export safely: strips calculator and extra arrays. Call once on the main
    final structure (the most stable slab+adsorbate). NEVER call ase.io.write."""
    out = atoms.atoms.copy() if isinstance(atoms, _RelaxResult) else atoms.copy()
    out.calc = None
    out.set_constraint()
    for key in [k for k in list(out.arrays) if k not in ("numbers", "positions")]:
        del out.arrays[key]
    _ase_write(filename, out)
    return filename
