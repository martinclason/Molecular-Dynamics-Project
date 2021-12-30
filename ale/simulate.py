from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)

#from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin

# Use ase.io to make traj-writing from different processes work
from ase.io import Trajectory
import numpy as np
from ase import units


from ale.createAtoms import createAtoms
from ale.equilibriumCondition import equilibiriumCheck
from ase.calculators.kim.kim import KIM
from ale.simulationDataIO import outputGenericFromTraj, outputSingleProperty
from ale.errors import ConfigError
from ale.cohesive_energy import cohesive_energy, retrieve_cohesive_energy
from ale.create_potential import create_potential, built_in_LennardJones
import os


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
        print("Running dynamics with asap")
        from asap3.md.verlet import VelocityVerlet
    else:
        print("Running with ase")
        from ase.md.verlet import VelocityVerlet

    # Set up a crystal
    atoms = createAtoms(options)
    calc = create_potential(options)
    print(f"Using potential: {calc}")
    atoms.calc = calc
    
    time_step = options["dt"] * units.fs
    temperature = options["temperature_K"]
    nvt_friction = options.get("NVT_friction", 0.002) # default to 0.002
    print(f"nvt_friction {nvt_friction}")

    # Set the momenta corresponding to the temperature
    # The communicator is set to 'serial' to inhibit this function trying 
    # to communicate between processes. This would send a broadcast which seems to deadlock
    # the program if processes calls this function a different number of times.
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature, communicator='serial')
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


    atoms_positions = atoms.get_positions()
    atoms_number_of_atoms = len(atoms_positions)
    print("Number of atoms: " + str(atoms_number_of_atoms))

    dyn.attach(printenergy, interval=interval)
    printenergy()

    # Setup writing of simulation data to trajectory file
    output_dir = options['out_dir']
    main_trajectory_file_name = options['traj_file_name']

    # This process makes the simulation wait for equilibrium before it starts
    # writing data to the outpul .traj-file.
    if options["checkForEquilibrium"]:

        raw_trajectory_file_path = os.path.join(output_dir, f"raw{main_trajectory_file_name}")
        # Defines the full, pre-equilibrium, .traj-file to work with during the simulation
        rawTraj = Trajectory(raw_trajectory_file_path, "w", atoms, properties="energy, forces", master=True)
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
            eqReached = equilibiriumCheck(raw_trajectory_file_path,
                            atoms_number_of_atoms,
                            ensamble,
                            eqCheckInterval)
        
            numberOfChecks = numberOfChecks + 1

            dyn.run(iterationsBetweenChecks)
        
        # When equilibrium is or isn't reached the elapsed time is calculated
        # and a statement is written in the terminal on wheter the system reached
        # equilibrium and how long it took or how long the simulation waited.
        timeToEquilibrium = (initIterations + numberOfChecks*iterationsBetweenChecks) / options["dt"]

        out_file_path = os.path.join(options['out_dir'], options['out_file_name'])

        # Writes meta data about the equilibrium to the output .json-file
        f = open(out_file_path, 'a')
        equilibiriumProp = {
            'Equilibrium reached':
                outputSingleProperty(
                    f,
                    'Equilibrium reached',
                    eqReached
                ),
            'Time before equilibrium':
                outputSingleProperty(
                    f,
                    'Time before equilibrium',
                    timeToEquilibrium
                )
        }

        for prop in list(equilibiriumProp):
            equilibiriumProp[prop]()

        f.close()

        if eqReached:
            print("System reached equilibirium after",timeToEquilibrium,"fs")
        else:
            print("Equilibriumcheck timeout after",timeToEquilibrium,"fs")
            print("Continues")
    coh_E_trajectory_file_name = "_" + options['symbol'] + "_coh_E.traj"
    cohesive_energy_file_path = os.path.join(output_dir, coh_E_trajectory_file_name)
    if options.get("calculateCohesiveEnergy") and eqReached:
        cohesive_energy(options,atoms,initIterations + numberOfChecks*iterationsBetweenChecks,cohesive_energy_file_path)
    elif options.get("calculateCohesiveEnergy") and not eqReached:
        cohesive_energy(options,atoms,options.get("max_iterations_coh_E"),cohesive_energy_file_path)

    # Setup writing of simulation data to trajectory file
    main_trajectory_file_name = options["symbol"]+".traj"
    main_trajectory_file_path = os.path.join(output_dir, main_trajectory_file_name)
    print(f"Traj will be written to: {main_trajectory_file_path}")
    traj = Trajectory(
                main_trajectory_file_path,
                "w", 
                atoms, 
                properties="energy, forces",
                # TODO: Write about how processes seem to work in ase and asap and our tradeoff...
                master=True, # Let processes write to their own respective traj-files
            )
    
    dyn.attach(traj.write, interval=interval)
    
    dyn.run(iterations)

    traj.close()
    print(f"Traj {main_trajectory_file_path} should be written")

    
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
    
