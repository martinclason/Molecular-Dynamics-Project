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

from equilibriumCondition import equilibiriumCheck

from ase.calculators.kim.kim import KIM

from simulationDataIO import outputGenericFromTraj

def MD(options):
    """The function 'MD()' runs defines the ASE and ASAP enviroment to run the
    molecular dynamics simulation with. The elements and configuration to run
    the MD simulation is defined in the 'config.yaml' file which needs to be
    present in the same directory as the MD program (the 'main.py' file)."""

    # Use Asap for a huge performance increase if it is installed
    use_asap = options["use_asap"]
    iterations = options["iterations"] if options["iterations"] else 200
    interval = options["interval"] if options["interval"] else 10

    if use_asap:
        print("Running with asap")
        from asap3.md.verlet import VelocityVerlet
    else:
        print("Running with ase")
        from ase.md.verlet import VelocityVerlet

    # Set up a crystal
    atoms = createAtoms(options)
    atoms.calc = KIM(options["openKIMid"]) # Attach the openKIM calculator
    
    time_step = options["dt"] * units.fs
    temperature = options["temperature_K"]
    nvt_friction = options.get("NVT_friction", 0.002) # default to 0.002
    print(f"nvt_friction {nvt_friction}")

    # Set the momenta corresponding to the temperature
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)
    # Is this where the temperature is halfed??
    Stationary(atoms)
    ZeroRotation(atoms)

    dynamics_from_ensemble = {
        # Run MD with constant energy using the VelocityVerlet algorithm
        'NVE' : VelocityVerlet(atoms, time_step),
        # Langevin dynamics for NVT dynamics
        'NVT' : Langevin(atoms, time_step, temperature_K=temperature, friction=nvt_friction),
    }

    dyn = dynamics_from_ensemble[options.get("ensemble", "NVE")] # default to NVE

    print(f"Using ensemble: {options['ensemble']}, resulting in dynamics: {type(dyn).__name__}")

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))

    dyn.attach(printenergy, interval=interval)
    printenergy()

    atoms_positions = atoms.get_positions()
    atoms_number_of_atoms = len(atoms_positions)
    print("Number of atoms: " + str(atoms_number_of_atoms))

    # This process makes the simulation wait for equilibrium before it starts
    # writing data to the outpul .traj-file.
    if options.get("checkForEquilibrium", None):
        # Defines the full, pre-equilibrium, .traj-file to work with during the simulation
        rawTraj = Trajectory("raw"+options["symbol"]+".traj", "w", atoms, properties="energy, forces")
        dyn.attach(rawTraj.write, interval=interval)

        # Condtions for equilibrium.
        eqCheckInterval = 10
        initIterations = 2*interval*eqCheckInterval if(interval < 100) else 2000 
        iterationsBetweenChecks = 4*interval # Uses moving averages when checking for equilibrium
        eqLimit = atoms_number_of_atoms if (atoms_number_of_atoms > 30) else 30
        ensamble = options.get("ensemble", "NVE") # default to NVE

        # Variables that are updated in the process
        eqReached = False
        numberOfChecks = 0

        # Runs for first couple of itterations
        dyn.run(initIterations)

        while ((not eqReached) and (not (numberOfChecks > eqLimit))):
            eqReached = equilibiriumCheck("raw"+options["symbol"]+".traj",
                            atoms_number_of_atoms,
                            ensamble,
                            eqCheckInterval)
        
            numberOfChecks = numberOfChecks + 1

            dyn.run(iterationsBetweenChecks)
        
        # When equilibrium is or isn't reached the elapsed time is calculated
        # and a statement is written in the terminal on wheter the system reached
        # equilibrium and how long it took or how long the simulation waited.
        # TODO: Store this information together with the calculate quantities.
        timeToEquilibrium = (initIterations + numberOfChecks*iterationsBetweenChecks) / options["dt"]

        if eqReached:
            print("System reached equilibirium after",timeToEquilibrium,"fs")
        else:
            print("Equilibriumcheck timeout after",timeToEquilibrium,"fs")
            print("Continues")

    # Setup writing of simulation data to trajectory file
    main_trajectory_file_name = options["symbol"]+".traj"
    traj = Trajectory(
                main_trajectory_file_name, 
                "w", 
                atoms, 
                properties="energy, forces"
            )
    
    dyn.attach(traj.write, interval=interval)
    
    dyn.run(iterations)
    
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
    
