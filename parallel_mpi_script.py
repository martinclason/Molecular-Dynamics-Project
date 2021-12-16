from mpi4py import MPI
from itertools import accumulate as acc
import pickle
import argparse
import pprint
import os

from main import main as simulate_main
from analyse_main import analyse_main as analyze_main

# TODO: Should this use asap3?
from asap3 import Trajectory

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def do_work(options):
    print(f"process {rank} will write to traj: {options['out_dir']}/{options['traj_file_name']}")
    try:
        simulate(options)
    except Exception as e:
        print(f"Something went wrong when simulating {options['symbol']} in process {rank}")
        print(f"---- error: {e}")

    try:
        print(f"process {rank} done with simulation")
        print(f"process {rank} starts analysis: {options['out_dir']}/{options['traj_file_name']}")
        analyze(options)
    except Exception as e:
        print(f"Something went wrong when analyzing {options['symbol']} in process {rank}")
        print(f"---- error: {e}")

def simulate(options):
    simulate_main(options)

def analyze(options):
    print(f"process {rank} writes output to: {options['out_dir']}/{options['out_file_name']}")
    traj_read_path = os.path.join(options['out_dir'], options['traj_file_name'])
    traj_read = Trajectory(traj_read_path)
    analyze_main(options, traj_read)

if rank == 0:
    print(f"Number of processes: {size}")

    # parser = argparse.ArgumentParser()
    # parser.add_argument("options_pickle_file_path")
    # parser.parse_args()
    #options_pickle_file_path = parser.options_pickle_file_path
    options_pickle_file_path = 'options_pickle'

    with open(options_pickle_file_path, 'rb') as f:
        options_list = pickle.load(f)

    print(f"Number of options: {len(options_list)}")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(options_list)

    n_options = len(options_list)
    q, r = divmod(n_options, size)

    lengths = [q + 1 if i < r else q for i in range(size)]

    # create lists with start index and stop index for each process
    starts, stops = zip(*[(start, stop) for (start, stop) in
                          zip(acc([0] + lengths), acc(lengths))])

    print(starts)
    print(stops)

else:
    starts = None
    stops = None
    options_list = None

def get_symbol(options):
    return options['symbol']

start = comm.scatter(starts, root=0)
stop = comm.scatter(stops, root=0)
options_list = comm.bcast(options_list, root=0)

if rank < len(options_list):
    print(f"\n\n\nProcess: {rank}, start: {start}, stop: {stop}\n\n\n")
    # if rank == 1:
    #     assert False
    # for i in range(start, stop):
    for options in options_list[start:stop]:
        print(f"rank: {rank}, option: {get_symbol(options)}")
        traj_path = os.path.join(options['out_dir'], options['traj_file_name'])
        # open(traj_path, 'w').close()
        print(f"rank: {rank}, traj_path before work: {traj_path}")
        do_work(options)
        print(f"process {rank} done with work")
        print(f"rank: {rank}, traj_path after work: {traj_path}")

        # try:
        #     assert os.path.isfile(traj_path), f"Didn't exist: {traj_path}"
        # except AssertionError:
        #     comm.Barrier()
        #     raise Exception(f"File {traj_path} didn't exist, ending this process with rank: {rank}")
else:
    print(f"\n\n\nprocess {rank} did no work\n\n\n")

print(f"process {rank} all done")
