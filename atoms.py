from ase.lattice.cubic import FaceCenteredCubic

atoms = FaceCenteredCubic(
      directions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
      symbol = "Cu",
      size = (4, 4, 4),
      pbc = True)

atoms_volume = atoms.get_volume()

print (atoms_volume)
