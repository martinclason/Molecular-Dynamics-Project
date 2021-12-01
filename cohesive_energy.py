from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)
from ase.md.verlet import VelocityVerlet
from ase import units



def cohesive_energy(atoms):
    """The cohesive_energy function takes argument atoms, that is the simulated material,
    and makes another simulation for the material at temperature 0 K.
    It the looks extracts the potential energy which is the cohesive energy for the material"""
    MaxwellBoltzmannDistribution(atoms, temperature_K=0)
    Stationary(atoms)
    ZeroRotation(atoms)
    coh_dyn = VelocityVerlet(atoms, 5 * units.fs)
    def retrieve_potential_energy(a=atoms):
        print("The cohesive energy:" + str(-a.get_potential_energy()/len(a)))
        return a.get_potential_energy()
    coh_dyn.attach(retrieve_potential_energy, interval=1)
    coh_dyn.run(5)
#TODO Implementera så denna skriver ut cohesive energy vid equillibrium