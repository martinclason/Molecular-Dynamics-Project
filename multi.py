from itertools import product
import os

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

    for element_combination in element_combinations:
        print("Should run simulation with: ", end="")
        print(element_combination)

        # TODO: Fix for multiple elements aswell
        element = element_combination[0]

        # Prepare options
        options['symbol'] = element

        # Set potential if specified for this element combination
        if potentials_spec := multi_config.get('potentials'):
            if specified_pot := get_spec_potential_for_element(potentials_spec, element):
                print(f"Using specified potential {specified_pot} for: {element}")
                options['potential'] = specified_pot
            elif default_pot := potentials_spec.get('default'):
                print(f"Using default potential {default_pot} for: {element}")
            else:
                print(f"No specific potential for: {element} was specified. Will try to use potential specified in config file instead.")

        # Setup traj file
        traj_file_name = f"{element}.traj"
        options['traj_file_name'] = traj_file_name
        options['out_dir'] = output_dir

        simulate(options)

        # Setup out file
        options['out_file_name'] = f"{element}_out.json"

        analyze(options)

def get_spec_potential_for_element(potentials_spec, element):
    if element in potentials_spec:
        return potentials_spec[element]
    return None
