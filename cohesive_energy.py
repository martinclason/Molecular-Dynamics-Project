from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)
from ase.md.verlet import VelocityVerlet
from asap3 import Trajectory
from ase import units
from equilibriumCondition import equilibiriumCheck



def cohesive_energy(atoms,iterations):
    """The cohesive_energy function takes argument atoms, that is the simulated material,
    and makes another simulation for the material at temperature 0 K.
    It the looks extracts the potential energy which is the cohesive energy for the material"""
    MaxwellBoltzmannDistribution(atoms, temperature_K=0)
    Stationary(atoms)
    ZeroRotation(atoms)
    coh_dyn = VelocityVerlet(atoms, 5 * units.fs)
    coh_traj = Trajectory(
                "coh_E.traj", 
                "w", 
                atoms, 
                properties="energy, forces"
            )
    coh_dyn.attach(coh_traj.write, interval=iterations)
    coh_dyn.run(iterations)

def retrieve_cohesive_energy(traj_file):
    traj_read_cohE = Trajectory(traj_file)
    return -traj_read_cohE[-1].get_potential_energy()/len(traj_read_cohE[0].get_positions())
