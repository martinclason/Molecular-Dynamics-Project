"""Demonstrates molecular dynamics with constant energy."""
from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)

#from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin

# Use ase.io to make traj-writing from different processes work
from ase.io import Trajectory
from ase import units
import numpy as np

from createAtoms import createAtoms
from equilibriumCondition import equilibiriumCheck
from ase.calculators.kim.kim import KIM
from simulationDataIO import outputGenericFromTraj
from aleErrors import ConfigError
from cohesive_energy import cohesive_energy, retrieve_cohesive_energy
import os

def built_in_LennardJones(options, use_asap):
    # Fallback/default values if not present in config
    fallback_atomic_number = 1
    fallback_epsilon = 0.010323 # eV
    fallback_sigma = 3.40 # Å
    fallback_cutoff = 6.625 # Å

    if use_asap:
        print("Running LJ potential with asap")
        from asap3 import LennardJones

        atomic_number = options.get("atomic_number", fallback_atomic_number)
        epsilon = options.get("epsilon", fallback_epsilon) * units.eV
        sigma = options.get("sigma", fallback_sigma) * units.Ang
        cutoff = options.get("cutoff", fallback_cutoff) * units.Ang
        
        keys = ("atomic_number", "epsilon", "sigma", "cutoff")
        if not all (key in options for key in keys):
            print(f"Warning, using fallback values for some values in: {keys}")

        return LennardJones(
                [atomic_number],
                [epsilon],
                [sigma],
                rCut=cutoff,
                modified=True,
            )
    else:
        print("Running LJ potential with ase")
        from ase.calculators.lj import LennardJones

        epsilon = options.get("epsilon", fallback_epsilon) * units.eV
        sigma = options.get("sigma", fallback_sigma) * units.Ang
        
        keys = ("epsilon", "sigma")
        if not all (key in options for key in keys):
            print(f"Warning, using fallback values for some values in: {keys}")

        return LennardJones(
                epsilon=epsilon,
                sigma=sigma,
            )

def create_potential(options, use_asap):
    potential_str = options["potential"]
    if potential_str.lower() in ("lj", "LennardJones".lower()):
        # return built in LennardJones
        return built_in_LennardJones(options, use_asap)
    if "openkim:" in potential_str.lower():
        # extract openKIM id from string prefixed with 'openkim:'
        openKIMpotential_str = potential_str.split(":")[1]
        try:
            return KIM(openKIMpotential_str)
        except:
            raise ConfigError(
                    message=f"A openKIM potential couldn't be created from given config: {openKIMpotential_str}",
                    config_properties=["potential"],
                  )
    raise ConfigError(
                message=f"No potential could be created from given config: {potential_str}",
                config_properties=["potential"],
          )


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
    calc = create_potential(options, use_asap)
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
    if options.get("checkForEquilibrium", None):

        raw_trajectory_file_path = os.path.join(output_dir, f"raw{main_trajectory_file_name}")
        # Defines the full, pre-equilibrium, .traj-file to work with during the simulation
        rawTraj = Trajectory(raw_trajectory_file_path, "w", atoms, properties="energy, forces")
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
        # TODO: Store this information together with the calculate quantities.
        timeToEquilibrium = (initIterations + numberOfChecks*iterationsBetweenChecks) / options["dt"]

        if eqReached:
            print("System reached equilibirium after",timeToEquilibrium,"fs")
        else:
            print("Equilibriumcheck timeout after",timeToEquilibrium,"fs")
            print("Continues")

    if options.get("calculateCohesiveEnergy") and eqReached:
        cohesive_energy(atoms,initIterations + numberOfChecks*iterationsBetweenChecks)
    elif options.get("calculateCohesiveEnergy") and not eqReached:
        cohesive_energy(atoms,options.get("max_iterations_coh_E"))

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
    
