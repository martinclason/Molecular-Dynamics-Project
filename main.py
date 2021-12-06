"""Demonstrates molecular dynamics with constant energy."""
from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)

#from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin

from asap3 import Trajectory
from ase import units
import numpy as np

from pressure import pressure, printpressure
from createAtoms import createAtoms
from MSD import MSD, MSD_plot, self_diffusion_coefficient, Lindemann_criterion
from density import density
from debye_temperature import debye_temperature

from ase.calculators.kim.kim import KIM

from simulationDataIO import outputGenericFromTraj

def MD(options):
    """The function 'MD()' runs defines the ASE and ASAP enviroment to run the
    molecular dynamics simulation with. The elements and configuration to run
    the MD simulation is defined in the 'config.yaml' file which needs to be
    present in the same directory as the MD program (the 'main.py' file)."""

    # Use Asap for a huge performance increase if it is installed
    use_asap = options["use_asap"]

    atomic_number = options["atomic_number"]
    epsilon = options["epsilon"] * units.eV
    sigma = options["sigma"] * units.Ang
    cutoff = options["cutoff"] * units.Ang
    iterations = options["iterations"] if options["iterations"] else 200
    interval = options["interval"] if options["interval"] else 10

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

    def LJ(use_asap=use_asap):
        if use_asap:
            return LennardJones(
                [atomic_number],
                [epsilon],
                [sigma],
                rCut=cutoff,
                modified=True)
        else:
            return LennardJones(
                epsilon=epsilon,
                sigma=sigma)

    # Set up a crystal
    atoms = createAtoms(options)

    def OpenKIMPotential():
        try:
            return KIM(options["openKIMid"])
        except:
            return None

    potential = options["potential"]
    if potential :
        known_potentials = {
        'EMT' : EMT(),
        'LJ' : LJ(use_asap),
        'openKIM' : OpenKIMPotential(),
        }

    potential = options["potential"]
    # Default to using EMT
    atoms.calc = known_potentials[potential] if potential else EMT()

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=options["temperature_K"])
    # Is this where the temperature is halfed??
    Stationary(atoms)
    ZeroRotation(atoms)
    
    time_step = options["dt"] * units.fs
    temperature = options["temperature_K"]

    # default to 0.002
    nvt_friction = options.get("NVT_friction", 0.002)
    print(f"nvt_friction {nvt_friction}")

    dynamics_from_ensemble = {
        # Run MD with constant energy using the VelocityVerlet algorithm
        'NVE' : VelocityVerlet(atoms, time_step),
        # Langevin dynamics for NVT dynamics
        'NVT' : Langevin(atoms, time_step, temperature_K=temperature, friction=nvt_friction),
    }

    dyn = dynamics_from_ensemble[options["ensemble"] if ("ensemble" in options) else "NVE"]
    print(f"using {options['ensemble']}", dyn)

    if options["make_traj"]:
        traj = Trajectory(options["symbol"]+".traj", "w", atoms, properties="energy, forces")
        dyn.attach(traj.write, interval=interval)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))

    atoms_positions = atoms.get_positions()
    atoms_number_of_atoms = len(atoms_positions)
    print("Number of atoms: " + str(atoms_number_of_atoms))

    # Now run the dynamics
    dyn.attach(printenergy, interval=interval)
    printenergy()
    dyn.run(iterations)
    if options["make_traj"]:
        traj.close()
        traj_read = Trajectory(options["symbol"]+".traj")
        #print(len(traj_read[0].get_positions()))
        #   print(MSD(0,traj_read))
        #print("The self diffusion coefficient is:", self_diffusion_coefficient(10,traj_read)) # TODO: Determine how long we should wait, t should approach infinity
        #print("Lindemann:", Lindemann_criterion(10, traj_read))
        #MSD_plot(len(traj_read),traj_read)
        print("Debye Temperature:",debye_temperature(traj_read))


def main(options):
    """The 'main()' function runs the 'MD()' function which runs the simulation.
    'main()' also prints out the density or other properties of the material at
    hand (which is to be implemented in future versions of this program, as of
    only density excists). What to print out during the run is defined in the
    'config.yaml' file."""

    MD(options)

if __name__ == "__main__":
    import os
    import sys
    import argparse
    import yaml

    # Adds parser so user can choose if to use asap or not with flags from terminal
    parser = argparse.ArgumentParser()
    parser.add_argument('--asap', dest='use_asap', action='store_true')
    parser.add_argument('--no-asap', dest='use_asap', action='store_false')
    parser.set_defaults(use_asap=True)
    args = parser.parse_args()

    # Parsing yaml config_file
    config_file = open("config.yaml")
    # Could be changed to current working directory
    #root_d = os.path.dirname(__file__)
    #config_file = open(os.path.join(root_d, "config.yaml"))
    parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
    parsed_config_file["use_asap"] = args.use_asap

    main(parsed_config_file)
    
