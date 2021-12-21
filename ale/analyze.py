from ale.density import density
from ale.MSD import MSD, self_diffusion_coefficient, lindemann_criterion
from ale.pressure import pressure, avg_pressure
from ale.simulationDataIO import outputGenericFromTraj, outputSingleProperty, outputGenericResultLazily
from ale.debye_temperature import debye_temperature
from ale.shear_modulus import shear_modulus
from ale.effective_velocity import longitudinal_sound_wave_velocity, transversal_sound_wave_velocity
from ale.cohesive_energy import retrieve_cohesive_energy
from ale.specificHeatCapacity import specificHeatCapacity
from ale.utils import EoSResults

from ase.io import Trajectory

import numpy as np
import os

def run_analysis(options):
    """The function run_analysis takes options as arguments where options are the
    options for analyzing the simulated material. It is specified in config file exactly what
    the user wants to calculate"""

    if not options.get('output'):
        print("Nothing to analyze since output list in config is empty.")
        return

    output_dir = options['out_dir']
    out_file_path = os.path.join(output_dir, options['out_file_name'])

    # Creates or wipes the properties file if the user asks for output.
    if len(options['output']) > 0:
        if os.path.exists(out_file_path):
          f = open(out_file_path, 'r+')
          f.truncate(0) # need '0' when using r+
          f.close()
        else:
          f = open(out_file_path, 'x')
          f.close()

    traj_file_path = os.path.join(output_dir, options['traj_file_name'])
    traj_read = Trajectory(traj_file_path)

    output_properties_to_file(options, traj_read)


def output_properties_to_file(options, traj):
    """ Outputs the chosen properties from a traj file to
        json-file.
    """

    out_file_path = os.path.join(options['out_dir'], options['out_file_name'])
    coh_E_path = os.path.join(options['out_dir'],"_" + options['symbol'] + "_coh_E.traj")

    with open(out_file_path, 'a') as f:
        last_atoms_object = traj[-1] #Take the last atoms object
        first_atoms_object = traj[0] #Take the first atoms object
        eos_results = EoSResults(options)

        # Dictionary which contains a function for each key
        # which can be called to output the data to file.
        # This way the data is accessed only when needed only for those properties
        # that the user chose.
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
            'Debye Temperature' :
                outputGenericResultLazily(
                    f,
                    'Debye Temperature',
                    retrieve_result=lambda: debye_temperature(
                                                first_atoms_object,
                                                options,
                                                eos_results.get_bulk_modulus()
                                            )
                ),
            'Self Diffusion Coefficient' :
                outputGenericResultLazily(
                    f,
                    'Self Diffusion Coefficient',
                    retrieve_result=lambda: self_diffusion_coefficient(traj)
                ),
            'Density' :
                outputGenericResultLazily(
                    f,
                    'Density',
                    retrieve_result=lambda: density(last_atoms_object)
                ),
            'Instant Pressure' :
                outputGenericResultLazily(
                    f,
                    'Instant Pressure',
                    retrieve_result=lambda: pressure(last_atoms_object)
                ),
            'Average Pressure' :
                outputGenericResultLazily(
                    f,
                    'Average Pressure',
                    retrieve_result=lambda: avg_pressure(traj)
                    ),
            'Self Diffusion Coefficient Array' :
                outputGenericResultLazily(
                    f,
                    "Self Diffusion Coefficient Array",
                    retrieve_result=lambda: list(self_diffusion_coefficient_calc(traj)),
                ),
            'MSD' :
                outputGenericResultLazily(
                    f,
                    "MSD",
                    retrieve_result=lambda: list(MSD_data_calc(traj)),
                ),
            'Cohesive Energy' :
                outputGenericResultLazily(
                    f,
                    'Cohesive Energy',
                    retrieve_result=lambda: retrieve_cohesive_energy(coh_E_path)
                ),
            'Lindemann criterion' :
                outputGenericResultLazily(
                    f,
                    'Lindemann criterion',
                    retrieve_result=lambda: lindemann_criterion(traj)
                ),
            'Specific Heat Capacity' :
                outputGenericResultLazily(
                    f,
                    'Specific Heat Capacity',
                    retrieve_result=lambda: specificHeatCapacity(options['ensemble'], traj)
                ),
            'Optimal Lattice Constant' :
                outputGenericResultLazily(
                    f,
                    'Optimal Lattice Constant',
                    retrieve_result=lambda: eos_results.get_optimal_lattice_constant()
                ),
            'Optimal Lattice Volume' :
                outputGenericResultLazily(
                    f,
                    'Optimal Lattice Volume',
                    retrieve_result=lambda: eos_results.get_bulk_optimal_lattice_volume()
                ),
            'Bulk Modulus' :
                outputGenericResultLazily(
                    f,
                    'Bulk Modulus',
                    retrieve_result=lambda: eos_results.get_bulk_modulus(),
                ),
            'Transversal Sound Wave Velocity' :
                outputGenericResultLazily(
                    f,
                    'Transversal Sound Wave Velocity',
                    retrieve_result=lambda: transversal_sound_wave_velocity(last_atoms_object, options)
                ),
            'Longitudinal Sound Wave Velocity' :
                outputGenericResultLazily(
                    f,
                    'Longitudinal Sound Wave Velocity',
                    retrieve_result=lambda: longitudinal_sound_wave_velocity(
                                        last_atoms_object,
                                        options,
                                        eos_results.get_bulk_modulus()
                                    )
                ),
            'Shear Modulus' :
                outputGenericResultLazily(
                    f,
                    'Shear Modulus',
                    retrieve_result=lambda: shear_modulus(options)
                ),
        }

        # Output the data specified in options using the known property outputters
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
    from md_config_reader import parse_config

    from asap3 import Trajectory

    args = parser.parse_args()
    parsed_config_file = parse_config(args.config_file)

    options = parsed_config_file
    options['use_asap'] = args.use_asap

    traj_read = Trajectory(options["symbol"]+".traj")
    run_analysis(options,traj_read)