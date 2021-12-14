from density import density
from MSD import MSD, self_diffusion_coefficient, lindemann_criterion
from pressure import pressure
from simulationDataIO import outputGenericFromTraj,outputarraytofile, outputSingleProperty
from debye_temperature import debye_temperature
<<<<<<< HEAD
import os
=======
from specificHeatCapacity import specificHeatCapacity
import numpy as np
>>>>>>> develop

def analyse_main(options,traj_read):
    """The function analyse_main takes options and a traj_read as arguments where options are the
    options for analysing the simulated material. It is specified in config file exactly what 
    the user wants to calculate"""


    # Output specified data to outfile
    output_dir = options['out_dir']
    out_file_path = os.path.join(output_dir, options['out_file_name'])

    if options['output']:
        output_properties_to_file(options, traj_read, options['out_file_name'])

def output_properties_to_file(options, traj, out_file_name='out.json'):
    """ Outputs the chosen properties from a traj file to
        json-file.
    """
    with open(out_file_name, 'w+') as f:
        last_atoms_object = traj[-1] #Take the last atoms object
        known_property_outputters = {
            'Temperature' : 
                outputGenericFromTraj(
                    traj,
                    f,
                    'Temperature',
                    lambda atoms: atoms.get_temperature(),
                ),
            'Volume' : 
                outputGenericFromTraj(
                    traj,
                    f,
                    'Volume',
                    lambda atoms: atoms.get_volume(),
                ),
            # 'Debye Temperature' : 
            #     outputSingleProperty(
            #         traj,
            #         f,
            #         'Debye Temperature',
            #         debye_temperature(last_atoms_object)
            #     ),
            'Self Diffusion Coefficient' : 
                outputSingleProperty(
                    traj,
                    f,
                    'Self Diffusion Coefficient',
                    self_diffusion_coefficient(traj)
                ),
            'Density' : 
                outputSingleProperty(
                    traj,
                    f,
                    'Density',
                    density(last_atoms_object)
                ),
            'Pressure' : #TODO: Should this be tagged 'instant' pressure instead?
                outputSingleProperty(
                    traj,
                    f,
                    'Instant Pressure',
                    pressure(last_atoms_object)
                ),
            'Self Diffusion Coefficient Array' :
                outputarraytofile("Self Diffusion Coefficient Array",self_diffusion_coefficient_calc(traj),f),
            'MSD' :
                outputarraytofile("MSD",MSD_data_calc(traj),f),
            'Specific Heat Capacity' :
                outputSingleProperty(
                    traj,
                    f,
                    'Specific Heat Capacity',
                    specificHeatCapacity(options['ensemble'],traj)
                ),
        }

        for prop in options['output']:
            if prop in known_property_outputters:
                known_property_outputters[prop]()

def MSD_data_calc(traj_read):
    """Calculates all MSD for all timesteps registered in the .traj file"""
    MSD_data = np.array([])
    for t in range(len(traj_read)):
        MSD_data = np.append(MSD_data,MSD(t,traj_read))
    return MSD_data

def self_diffusion_coefficient_calc(traj_read):
    sdc = np.array([])
    for t in range(len(traj_read)):
        sdc = np.append(sdc,self_diffusion_coefficient(traj_read))
    return sdc

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
