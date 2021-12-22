from ale.command_line_arg_parser import CreateParser
from ale.md_config_reader import parse_config
from ale.simulate import run_simulation
from ale.analyze import run_analysis
from ale.visualize_main import visualize as visualize_simulation
from ale.multi import multi as multi_main
from asap3 import Trajectory
import os
import pprint
import logging

"""This file is the entry point for the CLI interface and
calls all other parts of the ale software.
"""

pp = pprint.PrettyPrinter(indent=4)


def default(options, args=None):
    """This function is run when no subcommand is passed to ale, e.g. 'ale -c my_config.yaml'
    It will run simulation followed by analysis.
    """
    print("Running default, i.e. simulation followed by analysis...")
    simulate(options)
    analyze(options)


def multi(options, args):
    """This function runs multiple simulations and analyzations in parallel on multiple cores.
    For this it needs a multi-config-file and a directory where to store the resulting files.
    """
    print("Should run multiple simulations and analyzations parallelized on multiple cores...")

    multi_config_file = args.multi_config_file
    multi_config = parse_config(multi_config_file)
    logging.debug(f"Using multi config: {multi_config_file}")

    # Run simulate and analyze distributed on many processes
    multi_main(multi_config, options)

    print("exiting multi run")


def simulate(options, args=None):
    """This function runs a molecular dynamics simulation using the options specified in an options object.
    """
    run_simulation(options)


def analyze(options, args=None):
    """This function runs analysis on simulation data. What analysis and what to
    output is specified in the options object.
    """
    run_analysis(options)


def visualize(options, args=None):
    out_file_path = os.path.join(options['out_dir'], options['out_file_name'])

    if args.scatter_dir:
        options['scatter_dir'] = args.scatter_dir

    visualize_simulation(options, out_file_path)


def run(arguments=None):
    """This function is the main entrypoint for ale. It takes an optional argument which
    if passed makes the parser read those arguments instead of argv from the command line.

    This function parses the contents of the given config file and passes these options
    to the functions which actually do calculations or visualizations.

    The argument parser takes a flag which enables
    or disables the use of asap on the current run with the flags '--asap' for
    enabling it and '--no-asap' to disable it.

    Passing this flag is to avoid getting the error 'illegal instruction (core dumped)'
    in the terminal since some machines cannot run the current version of ASAP which
    is used in this project. """

    # Create command line parser with callbacks for the respective subcommands
    parser = CreateParser(
        default=default,
        multi=multi,
        simulate=simulate,
        analyze=analyze,
        visualize=visualize,
    )

    if arguments:
        # parse arguments from the arguments parameter
        args = parser.parse_args(arguments.split(" "))
    else:
        # parse arguments from argv from command line
        args = parser.parse_args()

    parsed_config_file = parse_config(args.config_file)
    options = parsed_config_file

    options['use_asap'] = args.use_asap

    # Set traj_file_name to that given in command line, or config, or default
    if args.traj_file_name:
        options['traj_file_name'] = args.traj_file_name
    else:
        # default to <symbol>.traj
        default_traj_file_name = f"{options['symbol']}.traj"
        options['traj_file_name'] = default_traj_file_name

    print("Given configuration:")
    pp.pprint(options)
    print()

    # Sets the file name of the output file.
    if args.out_file_name:
        options['out_file_name'] = args.out_file_name
    else:
        # Defaults to <symbol>.json if not provided in the command line.
        default_out_file_name = f"{options['symbol']}_out.json"
        options['out_file_name'] = options.get("out_file_name", default_out_file_name)

    # Sets the output directory of the output file.
    if args.out_dir:
        output_dir = args.out_dir
        options['out_dir'] = output_dir
    else:
        # Defaults to current working directory if not present in options
        options['out_dir'] = options.get('out_dir', os.getcwd())

    # Executes the given subcommand, defaults to calling default
    args.sub_command(options, args)


if __name__ == "__main__":
    run()
    # Use this to run some specific command with args when debugging
    #run("multi m_config.yaml out")
