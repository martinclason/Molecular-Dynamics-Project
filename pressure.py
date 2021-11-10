from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from ase.visualize import view

atoms = FaceCenteredCubic(
      directions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
      symbol = "Cu",
      size = (4, 4, 4),
      pbc = True)

view(atoms)
