import argparse
from argparse import RawTextHelpFormatter


class CreateParser():
    """Class thar parses the command line arguments  given to ale.
    It handles sub commands that corresponds to different sub domains of the
    ale software. This is realized with subparsers for each sub command.

    :param default: function to call when no subcommand is specified.
    :type default: lambda or function.

    :param multi: function to call when multi subcommand is specified.
    :type multi: lambda or function.

    :param simulate: function to call when simulate subcommand is specified.
    :type simulate: lambda or function.

    :param analyze: function to call when analyze subcommand is specified.
    :type analyze: lambda or function.

    :param visualize: function to call when visualize subcommand is specified.
    :type visualize: lambda or function.
    """

    def __init__(self, default, multi, simulate, analyze, visualize):
        """Creates parser object.
        """
        description = "A program to run molecular dynamics calculations."
        self.parser = argparse.ArgumentParser(description=description, formatter_class=RawTextHelpFormatter)
        self.subparsers = self.parser.add_subparsers()

        # Adds parser so user can choose if to use asap or not with flags from terminal
        self.parser.add_argument(
                          '--asap',
                          dest='use_asap',
                          action='store_true',
                          help="use asap to greatly accelerate calculations (this is default)")
        self.parser.add_argument(
                          '--no-asap',
                          dest='use_asap',
                          action='store_false',
                          help="don't use asap to accelerate calculations (useful if asap isn't available)")
        self.parser.set_defaults(use_asap=True)

        self.parser.add_argument(
                          '-c',
                          '--config',
                          nargs='?',
                          type=argparse.FileType('r'),
                          dest='config_file',
                          default='./config.yaml',
                          help='where to read the configuration for the calculations (default: config.yaml)',
                          metavar='config_file')

        # traj file name passed as str since it is possible
        # the file hasn't been created yet when calling ale -t Cu.traj
        # since it is created when simulate is run.
        self.parser.add_argument(
                          '-t',
                          '--traj',
                          nargs='?',
                          type=str,
                          dest='traj_file_name',
                          default=None,
                          help="""where to output the simulated trajectory data (default: <Symbol>.traj)
The .traj-format is a binary format used by the ase library and contains
data about the atoms for time steps in the simulation.
                          """,
                          metavar='traj_file')

        self.parser.add_argument(
                          '-o',
                          '--out',
                          nargs='?',
                          type=str,
                          dest='out_file_name',
                          default=None,
                          help='where to output the analysis data (default: <symbol>.json)',
                          metavar='output_file')

        self.parser.add_argument(
                          '-d',
                          '--dir',
                          nargs='?',
                          type=str,
                          dest='out_dir',
                          default=None,
                          help='relative path to where simulation output files should be written.',
                          metavar='out_dir')

        self.parser.set_defaults(sub_command=default)


        # multi
        multi_parser = self.subparsers.add_parser('multi')
        multi_parser.set_defaults(sub_command=multi)
        multi_parser.add_argument(
                    type=argparse.FileType('r'),
                    dest='multi_config_file',
                    help='config for how a collection of simulations should be run and what to vary.',
                    metavar='multi_config_file',
              )
        multi_parser.add_argument(
                    dest='out_dir',
                    help='relative path to where simulation output files should be written.',
                    metavar='out_dir',
          )

        # simulate
        simulate_parser = self.subparsers.add_parser('simulate')
        simulate_parser.set_defaults(sub_command=simulate)

        # analyze
        analyze_parser = self.subparsers.add_parser('analyze')
        analyze_parser.set_defaults(sub_command=analyze)

        # visualize
        visualize_parser = self.subparsers.add_parser('visualize')
        visualize_parser.set_defaults(sub_command=visualize)
        visualize_parser.add_argument(
                    '-s',
                    '--scatter-dir',
                    nargs='?',
                    type=str,
                    dest='scatter_dir',
                    help='where to look for json data for scatter plots',
                    metavar='scatter_dir',
              )

    def parse_args(self, args=None):
        """This function runs the parser. If no arguments to parse are
        specified it reads the arguments from the command line.

        :param args: args to parse
        :type args: list
        """

        if args is not None:
            # Handle if caller passes explicit args list
            parsed_args = self.parser.parse_known_args(args)
            parsed_args = self.parser.parse_args(parsed_args[1], parsed_args[0])
            return parsed_args
        else:
            # multipass strategy: 
            # https://stackoverflow.com/questions/46962065/add-top-level-argparse-arguments-after-subparser-args
            args = self.parser.parse_known_args()
            args = self.parser.parse_args(args[1], args[0])
            return args


nop = lambda: None
parser = CreateParser(nop, nop, nop, nop, nop)
