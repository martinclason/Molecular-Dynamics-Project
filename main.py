"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import SimpleCubic, BodyCenteredCubic, FaceCenteredCubic,Diamond
from ase.lattice.tetragonal import SimpleTetragonal, CenteredTetragonal
from ase.lattice.orthorhombic import SimpleOrthorhombic, BaseCenteredOrthorhombic,FaceCenteredOrthorhombic, BodyCenteredOrthorhombic
from ase.lattice.monoclinic import SimpleMonoclinic, BaseCenteredMonoclinic
from ase.lattice.triclinic import Triclinic
from ase.lattice.hexagonal import Hexagonal, HexagonalClosedPacked, Graphite


import matplotlib.pyplot as plt
import math

from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)
from ase.md.verlet import VelocityVerlet

from asap3 import Trajectory
from ase import units
import numpy as np

import os
import sys
import argparse
import yaml

root_d = os.path.dirname(__file__)

"""There is a parser for passing flags from the command line to the MD which enables
or disables the use of asap on the current run with the flags '--asap' for enable-
ing it and '--no-asap' to disable it.

Passing this flag is to avoid getting the error 'illegal instruction (core dumped)'
in the terminal since some machines cannot run the current version of ASAP which
is used in this project. """

# Adds parser so user can choose if to use asap or not with flags from terminal
parser = argparse.ArgumentParser()

# parser.add_argument('--asap', dest='asap', action='store_true')
# parser.add_argument('--no-asap', dest='asap', action='store_false')
# parser.set_defaults(feature=True)
# args = parser.parse_args()

config_file = open("config.yaml")
# Could be changed to current working directory
#config_file = open(os.path.join(root_d, "config.yaml"))
parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

# Use Asap for a huge performance increase if it is installed

def density():
    """The function 'density()' takes no argument and calculates the density
    of the material defined in 'config.yaml' with the lattice constant and
    element defined in that file."""

    atoms = createAtoms()
    Element = parsed_config_file["Element"]
    #Properties for element
    Z = parsed_config_file["Z"] #Number of atoms
    M = parsed_config_file["M"] #Molar mass
    Na = parsed_config_file["Na"] #avogadros constant
    a = parsed_config_file["a"] # Lattice constant
    unitCellVolume = a**3
    density = Z * M / (Na * unitCellVolume)

    print('The density of ' + Element + ' is: ' + str(density) + " g/cm^3")

    return density

def pressure(forces, volume, positions, temperature, number_of_atoms, kinetic_energy):

    forces_times_positions = sum(np.dot(x,y) for x, y in zip(positions, forces))

    instant_pressure = (1/3 * volume) * ((2 * number_of_atoms * kinetic_energy)
                            + forces_times_positions)

    print("The instant pressure is: " + str(instant_pressure))

    return instant_pressure


def MD():
    """The function 'MD()' runs defines the ASE and ASAP enviroment to run the
    molecular dynamics simulation with. The elements and configuration to run
    the MD simulation is defined in the 'config.yaml' file which needs to be
    present in the same directory as the MD program (the 'main.py' file)."""

    use_asap = args.asap

    use_asap = True

    atomic_number = parsed_config_file["atomic_number"]
    epsilon = parsed_config_file["epsilon"] * units.eV
    sigma = parsed_config_file["sigma"] * units.Ang
    cutoff = parsed_config_file["cutoff"] * units.Ang
    iterations = parsed_config_file["iterations"] if parsed_config_file["iterations"] else 200
    interval = parsed_config_file["interval"] if parsed_config_file["interval"] else 10

    if use_asap:
        print("Running with asap")
        from asap3 import EMT
        from asap3.md.verlet import VelocityVerlet
        from asap3 import LennardJones
    else:
        print("Running with ase")
        from ase.calculators.emt import EMT
        from ase.calculators.lj import LennardJones
        from ase.md.verlet import VelocityVerlet

    size = parsed_config_file["size"]

    # Set up a crystal
    atoms = createAtoms()

    # Describe the interatomic interactions with the Effective Medium Theory

    potential = parsed_config_file["potential"]
    if potential :
        known_potentials = {
        'EMT' : EMT(),
        'LJ' : LennardJones([atomic_number], [epsilon], [sigma],
                    rCut=cutoff, modified=True,),
        }

    atoms.calc = known_potentials[potential] if potential else EMT()

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=parsed_config_file["temperature_K"])
    Stationary(atoms)
    ZeroRotation(atoms)
    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.
    if parsed_config_file["make_traj"]:
        traj = Trajectory(parsed_config_file["symbol"]+".traj", "w", atoms, properties="forces")
        dyn.attach(traj.write, interval=interval)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))

    def printpressure(b=atoms):
         """Function to calculate and print the instant pressure in XXX for every timestep """
         forces_times_positions = sum(np.dot(x,y) for x, y in
                                zip(b.get_positions(), b.get_forces()))

         instant_pressure = ((1/(3 * b.get_volume())) * ((2 * len(b) *
         b.get_kinetic_energy()) + forces_times_positions))

         print("The instant pressure is: " + str(instant_pressure))

#Calculates MSD for one time step from .traj file
    def MSD(t,atom_list):
        r0 = atom_list[0].get_positions()
        rt = atom_list[t].get_positions()
        N = len(r0)
        diff= rt-r0
        squareddiff = diff**2
        summ = sum(sum(squareddiff))
        normsum = (1/N) * summ
        #return math.sqrt(normsum[0]**2 + normsum[1]**2 + normsum[2]**2)
        return normsum
#Calculates MSD for all the time steps and plots them
    def MSD_plot(time,atom_list):
        MSD_data = []
        for t in range(time):
            MSD_data.append(MSD(t,atom_list))
        plt.plot(range(time),MSD_data)
        plt.ylabel("MSD-[Å]")
        plt.xlabel("Measured time step")
        plt.title("Mean Square Displacement")
        plt.show()

    def self_diffusion_coefficient(t, atom_list) : #for liquids only
        """The self_diffusion_coefficient(t, atom_list) function calculates and returns the
        self diffusion coefficient for a liquid. The function takes two arguments, the time
        t and an atom_list which it sends to the MSD(t,atom_list) function to retrieve the
        MSD. The self diffusion coefficient is then taken as the slope of the
        mean-square-displacement."""
        return 1/(6*t) * MSD(t, atom_list)

    # Now run the dynamics
    dyn.attach(printenergy, interval=interval)
    printenergy()
    dyn.attach(printpressure, interval =interval)
    printpressure()
    dyn.run(iterations)
    if parsed_config_file["make_traj"]:
        traj.close()
        traj_read = Trajectory(parsed_config_file["symbol"]+".traj")
        print(len(traj_read[0].get_positions()))
        print(MSD(0,traj_read))
        print("The self diffusion coefficient is:", self_diffusion_coefficient(10,traj_read)) # TODO: Determine how long we should wait, t should approach infinity
        MSD_plot(len(traj_read),traj_read)

        # TODO: Should this be here?
        return traj_read


def main():
    """The 'main()' function runs the 'MD()' function which runs the simulation.
    'main()' also prints out the density or other properties of the material at
    hand (which is to be implemented in future versions of this program, as of
    only density excists). What to print out during the run is defined in the
    'config.yaml' file."""

    run_density = parsed_config_file["run_density"]
    run_MD = parsed_config_file["run_MD"]
    run_pressure = parsed_config_file["run_pressure"]

    if run_density :
        density()

    if run_MD :

        traj_results = MD()

        atoms_volume = traj_results[1].get_volume()
        atoms_positions = traj_results[1].get_positions()
        atoms_kinetic_energy = traj_results[1].get_kinetic_energy()
        atoms_forces = traj_results[1].get_forces()
        atoms_temperature = traj_results[1].get_temperature()
        atoms_number_of_atoms = len(atoms_positions)
        print("Number of atoms: " + str(atoms_number_of_atoms))

    if run_pressure :

        pressure(
            atoms_forces,
            atoms_volume,
            atoms_positions,
            atoms_temperature,
            atoms_number_of_atoms,
            atoms_kinetic_energy
        )


def createAtoms() :
    """createAtoms() loads material parameters from the config.yaml file and
   returns a solid slab of a material in the form of an Atoms object with
   one of the 14 bravais lattice structures. The HCP and H structures
   require a 4-index input for each direction (Miller-Bravais-notation) and
   will return a SC atoms object if the user fails to use the correct input
   for those structures."""
    directions = parsed_config_file["directions"]
    symbol = parsed_config_file["symbol"]
    size = (parsed_config_file["size"], parsed_config_file["size"], parsed_config_file["size"])
    pbc = parsed_config_file["pbc"]
    latticeconstants = parsed_config_file["latticeconstants"]
    structure = parsed_config_file["structure"]
    if(structure == "SC") :
        return SimpleCubic(directions = directions,
                           symbol = symbol,
                           size = size,
                           pbc = pbc,
                           latticeconstant = latticeconstants[0] if latticeconstants else None)
    if(structure == "BCC") :
        return BodyCenteredCubic(directions = directions,
                                 symbol = symbol,
                                 size = size,
                                 pbc = pbc,
                                 latticeconstant = latticeconstants[0] if latticeconstants else None)
    if(structure == "FCC") :
        return FaceCenteredCubic(directions = directions,
                                 symbol = symbol,
                                 size = size,
                                 pbc = pbc,
                                 latticeconstant = latticeconstants[0] if latticeconstants else None)
    if(structure == "ST") :
        return SimpleTetragonal(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'c' : latticeconstants[2]})
    if(structure == "CT") :
        return CenteredTetragonal(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'c' : latticeconstants[2]})
    if(structure == "SO") :
        return SimpleOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
    if(structure == "BaCO") :
        return BaseCenteredOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
    if(structure == "FCO") :
        return FaceCenteredOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
    if(structure == "BCO") :
        return BodyCenteredOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
    if(structure == "SM") :
        return SimpleMonoclinic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2],
                                                   'alpha' : latticeconstants[3]})
    if(structure == "BCM") :
        return BaseCenteredMonoclinic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2],
                                                   'alpha' : latticeconstants[3]})
    if(structure == "T") :
        return Triclinic(directions = directions,
                            symbol = symbol,
                            size = size, pbc = pbc,
                            latticeconstant = {'a' : latticeconstants[0],
                                               'b' : latticeconstants[1],
                                               'c' : latticeconstants[2],
                                               'alpha' : latticeconstants[3],
                                               'beta' : latticeconstants[4],
                                               'gamma' : latticeconstants[5]})
    if(structure == "H") :
        if(len(directions) != 4) :
            print("Incorrect number of directional indices for hexagonal structure, use the 4" +
            "-index Miller-Bravais notation, creating SC-lattice instead")
            return SimpleCubic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = latticeconstants[0])
        return Hexagonal(directions = directions,
                         symbol = symbol,
                         size = size, pbc = pbc,
                         latticeconstant = {'a' : latticeconstants[0],
                                            'c' : latticeconstants[2]})

    if(structure == "HCP") :
        if(len(directions) != 4) :
             print("Incorrect number of directional indices for hexagonal structure, use the 4" +
             "-index Miller-Bravais notation, creating SC-lattice instead")
             return SimpleCubic(directions = directions,
                                     symbol = symbol,
                                     size = size, pbc = pbc,
                                     latticeconstant = latticeconstants[0])
        return HexagonalClosedPacked(directions = directions,
                                        symbol = symbol,
                                        size = size, pbc = pbc,
                                        latticeconstant = {'a' : latticeconstants[0],
                                                           'c' : latticeconstants[2]})


if __name__ == "__main__":
    # Adds parser so user can choose if to use asap or not with flags from terminal

    parser.add_argument('--asap', dest='asap', action='store_true')
    parser.add_argument('--no-asap', dest='asap', action='store_false')
    parser.set_defaults(feature=True)
    args = parser.parse_args()

    main()
