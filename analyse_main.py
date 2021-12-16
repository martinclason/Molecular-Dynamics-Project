from density import density
from MSD import MSD, self_diffusion_coefficient, lindemann_criterion
from pressure import pressure
from simulationDataIO import outputGenericFromTraj, outputarraytofile, outputSingleProperty, outputGenericResultLazily
from debye_temperature import debye_temperature
from shear_modulus import shear_modulus
from effective_velocity import longitudinal_sound_wave_velocity, transversal_sound_wave_velocity
from cohesive_energy import retrieve_cohesive_energy
from specificHeatCapacity import specificHeatCapacity
from bulk_modulus import calc_lattice_constant

import numpy as np
import os

def analyse_main(options,traj_read):
    """The function analyse_main takes options and a traj_read as arguments where options are the
    options for analysing the simulated material. It is specified in config file exactly what
    the user wants to calculate"""


    # # Output specified data to outfile
    # output_dir = options['out_dir']
    # out_file_path = os.path.join(output_dir, options['out_file_name'])

    if not options.get('output'):
        print("Nothing to analyze since output list in config is empty.")
        return

    output_dir = options['out_dir']
    # Stores the formated output path in the options dictionary
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

    output_properties_to_file(options, traj_read)

class EoSResults:
    """EoSResults stores results from EoS equations lazily. 
    The class can be instantiated without running the costly computation but when
    someone tries to access a value, the computation will be run if it hasn't
    been run yet."""

    def __init__(self, options):
        self.options = options
        self.__optimal_lattice_constant = None
        self.__bulk_modulus = None
        self.__optimal_lattice_volume = None

    def _run_calculations(self):
        a0, B0, v0 = calc_lattice_constant(self.options)
        self.__optimal_lattice_constant = a0
        self.__bulk_modulus = B0
        self.__optimal_lattice_volume = v0

    def get_optimal_lattice_constant(self):
        if not self.__optimal_lattice_constant:
            self._run_calculations()
        return self.__optimal_lattice_constant

    def get_bulk_modulus(self):
        if not self.__bulk_modulus:
            self._run_calculations()
        return self.__bulk_modulus

    def get_bulk_optimal_lattice_volume(self):
        if not self.__optimal_lattice_volume:
            self._run_calculations()
        return self.__optimal_lattice_volume


def output_properties_to_file(options, traj):
    """ Outputs the chosen properties from a traj file to
        json-file.
    """

    out_file_path = os.path.join(options['out_dir'], options['out_file_name'])
    coh_E_path = os.path.join(options['out_dir'],"_coh_E.traj")

    with open(out_file_path, 'a') as f:
        last_atoms_object = traj[-1] #Take the last atoms object
        first_atoms_object = traj[0] #Take the first atoms object
        eos_results = EoSResults(options)
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
                outputSingleProperty(
                    f,
                    'Density',
                    density(last_atoms_object)
                ),
            'Pressure' : #TODO: Should this be tagged 'instant' pressure instead?
                outputSingleProperty(
                    f,
                    'Instant Pressure',
                    pressure(last_atoms_object)
                ),
            'Self Diffusion Coefficient Array' :
                outputarraytofile("Self Diffusion Coefficient Array",self_diffusion_coefficient_calc(traj),f),
            'MSD' :
                outputarraytofile("MSD",MSD_data_calc(traj),f),
            'Cohesive Energy' :
                outputSingleProperty(
                    f,
                    'Cohesive Energy',
                    retrieve_cohesive_energy(coh_E_path)
                ),
            'Lindemann criterion' :
                outputSingleProperty(
                    f,
                    'Lindemann criterion',
                    lindemann_criterion(traj)
                ),
            'Specific Heat Capacity' :
                outputSingleProperty(
                    f,
                    'Specific Heat Capacity',
                    specificHeatCapacity(options['ensemble'],traj)
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
