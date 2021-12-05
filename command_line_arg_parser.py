import argparse

# Adds parser so user can choose if to use asap or not with flags from terminal

class CreateParser():
    def __init__(self, default, subcommands):
        description = "A program to run molecular dynamics calculations."
        self.parser = argparse.ArgumentParser(description=description)
        self.subparsers = self.parser.add_subparsers()

        self.parser.add_argument('--asap', dest='use_asap', action='store_true')
        self.parser.add_argument('--no-asap', dest='use_asap', action='store_false')
        self.parser.set_defaults(use_asap=True)

        self.parser.add_argument(
                          '-c',
                          '--config',
                          nargs='?',
                          type=argparse.FileType('r'),
                          dest='config_file',
                          default='./config.yaml')

        # traj file name passed as str since it is possible
        # the file hasn't been created yet when calling ale -t Cu.traj
        # since it is created when simulate is run.
        self.parser.add_argument(
                          '-t',
                          '--traj',
                          nargs='?',
                          type=str,
                          dest='traj_file_name',
                          default=None)

        self.parser.add_argument(
                          '-o',
                          '--out',
                          nargs='?',
                          type=str,
                          dest='out_file_name',
                          default='out.json',
                          help='where to output the analysis data (default: out.json)',
                          metavar='output_file')

        self.parser.set_defaults(sub_command=default)

        for command in subcommands:
            cmd = self.subparsers.add_parser(command)
            cmd.set_defaults(sub_command=subcommands[command])

    def parse_args(self, args=None):
        if args:
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
parser = CreateParser(nop, {})
