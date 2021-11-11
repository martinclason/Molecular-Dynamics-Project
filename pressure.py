from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from ase.visualize import view
from asap3 import Trajectory
#from ase.io import read

atoms = FaceCenteredCubic(
      directions = [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
      symbol = "Cu",
      size = (10, 10, 10),
      pbc = True)

atoms_volume_init = atoms.get_volume()
print ("Initial volume is: " + str(atoms_volume_init))

atoms_temp_init = atoms.get_temperature()
print ("Initial temperature is: " + str(atoms_temp_init))



###view(atoms)

# Use Asap for a huge performance increase if it is installed
use_asap = True

if use_asap:
       from asap3 import EMT
       size = 10
else:
       from ase.calculators.emt import EMT
       size = 3

# Describe the interatomic interactions with the Effective Medium Theory
atoms.calc = EMT()

    # Set the momenta corresponding to T=300K
MaxwellBoltzmannDistribution(atoms, temperature_K=3000)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.


traj = Trajectory("cu.traj", "w", atoms)
dyn.attach(traj.write, interval=10)
dyn.run(1000)

traj.close()
traj_read = Trajectory("cu.traj")
###atoms_volume_final = traj_read[0].get_volume()[0]
###print("Final volume is: " + str(atoms_volume_final))
print("Final volume is: " +  str(traj_read[10].get_volume()))
print("Final temperature is: " +  str(traj_read[10].get_temperature()))
