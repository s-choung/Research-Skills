# ASE Skill — Library Reference

> ASE 3.27 (Atomic Simulation Environment). 이 레퍼런스로 Python 스크립트 작성 시 import 경로, 클래스명, 핵심 파라미터를 확인.

## 1. Core Objects
```python
from ase import Atoms           # Atoms(symbols, positions=, cell=, pbc=)
from ase.atom import Atom       # 단일 원자
from ase.cell import Cell       # 3x3 unit cell
from ase import units           # units.fs, units.kB, units.bar, units.kJ, units.Bohr, units.Hartree
```

## 2. Structure Building — `ase.build`
```python
from ase.build import (
    bulk,                  # bulk('Cu','fcc', a=3.6, cubic=True, orthorhombic=True)
    molecule,              # molecule('H2O') — G2 database (H2O, CO2, CH4, NH3, C60 등)
    fcc111, fcc100, fcc110, fcc211,  # fcc 표면 — size=(x,y,layers), vacuum=, a=
    bcc100, bcc110, bcc111,          # bcc 표면
    hcp0001, hcp10m10,               # hcp 표면
    diamond100, diamond111,          # diamond 표면
    mx2,                   # mx2('MoS2', kind='2H', a=3.18, thickness=3.17, vacuum=10) — 2D MX2
    surface,               # surface(lattice, indices, layers) — 일반 Miller index 표면
    add_adsorbate,         # add_adsorbate(slab, adsorbate_Atoms, height, position='ontop')
                           #   adsorbate는 Atoms 객체로 전달, 문자열은 단일 원소만 가능
    add_vacuum,            # add_vacuum(atoms, vacuum) — z방향 진공 추가
    nanotube,              # nanotube(n, m, length=, bond=, symbol=)
    graphene_nanoribbon,   # graphene_nanoribbon(n, m, type='armchair'|'zigzag')
    make_supercell,        # make_supercell(atoms, P) — P는 3x3 변환 행렬
    cut, stack, sort,      # 슬랩 조작 유틸리티
    niggli_reduce,         # Niggli cell reduction
    minimize_tilt,         # 기울기 최소화
)
```

## 3. Calculators — `ase.calculators`
```python
# Built-in (Python, 외부 코드 불필요)
from ase.calculators.emt import EMT          # EMT() — FCC 금속 (Cu,Ag,Au,Ni,Pd,Pt,Al)
from ase.calculators.eam import EAM          # EAM(potential='file.alloy')
from ase.calculators.tersoff import Tersoff  # Tersoff 포텐셜
# lj, morse도 내장

# External wrappers (외부 코드 필요)
from ase.calculators.vasp import Vasp            # VASP
from ase.calculators.espresso import Espresso     # Quantum ESPRESSO
from ase.calculators.gaussian import Gaussian     # Gaussian
from ase.calculators.cp2k import CP2K             # CP2K
from ase.calculators.aims import Aims             # FHI-aims
from ase.calculators.orca import ORCA             # ORCA
from ase.calculators.siesta import Siesta         # SIESTA
from ase.calculators.abinit import Abinit         # ABINIT
from ase.calculators.nwchem import NWChem         # NWChem
from ase.calculators.lammps import LAMMPSlib      # LAMMPS (library)
from ase.calculators.dftb import Dftb             # DFTB+
from ase.calculators.gulp import GULP             # GULP
from ase.calculators.castep import Castep         # CASTEP
from ase.calculators.psi4 import Psi4             # Psi4

# Meta-calculators
from ase.calculators.mixing import SumCalculator, MixedCalculator  # 합산/혼합
from ase.calculators.socketio import SocketIOCalculator  # i-PI 소켓
from ase.calculators.qmmm import EIQMMM, SimpleQMMM     # QM/MM

# 연결: atoms.calc = EMT()  ->  항상 optimizer/MD 전에 설정
# 설정: ~/.config/ase/config.ini 또는 ASE_CONFIG_PATH
```

## 4. I/O — `ase.io`
```python
from ase.io import read, iread, write
# read('file.xyz')  read('POSCAR', format='vasp')  read('input.traj', index=':')
# write('out.xyz', atoms)  write('POSCAR', atoms, format='vasp')
# format 이름: 'vasp' (not 'poscar'), 'espresso-in', 'gaussian-in', 'xyz', 'extxyz', 'cif', 'pdb', 'lammps-data'
# 압축 지원: .gz, .bz2, .xz

from ase.io.trajectory import Trajectory  # Trajectory('file.traj', 'w', atoms)
```

## 5. Optimization — `ase.optimize`
```python
from ase.optimize import BFGS, LBFGS, FIRE, GPMin, MDMin
from ase.optimize import BFGSLineSearch as QuasiNewton  # alias
from ase.optimize.precon import PreconLBFGS  # 대형 시스템용

# 사용: opt = BFGS(atoms, trajectory='opt.traj')
#       opt.run(fmax=0.05, steps=1000)  # fmax: eV/Ang
# Optimizer는 내부 원자 위치만 최적화. 셀은 Filter 필요 (7)
```

## 6. Molecular Dynamics — `ase.md`
```python
from ase.md.verlet import VelocityVerlet          # NVE
from ase.md.langevin import Langevin              # NVT (추천)
from ase.md.bussi import Bussi                    # NVT (추천)
from ase.md.nose_hoover_chain import NoseHooverChainNVT  # NVT
from ase.md.nptberendsen import NPTBerendsen      # NPT
from ase.md.nose_hoover_chain import MTKNPT, IsotropicMTKNPT  # NPT
from ase.md.langevinbaoab import LangevinBAOAB    # NVE/NVT/NPT 겸용
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary, ZeroRotation

# 사용: dyn = Langevin(atoms, timestep=5*units.fs, temperature_K=300, friction=0.01/units.fs)
#       dyn.run(1000)
# 단위: timestep -> units.fs, friction -> /units.fs, temperature -> temperature_K (Kelvin)
# 초기 속도: MaxwellBoltzmannDistribution(atoms, temperature_K=300)
#            Stationary(atoms)  # COM 이동 제거
```

## 7. Constraints & Filters
```python
# Constraints — ase.constraints
from ase.constraints import (
    FixAtoms,          # FixAtoms(indices=[0,1,2]) 또는 FixAtoms(mask=[True,False,...])
    FixBondLength,     # FixBondLength(a1, a2)
    FixBondLengths,    # FixBondLengths(pairs=[[0,1],[2,3]]) — 다중 결합
    FixLinearTriatomic,# FixLinearTriatomic(triples=[(1,0,2)])
    FixedLine,         # 직선 방향 구속
    FixedPlane,        # 평면 구속
    FixInternals,      # bond/angle/dihedral 내부 좌표
    FixSymmetry,       # 대칭 보존
    Hookean,           # 스프링 구속
    ExternalForce,     # 외력
    FixCom,            # 질량중심 고정
)
# atoms.set_constraint([c1, c2])  # 다중 구속 가능

# Filters — ase.filters (constraints 아님!)
from ase.filters import (
    FrechetCellFilter,  # 셀+위치 동시 최적화 (추천)
    ExpCellFilter,      # 셀+위치 (구버전 추천)
    UnitCellFilter,     # 셀+위치
    StrainFilter,       # 셀만 (scaled positions 고정)
    Filter,             # 원자 숨기기
)
# 사용: opt = BFGS(FrechetCellFilter(atoms))
```

## 8. Analysis
```python
# Vibrations — ase.vibrations (Vibrations 복수형!)
from ase.vibrations import Vibrations  # vib = Vibrations(atoms); vib.run(); vib.summary()
from ase.vibrations import Infrared    # IR 스펙트럼
from ase.vibrations.raman import StaticRamanCalculator  # 라만

# Phonons
from ase.phonons import Phonons  # 주기계 포논 (small displacement)

# MEP — ase.mep (ase.neb 아님!)
from ase.mep import NEB, DyNEB         # images = [initial] + [initial.copy() for _ in range(N)] + [final]
from ase.mep.autoneb import AutoNEB    # neb.interpolate(method='idpp')
from ase.mep.dimer import DimerControl # NEB 이미지는 반드시 .copy() 사용

# DFT tools — ase.dft
from ase.dft.kpoints import bandpath   # path = bandpath('GXWLGK', cell, npoints=100)
from ase.dft.dos import DOS            # 상태밀도
from ase.dft.bandgap import bandgap    # 밴드갭 계산

# EOS — ase.eos (ase.utils.eos 아님!)
from ase.eos import EquationOfState    # eos = EquationOfState(V, E, eos='birchmurnaghan')
                                       # v0, e0, B = eos.fit()

# Thermochemistry
from ase.thermochemistry import IdealGasThermo, HarmonicThermo, CrystalThermo
```

## 9. Database & Utilities
```python
from ase.db import connect  # db = connect('file.db'); db.write(atoms, key=value); db.select(...)
from ase.data import atomic_numbers, atomic_masses, covalent_radii  # 원소 데이터
from ase.collections import g2, s22  # 분자 컬렉션
from ase.neighborlist import NeighborList, natural_cutoffs
from ase.geometry import get_distances
from ase.spacegroup import crystal  # crystal('Al', [(0,0,0)], spacegroup=225, ...)
from ase.phasediagram import PhaseDiagram
from ase.cluster import Octahedron, Icosahedron, Decahedron  # 나노입자/클러스터
from ase.visualize import view  # view(atoms) — GUI 뷰어
```

## Quick Recipes
```python
# Bulk 최적화 (셀 + 위치)
atoms = bulk('Cu','fcc',a=3.5); atoms.calc = EMT()
BFGS(FrechetCellFilter(atoms)).run(fmax=0.01)

# Slab relaxation (하부 고정)
slab = fcc111('Pt', size=(2,2,4), vacuum=10.0); slab.calc = EMT()
slab.set_constraint(FixAtoms(mask=[a.tag >= 3 for a in slab]))
BFGS(slab).run(fmax=0.05)

# MD (NVT, 300K)
atoms.calc = EMT()
MaxwellBoltzmannDistribution(atoms, temperature_K=300); Stationary(atoms)
Langevin(atoms, 5*units.fs, temperature_K=300, friction=0.01/units.fs).run(1000)

# NEB
images = [initial] + [initial.copy() for _ in range(5)] + [final]
NEB(images).interpolate(method='idpp')
for img in images[1:-1]: img.calc = EMT()
BFGS(NEB(images)).run(fmax=0.05)
```
