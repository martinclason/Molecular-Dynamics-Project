"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import SimpleCubic, BodyCenteredCubic, FaceCenteredCubic,Diamond
from ase.lattice.tetragonal import SimpleTetragonal, CenteredTetragonal
from ase.lattice.orthorhombic import SimpleOrthorhombic, BaseCenteredOrthorhombic,FaceCenteredOrthorhombic, BodyCenteredOrthorhombic
from ase.lattice.monoclinic import SimpleMonoclinic, BaseCenteredMonoclinic
from ase.lattice.triclinic import Triclinic
from ase.lattice.hexagonal import Hexagonal, HexagonalClosedPacked, Graphite

from ase.md.velocitydistribution import MaxwellBoltzmannDistribution


from asap3 import Trajectory
from ase import units
import numpy as np

import argparse


# Adds parser so user can choose if to use asap or not with flags from terminal
parser = argparse.ArgumentParser()
parser.add_argument('--asap', dest='asap', action='store_true')
parser.add_argument('--no-asap', dest='asap', action='store_false')
parser.set_defaults(feature=True)
args = parser.parse_args()

import yaml

config_file = open("config.yaml")
parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

# Use Asap for a huge performance increase if it is installed

def density():
    atoms = createAtoms() #
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

def pressure(forces, volume, positions, temperature,
    number_of_atoms, kinetic_energy):

    forces_times_positions = sum(np.dot(x,y) for x, y in zip(positions, forces))

    instant_pressure = (1/3 * volume) * ((2 * number_of_atoms * kinetic_energy)
                            + forces_times_positions)

    print("The instant pressure is: " + str(instant_pressure))

    return pressure

def MD():
    use_asap = args.asap

    if use_asap:
        print("Running with asap")
        from asap3 import EMT
        from asap3.md.verlet import VelocityVerlet
    else:
        print("Running with ase")
        from ase.calculators.emt import EMT
        from ase.md.verlet import VelocityVerlet
    # Set up a crystal
    atoms = createAtoms()

    # Describe the interatomic interactions with the Effective Medium Theory
    atoms.calc = EMT()

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=parsed_config_file["temperature_K"])
    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.
    if parsed_config_file["make_traj"]:
        traj = Trajectory(parsed_config_file["symbol"]+".traj", "w", atoms, properties="forces")
        dyn.attach(traj.write, interval=10)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))


    # Now run the dynamics
    dyn.attach(printenergy, interval=10)
    printenergy()
    dyn.run(200)
    if parsed_config_file["make_traj"]:
        traj.close()
        traj_read = Trajectory(parsed_config_file["symbol"]+".traj")
        print(traj_read[0].get_positions()[0])

        return traj_read


def main():
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

        pressure(atoms_forces, atoms_volume, atoms_positions, atoms_temperature,
        atoms_number_of_atoms, atoms_kinetic_energy)

def createAtoms() :
     directions=parsed_config_file["directions"]
     symbol=parsed_config_file["symbol"]
     size=(parsed_config_file["size"],
     parsed_config_file["size"],parsed_config_file["size"])
     pbc= parsed_config_file["pbc"]
     latticeconstants = parsed_config_file["latticeconstants"]
     structure = parsed_config_file["structure"]
     if(structure == "SC") :
        return SimpleCubic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = latticeconstants[0])
     if(structure == "BCC") :
        return BodyCenteredCubic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = latticeconstants[0])
     if(structure == "FCC") :
        return FaceCenteredCubic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = latticeconstants[0])
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
        print("Triclinic")
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


main()
