from ale.command_line_arg_parser import CreateParser
from ale.md_config_reader import config_parser as config_file_parser
from ale.simulate import main
from ale.analyse_main import analyse_main
from ale.visualize_main import visualize as visualize_simulation
import os
from ale.multi import multi as multi_main

from asap3 import Trajectory

import pprint
"""There is a parser for passing flags from the command line to the MD which enables
or disables the use of asap on the current run with the flags '--asap' for enable-
ing it and '--no-asap' to disable it.

Passing this flag is to avoid getting the error 'illegal instruction (core dumped)'
in the terminal since some machines cannot run the current version of ASAP which
is used in this project. """

pp = pprint.PrettyPrinter(indent=4)

def default(options, args=None):
  print("Running default")
  simulate(options)
  analyze(options)

def multi(options, args):
  print("Should run multiple simulations and analyzations parallelized on multiple cores")

  multi_config_file = args.multi_config_file
  print(f"multi_config_file: {multi_config_file}")
  multi_config = config_file_parser(multi_config_file)

  output_dir = args.out_dir
  options['out_dir'] = output_dir

  # Run simulate and analyze distributed
  multi_main(multi_config, options, simulate=simulate, analyze=analyze)
  print("exiting multi run")

def simulate(options, args=None):
  print(f'Use asap: {options["use_asap"]}')
  print("Using traj:", options['traj_file_name'])
  main(options)

def analyze(options, args=None):
  output_dir = options['out_dir']
  traj_file_path = os.path.join(output_dir, options['traj_file_name'])
  traj_read = Trajectory(traj_file_path)
  analyse_main(options,traj_read)

def visualize(options, args=None):
  # pp.pprint(options)
  output_dir = options['out_dir']
  out_file_path = os.path.join(output_dir, options['out_file_name'])

  if args.scatter_dir:
    options['scatter_dir'] = args.scatter_dir

  visualize_simulation(options, out_file_path)

def run(arguments=None):
  parser = CreateParser(
                default=default,
                multi=multi,
                simulate=simulate,
                analyze=analyze,
                visualize=visualize,
           )

  if arguments:
    args = parser.parse_args(arguments.split(" "))
  else:
    args = parser.parse_args()

  parsed_config_file = config_file_parser(args.config_file)

  options = parsed_config_file
  options['use_asap'] = args.use_asap
  if args.traj_file_name:
    print("Using supplied traj_file")
    options['traj_file_name'] = args.traj_file_name
  else:
    # default to <symbol>.traj
    options['traj_file_name'] = f"{options['symbol']}.traj"
  print(options)

  # Sets the file name of the properties file.
  if args.out_file_name:
    options['out_file_name'] = args.out_file_name
  else:
    # Defaults to <symbol>.json if not provided in the command line.
    options['out_file_name'] = options.get("out_file_name", f"{options['symbol']}.json")

  # Sets the output directory of the properties file.
  if args.out_dir:
    output_dir = args.out_dir
    options['out_dir'] = output_dir
  else:
    # Defaults to current working directory
    options['out_dir'] = options.get('out_dir', os.getcwd())

  args.sub_command(options, args)

if __name__=="__main__":
  run()
  # Use this to run some specific command with args when debugging
  #run("multi m_config.yaml out")
