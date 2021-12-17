from itertools import product
import os
import pickle
from subprocess import Popen
from copy import deepcopy

def get_combinations_of_elements(elements):
    """Creates combination of the given elements.
    E.g.
    [[Na,Ca],[Cl]] gives ((Na,Cl), (Ca,Cl))
    """
    # Create (cartesian product) combinations of all given elements
    return product(*elements)


def multi(multi_config, options, simulate, analyze):
    elements = multi_config['elements']
    output_dir = options['out_dir']
    assert os.path.isdir(output_dir), f"There seems to be no output directory: {output_dir}"

    element_combinations = product(*elements)

    print("Combinations:")
    print(element_combinations)

    options_list = [options_from_element_combination(element_combination, multi_config, options, output_dir) 
                        for element_combination in element_combinations]

    run_in_parallell(options_list)

def options_from_element_combination(element_combination, multi_config, template_options, output_dir):
    options = deepcopy(template_options)

    # TODO: Fix for multiple elements aswell
    element = element_combination[0]

    # Prepare options
    options['symbol'] = element_combination_serialized

    print(f"\nSetting up properties for {element_combination_serialized}:")

    # maps into options object if present in multi_config
    map_to_each_element_combination = {
        'potentials': 'potential',
        'cells': 'cell',
        'scaled_positions': 'scaled_positions',
        'latticeconstants': 'latticeconstant',
        'temperatures': 'temperature_K'
    }

    for (known_key, target_prop) in map_to_each_element_combination.items():
        if known_key in multi_config:
            # dict comprehension to flatten lists of dicts to one dict
            element_combination_maps_for_prop = multi_config[known_key]
            # Only keeping entries matching this element combination
            prop_map_for_this_element_combination = {
                k:v for k,v in element_combination_maps_for_prop.items() 
                    if k == element_combination_serialized
            }
            for specified_element, new_value in prop_map_for_this_element_combination.items():
                print(f"{element_combination_serialized} using specified {target_prop}: {new_value}")
                options[target_prop] = new_value
            if len(prop_map_for_this_element_combination.items()) == 0:
                if 'default' in element_combination_maps_for_prop:
                    default_value = element_combination_maps_for_prop['default']
                    print(f"{element_combination_serialized} using default {target_prop}: {default_value}")
                    options[target_prop] = default_value
                else:
                    print(f"No specific {target_prop} for {element_combination_serialized} was specified. Will try to use {target_prop}: {options.get(target_prop)} specified in config file instead.")
                

    # Setup traj file
    traj_file_name = f"{element}.traj"
    options['traj_file_name'] = traj_file_name
    options['out_dir'] = output_dir

    # Setup out file for analysis
    options['out_file_name'] = f"{element}_out.json"
    return options


def get_spec_potential_for_element(potentials_spec, element):
    if element in potentials_spec:
        return potentials_spec[element]
    return None


def run_in_parallell(options_list):
    # pickle options_list to file
    pickle_file_path = 'options_pickle'
    with open(pickle_file_path, 'wb+') as f:
        pickle.dump(options_list, f)

    # start mpi process
    print("Calling mpirun...")
    parallel_mpi_script = 'parallel_mpi_script.py'
    n_options = len(options_list)
    # arguments = ['mpirun', '-n', f'{n_options}', 'python3', parallel_mpi_script]
    arguments = ['mpirun', 'python3', parallel_mpi_script]
    print(f"Will call mpirun with arguments: {arguments}")
    process = Popen(arguments)#, pickle_file_path])
    print(f"Waiting for process to finish...")
    process.wait()
    print(f"Process finished!")


