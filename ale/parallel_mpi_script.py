from mpi4py import MPI
from itertools import accumulate as acc
import pickle
import pprint
import os

from ale.simulate import run_simulation
from ale.analyze import run_analysis

# TODO: Should this use asap3?
from asap3 import Trajectory

def do_work(options):
    """The work that one process should do, i.e. simulate and analyze with its assigned options.
    If the process has many simulations to perform it will call this function many times in sequence.

    If an issue arises it will catch those exceptions and continue with the next computation.
    """
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
    run_simulation(options)

def analyze(options):
    print(f"process {rank} writes output to: {options['out_dir']}/{options['out_file_name']}")
    run_analysis(options)

def get_symbol(options):
    return options['symbol']


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # The rank 0 process unpickles to options list from file and handles
        # the distribution of work to all processes. It calculates start and stop indices
        # for each process that they use to index the options list

        print(f"Number of processes: {size}")

        # parser = argparse.ArgumentParser()
        # parser.add_argument("options_pickle_file_path")
        # parser.parse_args()
        #options_pickle_file_path = parser.options_pickle_file_path

        # TODO: Hard coded string representing file name of pickle file,
        # should probably be implemented in a safer way.
        # Maybe pass as command line argument?
        options_pickle_file_path = 'options_pickle'

        with open(options_pickle_file_path, 'rb') as f:
            options_list = pickle.load(f)

        print(f"Number of options: {len(options_list)}")
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(options_list)

        n_options = len(options_list)
        q, r = divmod(n_options, size)

        # the amount of simulations each process has to run
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

    # Distribute needed data to all processes
    start = comm.scatter(starts, root=0)
    stop = comm.scatter(stops, root=0)
    # Every thread gets access to the whole options list
    options_list = comm.bcast(options_list, root=0)

    # Only do work if this process has work to do in options list
    if rank < len(options_list):
        print(f"\n\n\nProcess: {rank}, start: {start}, stop: {stop}\n\n\n")
        for options in options_list[start:stop]:
            print(f"rank: {rank}, option: {get_symbol(options)}")
            traj_path = os.path.join(options['out_dir'], options['traj_file_name'])
            print(f"rank: {rank}, traj_path before work: {traj_path}")
            do_work(options)
            print(f"process {rank} done with work")
            print(f"rank: {rank}, traj_path after work: {traj_path}")
    else:
        print(f"\n\n\nprocess {rank} did no work\n\n\n")

    print(f"process {rank} all done")
