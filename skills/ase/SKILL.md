# ASE Skill — Library Reference v3

> ASE 3.27 (Atomic Simulation Environment). import 경로, 클래스명, 핵심 파라미터, 주의사항 참고.

## 1. Core Objects
```python
from ase import Atoms           # Atoms(symbols, positions=, cell=, pbc=)
from ase.atom import Atom       # 단일 원자
from ase.cell import Cell       # 3x3 unit cell
from ase import units           # units.fs, units.kB, units.bar, units.kJ, units.Bohr, units.Hartree
```
WARNING: `atoms.get_cell_lengths_and_angles()` -> 6개 원소 1차원 배열 반환 `[a, b, c, alpha, beta, gamma]`. 2개로 언패킹 불가.
WARNING: `atoms.calc = EMT()` 사용. `set_calculator()`는 deprecated.

## 2. Structure Building -- `ase.build`
```python
from ase.build import (
    bulk,                  # bulk('Cu','fcc', a=3.6, cubic=True, orthorhombic=True)
    molecule,              # molecule('H2O') -- G2 database (H2O, CO2, CH4, NH3, C60 등)
    fcc111, fcc100, fcc110, fcc211,  # fcc 표면 -- size=(x,y,layers), vacuum=, a=
    bcc100, bcc110, bcc111,          # bcc 표면
    hcp0001, hcp10m10,               # hcp 표면
    diamond100, diamond111,          # diamond 표면
    mx2,                   # mx2('MoS2', kind='2H', a=3.18, thickness=3.17, vacuum=10)
    surface,               # surface(lattice, indices, layers) -- 일반 Miller index
    add_adsorbate,         # add_adsorbate(slab, adsorbate, height, position='ontop')
    add_vacuum,            # add_vacuum(atoms, vacuum) -- z방향 진공 추가
    nanotube,              # nanotube(n, m, length=, bond=, symbol=)
    graphene_nanoribbon,   # graphene_nanoribbon(n, m, type='armchair'|'zigzag')
    make_supercell,        # make_supercell(atoms, P) -- P는 3x3 변환 행렬
    cut, stack, sort,
    niggli_reduce,
    minimize_tilt,
)
```
WARNING: `add_adsorbate(slab, ads, h, pos)` -- **in-place 수정, 리턴 None**. `slab`이 직접 변경됨. 다원자 분자는 `molecule('CO')` Atoms 객체로 전달.
WARNING: `add_vacuum(atoms, vac)` -- **in-place 수정, 리턴 None**. `atoms`가 직접 변경됨.
WARNING: supercell: `atoms * (2,2,2)` 또는 `atoms.repeat((2,2,2))` 모두 가능.

## 3. Calculators -- `ase.calculators`
```python
# Built-in (외부 코드 불필요)
from ase.calculators.emt import EMT          # EMT() -- FCC 금속 (Cu,Ag,Au,Ni,Pd,Pt,Al)
from ase.calculators.eam import EAM          # EAM(potential='file.alloy')
from ase.calculators.tersoff import Tersoff
from ase.calculators.lj import LennardJones  # LJ 포텐셜
from ase.calculators.morse import MorsePotential

# External wrappers (외부 코드 필요)
from ase.calculators.vasp import Vasp
from ase.calculators.espresso import Espresso
from ase.calculators.gaussian import Gaussian
from ase.calculators.cp2k import CP2K
from ase.calculators.aims import Aims
from ase.calculators.orca import ORCA
from ase.calculators.lammps import LAMMPSlib
from ase.calculators.dftb import Dftb

# Meta-calculators
from ase.calculators.mixing import SumCalculator, MixedCalculator
from ase.calculators.socketio import SocketIOCalculator
from ase.calculators.qmmm import EIQMMM, SimpleQMMM
```
WARNING: 연결: `atoms.calc = EMT()` -- optimizer/MD 전에 반드시 설정.

## 4. I/O -- `ase.io`
```python
from ase.io import read, iread, write
# read('file.xyz')  read('POSCAR', format='vasp')  read('input.traj', index=':')
# write('out.xyz', atoms)  write('POSCAR', atoms, format='vasp')
from ase.io.trajectory import Trajectory  # Trajectory('file.traj', 'w', atoms)
```
WARNING: format 이름: `'vasp'` (not `'poscar'`), `'espresso-in'`, `'gaussian-in'`, `'xyz'`, `'extxyz'`, `'cif'`, `'pdb'`, `'lammps-data'`
WARNING: 압축 지원: `.gz`, `.bz2`, `.xz`

## 5. Optimization -- `ase.optimize`
```python
from ase.optimize import BFGS, LBFGS, FIRE, GPMin, MDMin
from ase.optimize import BFGSLineSearch as QuasiNewton
from ase.optimize.precon import PreconLBFGS  # 대형 시스템용

# 사용: opt = BFGS(atoms, trajectory='opt.traj')
#       opt.run(fmax=0.05, steps=1000)  # fmax: eV/Ang
```
WARNING: Optimizer는 원자 위치만 최적화. **셀 최적화는 Filter 필요** (7번 참조).

## 6. Molecular Dynamics -- `ase.md`
```python
from ase.md.verlet import VelocityVerlet          # NVE  -- ase.md.verlet (not velocityverlet)
from ase.md.langevin import Langevin              # NVT
from ase.md.bussi import Bussi                    # NVT
from ase.md.nptberendsen import NPTBerendsen      # NPT
from ase.md.nose_hoover_chain import NoseHooverChainNVT, MTKNPT, IsotropicMTKNPT
from ase.md.langevinbaoab import LangevinBAOAB

from ase.md.velocitydistribution import (  # velocitydistribution (밑줄 없음!)
    MaxwellBoltzmannDistribution,
    Stationary,    # COM 이동 제거
    ZeroRotation,  # 회전 제거
)
```
WARNING: 초기 속도: `MaxwellBoltzmannDistribution(atoms, temperature_K=300)` -- `temperature_K` 키워드 사용.
WARNING: `Stationary(atoms)` -- MD 시작 전 반드시 호출 (COM drift 방지).
WARNING: Langevin: `Langevin(atoms, timestep=5*units.fs, temperature_K=300, friction=0.01/units.fs)` -- 키워드 인자 사용.
WARNING: VelocityVerlet: `VelocityVerlet(atoms, timestep=5*units.fs)`
WARNING: 온도 읽기: `atoms.get_temperature()` 사용 (수동 계산 불필요).

## 7. Constraints & Filters
```python
# Constraints -- ase.constraints
from ase.constraints import (
    FixAtoms,          # FixAtoms(indices=[0,1,2]) 또는 FixAtoms(mask=[...])
    FixBondLength,     # FixBondLength(a1, a2)
    FixBondLengths,    # FixBondLengths(pairs=[[0,1],[2,3]])
    FixLinearTriatomic,
    FixedLine, FixedPlane,
    FixInternals,      # bond/angle/dihedral 내부 좌표
    FixSymmetry,
    Hookean,
    ExternalForce,
    FixCom,
)
# atoms.set_constraint([c1, c2])

# Filters -- ase.filters (constraints 아님!)
from ase.filters import (
    FrechetCellFilter,  # 셀+위치 동시 최적화 (추천)
    ExpCellFilter,      # 셀+위치 (구버전)
    UnitCellFilter,     # 셀+위치
    StrainFilter,       # 셀만 (scaled positions 고정)
)
# 사용: opt = BFGS(FrechetCellFilter(atoms))
```

## 8. Analysis
```python
# Vibrations -- ase.vibrations (Vibrations 복수형!)
from ase.vibrations import Vibrations
from ase.vibrations import Infrared
from ase.vibrations.raman import StaticRamanCalculator

# Phonons
from ase.phonons import Phonons

# MEP -- ase.mep (ase.neb 아님!)
from ase.mep import NEB, DyNEB
from ase.mep.autoneb import AutoNEB
from ase.mep.dimer import DimerControl

# DFT tools -- ase.dft
from ase.dft.kpoints import bandpath
from ase.dft.dos import DOS
from ase.dft.bandgap import bandgap

# EOS -- ase.eos (ase.utils.eos 아님!)
from ase.eos import EquationOfState  # eos = EquationOfState(V, E, eos='birchmurnaghan')
                                     # v0, e0, B = eos.fit()

# Thermochemistry
from ase.thermochemistry import IdealGasThermo, HarmonicThermo, CrystalThermo
```
WARNING: `vib.get_frequencies()` -- cm^-1 numpy 배열 반환. **파라미터 없음** (`units=` 인자 없음).
WARNING: `vib.get_energies()` -- eV numpy 배열 반환.
WARNING: NEB 이미지: `images = [initial] + [initial.copy() for _ in range(N)] + [final]` -- 반드시 `.copy()`.

## 9. Database & Utilities
```python
from ase.db import connect  # db = connect('file.db'); db.write(atoms, key=value)
from ase.data import atomic_numbers, atomic_masses, covalent_radii
from ase.collections import g2, s22
from ase.neighborlist import NeighborList, natural_cutoffs
from ase.geometry import get_distances
from ase.spacegroup import crystal  # crystal('Al', [(0,0,0)], spacegroup=225, ...)
from ase.phasediagram import PhaseDiagram
from ase.cluster import Octahedron, Icosahedron, Decahedron  # 대문자! ase.cluster 모듈
from ase.visualize import view
```

## Quick Recipes

### Bulk 최적화 (셀 + 위치)
```python
atoms = bulk('Cu','fcc',a=3.5); atoms.calc = EMT()
BFGS(FrechetCellFilter(atoms)).run(fmax=0.01)
```

### Slab + 흡착 + relaxation
```python
slab = fcc111('Pt', size=(2,2,4), vacuum=10.0)
co = molecule('CO')
add_adsorbate(slab, co, height=1.8, position='ontop')  # slab이 직접 변경됨
slab.set_constraint(FixAtoms(mask=[a.tag >= 3 for a in slab]))
slab.calc = EMT()
BFGS(slab).run(fmax=0.05)
```

### MD (NVT, 300K)
```python
atoms.calc = EMT()
MaxwellBoltzmannDistribution(atoms, temperature_K=300)
Stationary(atoms)
Langevin(atoms, timestep=5*units.fs, temperature_K=300, friction=0.01/units.fs).run(1000)
```

### NEB
```python
images = [initial] + [initial.copy() for _ in range(5)] + [final]
neb = NEB(images)
neb.interpolate(method='idpp')
for img in images[1:-1]: img.calc = EMT()
BFGS(neb).run(fmax=0.05)
```

### Vibrations (반드시 구조 최적화 후!)
```python
atoms = molecule('N2'); atoms.calc = EMT()
BFGS(atoms).run(fmax=0.01)  # 최적화 먼저!
vib = Vibrations(atoms, name='vib')
vib.run()
freqs = vib.get_frequencies()  # cm^-1 numpy 배열, 파라미터 없음
vib.summary()
vib.clean()
```

### EOS 피팅
```python
from ase.eos import EquationOfState
cell = atoms.get_cell()
volumes, energies = [], []
for x in np.linspace(0.95, 1.05, 7):
    a = atoms.copy(); a.set_cell(cell * x, scale_atoms=True); a.calc = EMT()
    volumes.append(a.get_volume()); energies.append(a.get_potential_energy())
eos = EquationOfState(volumes, energies, eos='birchmurnaghan')
v0, e0, B = eos.fit()
```

### I/O (POSCAR)
```python
write('POSCAR', atoms, format='vasp')  # 'vasp' not 'poscar'
atoms_read = read('POSCAR', format='vasp')
```

### 나노입자
```python
from ase.cluster import Octahedron  # 대문자
atoms = Octahedron('Cu', length=5)
```

### Thermochemistry
```python
from ase.thermochemistry import IdealGasThermo
thermo = IdealGasThermo(vib_energies=vib_energies, atoms=atoms,
                        geometry='linear', symmetrynumber=2, spin=0)
G = thermo.get_gibbs_energy(temperature=298.15, pressure=101325)
```
