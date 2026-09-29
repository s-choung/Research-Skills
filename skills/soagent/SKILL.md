---
name: soagent
description: Compute solid-oxide cell material properties (perovskite oxides for SOEC/SOFC - O vacancy formation, surface energy, A-site/B-site substitution, EOS bulk modulus, database screening) with a machine-learned interatomic potential through SOAgent (https://soagent.schoung.com). Remote mode only - call the public SOAgent HTTP API and let ccel-mace run MACE. Triggers - /soagent, "O vacancy formation energy", "산소 공공", "surface energy", "A-site substitution", "bulk modulus", "EOS", "LSC", "BZCYYb", "perovskite screening", "soagent"
---

# SOAgent skill

SOAgent turns one plain-language question ("O vacancy formation energy in
La0.6Sr0.4CoO3") into a relaxed perovskite-oxide calculation with a
machine-learned interatomic potential (MLIP) and returns numbers, a plot and
a rendered structure. Web UI: https://soagent.schoung.com. Source of this
skill: https://github.com/s-choung/Research-Skills/tree/master/skills/soagent.

Use it when the user wants demo-grade (fmax 0.1 eV/A, 2x2x2 supercell)
solid-oxide material property estimates in about 1 to 4 minutes, not
publication-grade DFT.

## 1. Remote mode: HTTP API

Base URL `https://soagent.schoung.com`. All bodies are JSON. Long stages
return `{"jobId": ...}` immediately; poll `GET /api/simjob?id=<jobId>` every
5 s until `status == "done"`, then read `.result`. There is no local harness
file for SOAgent — remote mode only.

### 1.1 Plan (LLM, ~5 s)

```bash
curl -s https://soagent.schoung.com/api/plan \
  -H 'content-type: application/json' \
  -d '{"message": "La0.6Sr0.4CoO3에서 산소 공공 형성 에너지를 계산해줘.", "model": "openai/gpt-6-luna"}'
```

Response: `{"parsed": {"status": "spec"|"need_clarification", "tags": {...}, "spec": {...}}, "raw": "...", "usage": {...}}`.
If `status` is `need_clarification`, ask the user the listed `questions` and
call `/api/plan` again with the answer appended to the message. Keep the
whole `spec` object; every later stage takes it. `spec.estimated_runtime_s`
gives the expected wall time.

### 1.2 Write the script (LLM, ~15 s)

```bash
curl -s https://soagent.schoung.com/api/codewrite \
  -H 'content-type: application/json' \
  -d '{"spec": <spec>, "mlip": "mace-small", "query": "<original question>", "model": "openai/gpt-6-luna"}'
# -> {"jobId": "job_..."}   then poll /api/simjob?id=job_...
```

`result.code` is a python script that only imports from the fixed SOAgent
harness (section 3). `mlip` is one of `mace-small` (MACE-MP small, default,
fastest) or `matpes-r2scan` (MACE MatPES r2SCAN). You may also write the
script yourself with section 3 and skip this call.

### 1.3 Static audit (LLM, ~3 s, optional but recommended)

```bash
curl -s https://soagent.schoung.com/api/audit -H 'content-type: application/json' \
  -d '{"spec": <spec>, "code": "<script>"}'
# poll -> result: {"verdict": "pass"|"fix", "issues": [...], "fix_instruction": "..."}
```

On `fix`, call `/api/codewrite` again with `fixInstruction` and `prevCode`.

### 1.4 Structure preview (no MLIP, ~20 s, optional)

```bash
curl -s https://soagent.schoung.com/api/preview -H 'content-type: application/json' \
  -d '{"code": "<script>", "mlip": "mace-small"}'
# -> {"runId": "run_...", "structures": ["/live/run_.../preview_structure_0.png", ...]}
```

Show the PNG urls to the user before spending compute. Pass `runId` as
`previewRunId` in the next call so the files land in the same run folder.

### 1.5 Simulate (MLIP on ccel-mace, 1 to 4 min)

```bash
curl -s https://soagent.schoung.com/api/simulate -H 'content-type: application/json' \
  -d '{"code": "<script>", "mlip": "mace-small", "taskId": "lsc_ovac", "previewRunId": "run_..."}'
# -> {"jobId": "job_..."}
curl -s 'https://soagent.schoung.com/api/simjob?id=job_...'
# running: {"status": "running", "queueAhead": 0, "initialRender": "/live/run_.../initial.png"}
# done:    {"status": "done", "result": {"exit": 0, "output": "<stdout>", "runId": "run_...",
#           "render": "/live/run_.../structure.png", "walltime_s": 41.2, "hardware": "ccel-mace (16-core CPU)"}}
```

Tell the user the expected time before starting: `spec.estimated_runtime_s`
from the planner. `exit != 0` means a python error; the traceback is in
`output`. Fix the script (or call `/api/codewrite` with `fixInstruction` set
to the traceback) and resubmit. Do not resubmit unchanged code.

### 1.6 Read the numbers

The script prints one line `RESULT_JSON:{...}` with every requested value in
eV or GPa, plus `CASE <label> ...` lines and `[harness] ...` lines noting
which structures came from the local OPTIMADE snapshot vs. an ideal cell.
Parse `RESULT_JSON` from `output` yourself, or ask the analyzer:

```bash
curl -s https://soagent.schoung.com/api/analyze -H 'content-type: application/json' \
  -d '{"query": "<question>", "spec": <spec>, "stdout": "<output>", "lang": "en"}'
# poll -> result: {"verdict": "success"|"expert_review"|"failed", "conclusion": "...",
#                  "key_numbers": {...}, "physical_check": "..."}
```

Optional plot: `POST /api/resultplot` with `{"query", "spec", "runId"}`
returns `/live/<runId>/result_plot.png`. Files under `/live/<runId>/`
(structure.png, structure.extxyz, results.json, result_plot.png) are
fetchable with plain GET.

### 1.7 Etiquette

- One simulation at a time per visitor. If `queueAhead > 0`, wait, do not
  resubmit.
- Do not loop over dozens of compositions from a script. A handful of cases
  per query is the practical limit (about 3 minutes).
- No NEB, no molecular dynamics, no cells beyond 4x4x4, no `steps > 80`.
  The static auditor rejects these.
- Report every energy with its sign convention and whether the relax
  converged. Demo-grade means fmax 0.1 eV/A on a 2x2x2 (up to 48-atom)
  supercell.

## 2. Harness API (the only imports a script may use)

```python
from soagent_harness import (
    get_calculator, load_optimade, reference_bulk, get_o2_energy,
    relax, build_perovskite, build_fluorite, substitute,
    ovac_formation, eos_bulk_modulus, surface_energy, mu_metal,
    save_structure,
)
```

Allowed extra imports: `json`, `math`, `numpy`, `itertools`, `collections`.
Never build a calculator, never call `ase.io.write`, never use
`os`/`sys`/`subprocess`/`pickle`.

### Builders

| Function | Notes |
|---|---|
| `get_calculator()` | Returns the shared MACE calculator (fixed per-request to `mace-small` or `matpes-r2scan`, CPU). Never instantiate a calculator yourself. |
| `load_optimade(formula)` | Returns `(Atoms, db_id)` for the smallest local-OPTIMADE structure matching the reduced formula (e.g. `"LaCoO3"`), or `None`. Snapshot: 816 La/Ce/Pr/Sm SOEC oxides from Alexandria/MP/OQMD. |
| `reference_bulk(symbol)` | Vetted elemental reference cell (hcp/fcc/bcc with real lattice constants) for a metal like `La`, `Sr`, `Co`, `Ni`, `Zr`, etc. Use instead of guessing `ase.build.bulk` arguments. |
| `build_perovskite(A="La", B="Co", a=3.83, supercell=(2,2,2))` | Cubic ABO3 perovskite supercell. DB-first (OPTIMADE), ideal cubic fallback. Caps total size at 48 atoms, shrinking the supercell if needed. |
| `build_fluorite(M="Ce", a=None, supercell=(2,2,2))` | Fluorite MO2 (CeO2, ZrO2, ...) conventional cell, repeated. DB-first, ideal fluorite fallback. YSZ = substitute Zr->Y (+ O vacancy), GDC = substitute Ce->Gd. |
| `substitute(atoms, old, new, n=1, seed=42)` | Deterministically replaces `n` atoms of species `old` with `new` (e.g. A-site Sr doping on La, or B-site dopants); returns a copy. |

### Relax and energies

```python
e = relax(atoms, fmax=0.1, steps=50, cell=True)
# e is a float (final energy, eV) that also proxies the relaxed Atoms object
# (iterate/index/attribute-access it directly). Refuses cell relaxation
# when vacuum is present (slab/molecule) to avoid corrupting energies.

e_o2 = get_o2_energy(fmax=0.1, steps=50)
# Reference O2 molecule energy (eV), fixed 12 A box, positions-only relax.
# NEVER cell-relax a gas-phase reference.

e_vac = ovac_formation(bulk_atoms, fmax=0.1, steps=50, o_index=None)
# O vacancy formation energy (eV) for one representative O site (defaults
# to the first O atom). Pass prerelaxed=True if bulk_atoms is already
# relaxed to skip a redundant bulk relaxation.

eos = eos_bulk_modulus(atoms, fmax=0.1, steps=50, n_points=7, span=0.03)
# Relax then Birch-Murnaghan EOS fit.
# -> {"bulk_modulus_GPa": ..., "V0_A3": ..., "E0_eV": ...}

surf = surface_energy(prim_atoms, miller=(0,0,1), layers=4, vacuum=15.0, fmax=0.1, steps=50)
# Surface energy (eV/A^2) from a PRIMITIVE bulk cell.
# -> {"surface_energy_eV_A2": ..., "n_atoms_slab": ..., "slab": <Atoms>}
# Raises if the generated slab exceeds 60 atoms - pass a primitive cell.

mu = mu_metal("Sr", fmax=0.1, steps=50)
# Chemical potential (eV) of a metal in equilibrium with its binary oxide
# and O2 - the correct reservoir for substitution/doping energies in
# oxides. Defined for La, Pr, Sm, Nd, Gd, Y, Yb, Sr, Ca, Ba, Ce.
```

`save_structure(atoms, filename="structure.extxyz")` exports safely
(strips the calculator and any stray arrays) and must be called exactly
once per script.

### Script skeleton the server expects

```python
import json
from soagent_harness import build_perovskite, relax, ovac_formation, save_structure

def run(fmax, steps, production=False):
    bulk = build_perovskite("La", "Co", supercell=(2, 2, 2))
    e_bulk = relax(bulk, fmax=fmax, steps=steps, cell=True)
    e_vac = ovac_formation(bulk, fmax=fmax, steps=steps, prerelaxed=True)
    if production:
        print(f"CASE LaCoO3_Ovac E_vac_eV={e_vac} converged=True")
        save_structure(bulk, "structure.extxyz")
    return {"LaCoO3_Ovac_E_vac_eV": e_vac}

run(fmax=3.0, steps=3)            # smoke test, seconds
print("SMOKE_OK")
result = run(fmax=0.1, steps=50, production=True)
print("RESULT_JSON:" + json.dumps(result, separators=(",", ":")))
```

Rules the auditor enforces: smoke run first, `SMOKE_OK`, exactly one
`RESULT_JSON:` line with only numbers, one `save_structure` call, no
hard-coded reference energies, `steps <= 80`, supercell at most 4x4x4.

## 3. Worked examples (all verified on soagent.schoung.com, MACE-MP-0 small)

| Question | Result | Wall time |
|---|---|---|
| O vacancy formation energy in La0.6Sr0.4CoO3 | E_vac about 1.1 eV | 55 s |
| A-site substitution: La to Sr doping in LaCoO3, 25% | E_vac before/after doping | 90 s |
| Bulk modulus (EOS) of BaZr0.8Y0.2O3-d (BZCYYb-family) | B0 in GPa, V0, E0 | 70 s |
| Surface energy of LaCoO3 (001) | gamma in eV/A^2 | 100 s |
| Bulk modulus EOS for La0.6Sr0.4CoO3 | B0, V0, E0 | 70 s |
| Database screening: O vacancy energy across LSC compositions | table of E_vac per composition | 150 s |

## 4. Reporting to the user

Give the requested property with the scheme and site named, `fmax_final`
and whether it met 0.1 eV/A, the MLIP used (`mace-small` or
`matpes-r2scan`), and the wall time. Say "demo-grade MLIP estimate" in the
first sentence. Link the structure and plot PNGs when they exist.
