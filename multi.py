from itertools import product
import os
import pickle
from subprocess import Popen
from copy import deepcopy
from md_config_reader import config_parser as config_file_parser
import pprint

def get_combinations_of_elements(elements):
    """Creates combination of the given elements.
    E.g.
    [[Na,Ca],[Cl]] gives ((Na,Cl), (Ca,Cl))
    """
    # Create (cartesian product) combinations of all given elements
    return product(*elements)


def generate_options_list(multi_config, options):
    elements = multi_config['elements']
    output_dir = options['out_dir']
    assert os.path.isdir(output_dir), f"There seems to be no output directory: {output_dir}"

    element_combinations = product(*elements)

    print("Combinations:")
    print(element_combinations)

    options_list = [options_from_element_combination(element_combination, multi_config, options, output_dir) 
                        for element_combination in element_combinations]

    return options_list

def multi(multi_config, options, simulate, analyze):
    options_list = generate_options_list(multi_config, options)

    run_in_parallell(options_list)

def options_from_element_combination(element_combination, multi_config, template_options, output_dir):
    options = deepcopy(template_options)

    # TODO: Fix for multiple elements aswell
    element = element_combination[0]
    element_combination_serialized = element_combination[0]

    # Prepare options
    options['symbol'] = element

    # Set potential if specified for this element combination
    if potentials_spec := multi_config.get('potentials'):
        if specified_pot := get_spec_potential_for_element(potentials_spec, element):
            print(f"Using specified potential {specified_pot} for: {element}")
            options['potential'] = specified_pot
        elif default_pot := potentials_spec.get('default'):
            print(f"Using default potential {default_pot} for: {element}")
            options['potential'] = default_pot
        else:
            print(f"No specific potential for: {element} was specified. Will try to use potential specified in config file instead.")

    print(f"\n\nSetting up properties for {element_combination_serialized}:\n\n")

    # maps into options object
    map_to_each_element_combination = {
        'cells': 'cell',
        'scaled_positions': 'scaled_positions'
    }

    for (known_key, target_prop) in map_to_each_element_combination.items():
        if known_key in multi_config:
            # dict comprehension only keeping entries matching this element combination
            element_combination_maps_for_prop = {
                    k:v for d in multi_config[known_key]
                    for k,v in d.items()
            }
            print("element_combination_maps_for_prop")
            print(element_combination_maps_for_prop)

            prop_map_for_this_element_combination = {
                k:v for k,v in element_combination_maps_for_prop.items() 
                    if k == element_combination_serialized
            }
            print("prop_map_for_this_element_combination")
            print(prop_map_for_this_element_combination)

            for specified_element, new_value in prop_map_for_this_element_combination.items():
                print(f"Should configure {target_prop} for {element_combination_serialized} with {new_value}")
                options[target_prop] = new_value
            if len(prop_map_for_this_element_combination.items()) == 0:
            #else:
                print(f"no map for {target_prop} for {element_combination_serialized}")
                print(len(prop_map_for_this_element_combination.items()))
                print("was:")
                print(prop_map_for_this_element_combination.items())
                if 'default' in element_combination_maps_for_prop:
                    default_value = element_combination_maps_for_prop['default']
                    print(f"Setting default for {target_prop} for {element_combination_serialized} with default value {default_value}\n\n")
                    options[target_prop] = default_value
                

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

if __name__=="__main__":
    print("testing options list generation from multi config file")

    multi_config_file = 'm_config.yaml'
    config_file = 'config.yaml'

    print(f"using multi_config_file: {multi_config_file}")
    print(f"using config_file: {config_file}")

    with open(multi_config_file, 'r') as f:
        multi_config = config_file_parser(f)

    with open(config_file, 'r') as f:
        options = config_file_parser(f)
    
    # mock options
    options['out_dir'] = 'out'

    options_list = generate_options_list(multi_config, options)

    pp = pprint.PrettyPrinter(indent=4)

    should_print = True
    if should_print:
        for options in options_list:
            print("\n\n")
            print(f"{options['symbol']}:")
            pp.pprint(options)
            print("\n\n")

