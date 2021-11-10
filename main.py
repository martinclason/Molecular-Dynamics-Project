"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units

import argparse

"""There is a parser for passing flags from the command line to the MD which enables
or disables the use of asap on the current run with the flags '--asap' for enable-
ing it and '--no-asap' to disable it.

Passing this flag is to avoid getting the error 'illegal instruction (core dumped)'
in the terminal since some machines cannot run the current version of ASAP which
is used in this project. """

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
    """The function 'density()' takes no argument and calculates the density
    of the material defined in 'config.yaml' with the lattice constant and 
    element defined in that file."""

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
    
def MD():
    """The function 'MD()' runs defines the ASE and ASAP enviroment to run the 
    molecular dynamics simulation with. The elements and configuration to run
    the MD simulation is defined in the 'config.yaml' file which needs to be 
    present in the same directory as the MD program (the 'main.py' file)."""
    
    use_asap = args.asap

    if use_asap:
        from asap3 import EMT
        size = 10
    else:
        from ase.calculators.emt import EMT
        size = 3
    # Set up a crystal
    atoms = FaceCenteredCubic(directions=parsed_config_file["directions"],
                              symbol=parsed_config_file["symbol"],
                              size=(size, size, size),
                              pbc=True)

    # Describe the interatomic interactions with the Effective Medium Theory
    atoms.calc = EMT()

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=parsed_config_file["temperature_K"])
    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.

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

def main():
    """The 'main()' function runs the 'MD()' function which runs the simulation. 
    'main()' also prints out the density or other properties of the material at 
    hand (which is to be implemented in future versions of this program, as of 
    only density excists). What to print out during the run is defined in the 
    'config.yaml' file."""

    run_density = parsed_config_file["run_density"]
    run_MD = parsed_config_file["run_MD"]
    if run_density :
        density()
    if run_MD :
        MD()

main()
