import argparse

# Adds parser so user can choose if to use asap or not with flags from terminal

class CreateParser():
    def __init__(self, default, simulate, analyze, visualize):
        self.parser = argparse.ArgumentParser()
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

        self.parser.set_defaults(sub_command=default)

        parser_simulate = self.subparsers.add_parser('simulate')
        parser_simulate.set_defaults(sub_command=simulate)

        parser_analyze = self.subparsers.add_parser('analyze')
        parser_analyze.set_defaults(sub_command=analyze)

        parser_visualize = self.subparsers.add_parser('visualize')
        parser_visualize.set_defaults(sub_command=visualize)

    def parse_args(self):
        # multipass strategy: 
        # https://stackoverflow.com/questions/46962065/add-top-level-argparse-arguments-after-subparser-args
        args = self.parser.parse_known_args()
        print('pass 1: ', args)
        args = self.parser.parse_args(args[1], args[0])
        print('pass 2:', args)
        return args
