# ASE Skill (Basic)

ASE (Atomic Simulation Environment) is a Python library for atomistic simulations.

## Key Imports
```python
from ase import Atoms
from ase.build import bulk, molecule, fcc111, add_adsorbate, add_vacuum
from ase.io import read, write
from ase.optimize import BFGS
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.mep import NEB
from ase.vibrations import Vibrations
from ase import units
```

## Common Patterns
- Create atoms: `atoms = Atoms('H2O', positions=[(0,0,0), (1,0,0), (0,1,0)])`
- Attach calculator: `atoms.calc = EMT()`
- Get energy: `atoms.get_potential_energy()`
- Optimize: `BFGS(atoms).run(fmax=0.05)`
- Write file: `write('output.xyz', atoms)`
