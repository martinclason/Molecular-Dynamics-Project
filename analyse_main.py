from density import density
from MSD import MSD, self_diffusion_coefficient, Lindemann_criterion
from pressure import pressure
from outputSimulationData import outputGenericFromTraj

def analyse_main(options,traj_read):
    """The function analyse_main takes options and a traj_read as arguments where options are the
    options for analysing the simulated material. It is specified in config file exactly what 
    the user wants to calculate"""


    run_density = options["run_density"]
    density_time = options["density_time"] if options["density_time"] else 0
    run_MSD = options["run_MSD"]
    MSD_time = options["MSD_time"] if options["MSD_time"] else 0
    run_pressure = options["run_pressure"]
    run_self_diffusion_coefficient = options["run_self_diffusion_coefficient"]
    self_diffusion_coefficient_time = options["self_diffusion_coefficient_time"] if options["self_diffusion_coefficient_time"] else 1


    if run_density:
        density(traj_read,density_time,options)

    if run_MSD:
        MSD(MSD_time, traj_read)
    

    atoms_volume = traj_read[1].get_volume()
    atoms_positions = traj_read[1].get_positions()
    atoms_kinetic_energy = traj_read[1].get_kinetic_energy()
    atoms_forces = traj_read[1].get_forces()
    atoms_temperature = traj_read[1].get_temperature()
    atoms_number_of_atoms = len(atoms_positions)

    if run_pressure:
        pressure(atoms_forces,
            atoms_volume,
            atoms_positions,
            atoms_temperature,
            atoms_number_of_atoms,
            atoms_kinetic_energy)

    if run_self_diffusion_coefficient:
        self_diffusion_coefficient(self_diffusion_coefficient_time, traj_read)

    # Output specified data to outfile
    if options['output']:
        output_properties_to_file(options['output'], traj_read)

def output_properties_to_file(properties, traj):
    """ Outputs the chosen properties from a traj file to
        json-file.
    """
    with open('out.json', 'w+') as f:
        known_property_outputters = {
            'temperature' : 
                outputGenericFromTraj(
                    traj,
                    f,
                    'temperature',
                    lambda atoms: atoms.get_temperature(),
                ),
            'volume' : 
                outputGenericFromTraj(
                    traj,
                    f,
                    'volume',
                    lambda atoms: atoms.get_volume(),
                ),
        }

        for prop in properties:
            if prop in known_property_outputters:
                known_property_outputters[prop]()

if __name__=="__main__":
    from command_line_arg_parser import parser
    from md_config_reader import config_parser as config_file_parser

    from asap3 import Trajectory

    args = parser.parse_args()
    parsed_config_file = config_file_parser(args.config_file)

    options = parsed_config_file
    options['use_asap'] = args.use_asap

    traj_read = Trajectory(options["symbol"]+".traj")
    analyse_main(options,traj_read)