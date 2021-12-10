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

        # Hard code potential to default LJ for now
        options['openKIMid'] = "LJ_ElliottAkerson_2015_Universal__MO_959249795837_003"

        # Setup traj file
        traj_file_name = os.path.join(output_dir, f"{element}.traj")
        options['traj_file_name'] = traj_file_name

        simulate(options)

        # Setup out file
        options['out_file_name'] = os.path.join(output_dir, f"{element}_out.json")

        analyze(options)
