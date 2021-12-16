from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)
from ase.md.verlet import VelocityVerlet
from ase.io import Trajectory
from ase import units
from equilibriumCondition import equilibiriumCheck
import sys
import os



def cohesive_energy(options,atoms,iterations,file_output_path):
    """The cohesive_energy function takes argument atoms, that is the simulated material,
    and makes another simulation for the material at temperature 0 K.
    It the looks extracts the potential energy which is the cohesive energy for the material"""
    MaxwellBoltzmannDistribution(atoms, temperature_K=0, communicator='serial')
    Stationary(atoms)
    ZeroRotation(atoms)
    coh_dyn = VelocityVerlet(atoms, options.get('dt') * units.fs)
    coh_traj = Trajectory(
                file_output_path, 
                "w", 
                atoms, 
                properties="energy, forces",
                master = True
            )
    coh_dyn.attach(coh_traj.write, interval=iterations)
    print("Calculating Cohesive Energy")
    coh_dyn.run(iterations)
    print("Cohesive Energy calculated and stored in " + os.path.join(os.getcwd(),file_output_path))
    coh_traj.close()

def retrieve_cohesive_energy(traj_file):
    if not os.path.isfile(traj_file):
        return None
    traj_read_cohE = Trajectory(traj_file)
    return -traj_read_cohE[-1].get_potential_energy()/len(traj_read_cohE[0].get_positions())
