from ale.md_config_reader import parse_config

from itertools import product
import os
import pickle
from subprocess import Popen
from copy import deepcopy
import pprint


def get_combinations_of_elements(elements):
    """Creates combination of the given elements.
    E.g.
    [[Na,Ca],[Cl]] gives ((Na,Cl), (Ca,Cl))
    """
    # Create (cartesian product) combinations of all given elements
    return product(*elements)


def generate_options_list(multi_config, options):
    """This function generates a list of options objects derived from
    the multi config and the options object. It uses the options object as
    a template and replaces certain properties in the options object.

    This way many new options objects are generated which can vary certain
    properties.
    """

    elements = multi_config['elements']
    output_dir = options['out_dir']
    assert os.path.isdir(
        output_dir), f"There seems to be no output directory: {output_dir}"

    # create a list of element combinations.
    # An element combination is a tuple of elements, e.g. ("Na","Cl")
    # which together might form a material to simulate.
    element_combinations = get_combinations_of_elements(elements)

    print("Combinations:")
    print(element_combinations)

    options_list = [options_from_element_combination(element_combination, multi_config, options)
                    for element_combination in element_combinations]

    return options_list


def multi(multi_config, options):
    """This function runs many simulations and analyses in parallel on different processes.
    It takes a multi_config object which specifies how to generate configurations for each
    simulation to run.

    :param multi_config: object specifying how to generate many simulations.
    :param options: template options object to start from when generating new options.
    """
    options_list = generate_options_list(multi_config, options)

    run_in_parallell(options_list)


def serialize_element_combination(element_combination):
    """This function is used to create a string representation from
    an element combination which is a tuple of strings.
    This new representation could be used as keys in dictionaries.

    This is also later passed as the symbol parameter to ase when creating an atoms object.

    :param element_combination: arbitrary length tuple of strings which represents a material.
    """
    return "".join(element_combination)


def options_from_element_combination(element_combination, multi_config, template_options):
    """This function returns a new options object for a certain element combination.
    It uses the element combination and the multi config to derive what other properties to update.

    :param element_combination: tuple representing the material to generate options object for.
    :param multi_config: object containing configurations for how to vary this options object.
    :param template_options: options object to start from when creating the new options object for this element combination.
    """

    # create deep copy of the template to avoid modifying same objects
    options = deepcopy(template_options)

    element_combination_serialized = serialize_element_combination(
        element_combination)

    # Prepare options
    options['symbol'] = element_combination_serialized

    print(f"\nSetting up properties for {element_combination_serialized}:")

    # maps into options object if present in multi_config
    # This dict specifies what keys from the multi config should map to in
    # the generated options object. More mappings can be mapped here and the
    # rest of the code should automatically take care of updating the options
    # object for these properties if present in the multi config.
    map_to_each_element_combination = {
        'potentials': 'potential',
        'cells': 'cell',
        'scaled_positions': 'scaled_positions',
        'latticeconstants': 'latticeconstant',
        'temperatures': 'temperature_K',
    }

    def update_options_for_property_if_needed_for_element_combination(
        options,
        property_map_for_element_combinations,
        target_prop,
        element_key,
    ):
        """This function updates options for a specific property using a map
        mapping element combinations to values for this property. This is done
        for a specific element which has a key that could be present in the mapping.

        If the element key is present in this map that value is set in options.
        If it isn't but the key 'default' is present with a value, that value is set instead.
        Otherwise the options is left as is for this property

        :param options: inout object specifying options for a simulation run.
        :param property_map_for_element_combinations: maps element to value for some property
        :param target_prop: what property in options to potentially modify if needed.
        :param element_key: the element for which to look for mappings in property_map_for_element_combinations.
        """
        # dict comprehension to flatten lists of dicts to one dict
        # Only keeping entries matching this element_key
        prop_map_for_this_element_combination = {
            k: v for k, v in property_map_for_element_combinations.items()
            if k == element_key
        }
        # TODO: Maybe do without the for loop and check that dict only contains one mapping for this element
        for specified_element, new_value in prop_map_for_this_element_combination.items():
            print(f"{element_key} using specified {target_prop}: {new_value}")
            options[target_prop] = new_value
        # check if the element wasn't present in the given map
        if len(prop_map_for_this_element_combination.items()) == 0:
            if 'default' in property_map_for_element_combinations:
                default_value = property_map_for_element_combinations['default']
                print(f"{element_key} using default {target_prop}: {default_value}")
                options[target_prop] = default_value
            else:
                print(
                    f"No specific {target_prop} for {element_key} was specified.")
                print(
                    f"Will try to use {target_prop}: {options.get(target_prop)} specified in config file instead.")

    # Update properties in the options object using the multi config
    # E.g. if the element combination is Au and there exists a mapping
    # Au: 4.19 under latticeconstants in multi config it will update
    # the latticeconstant in the options object to match this.
    # If there exists a default: 3.71 mapping and no specific mapping for
    # Au it will update options with this value.
    # Otherwise it will leave this property as is.
    for (known_key, target_prop) in map_to_each_element_combination.items():
        if known_key in multi_config:
            update_options_for_property_if_needed_for_element_combination(
                options=options,
                property_map_for_element_combinations=multi_config[known_key],
                target_prop=target_prop,
                element_key=element_combination_serialized,
            )

    # Setup traj file
    traj_file_name = f"{element_combination_serialized}.traj"
    options['traj_file_name'] = traj_file_name

    # Setup out file for analysis
    options['out_file_name'] = f"{element_combination_serialized}_out.json"
    return options


def run_in_parallell(options_list):
    """This function pickles the options list to file and
    starts multiple processes using openmpi to run simulations
    for each options object in the list.

    The pickle file is hardcoded to be named 'options_pickle'
    and the script it calls for the multiprocessing is hardcoded
    to have the path 'ale/parallel_mpi_script.py'.

    The function waits until all processes are finished before it returns.
    """

    # pickle options_list to file
    pickle_file_path = 'options_pickle'
    with open(pickle_file_path, 'wb+') as f:
        pickle.dump(options_list, f)

    # start mpi process
    print("Calling mpirun...")
    parallel_mpi_script = 'ale/parallel_mpi_script.py'
    n_options = len(options_list)
    arguments = ['mpirun', 'python3', parallel_mpi_script]
    print(f"Will call mpirun with arguments: {arguments}")
    process = Popen(arguments)  # , pickle_file_path])
    print(f"Waiting for process to finish...")
    process.wait()
    print(f"Process finished!")


if __name__ == "__main__":
    print("testing options list generation from multi config file")

    multi_config_file = 'm_config.yaml'
    config_file = 'config.yaml'

    print(f"using multi_config_file: {multi_config_file}")
    print(f"using config_file: {config_file}")

    with open(multi_config_file, 'r') as f:
        multi_config = parse_config(f)

    with open(config_file, 'r') as f:
        options = parse_config(f)

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
