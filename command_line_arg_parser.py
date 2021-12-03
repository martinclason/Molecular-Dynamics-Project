import argparse

# Adds parser so user can choose if to use asap or not with flags from terminal

def CreateParser(default, simulate, analyze, visualize):
  
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  parser.add_argument('--asap', dest='use_asap', action='store_true')
  parser.add_argument('--no-asap', dest='use_asap', action='store_false')
  parser.set_defaults(use_asap=True)

  parser.add_argument('config_file',
                      nargs='?',
                      type=argparse.FileType('r'),
                      default='./config.yaml')

  parser.set_defaults(sub_command=default)

  parser_simulate = subparsers.add_parser('simulate')
  parser_simulate.set_defaults(sub_command=simulate)

  parser_analyze = subparsers.add_parser('analyze')
  parser_analyze.set_defaults(sub_command=analyze)

  parser_visualize = subparsers.add_parser('visualize')
  parser_visualize.set_defaults(sub_command=visualize)

  return parser
