from mpi4py import MPI
from itertools import accumulate as acc
import pickle

pickle_file_name = 'options_pickle'

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    print(f"Number of processes: {size}")
    comm.bcast

    # options = list(range(10))

    with open(pickle_file_name, 'rb') as f:
        options = pickle.load(f)

    print(f"Number of options: {len(options)}")

    n_options = len(options)
    q, r = divmod(n_options, size)

    lengths = [q + 1 if i < r else q for i in range(size)]

    # create lists with start index and stop index for each process
    starts, stops = zip(*[(start, stop - 1) for (start, stop) in
                          zip(acc([0] + lengths), acc(lengths))])

    print(starts)
    print(stops)

else:
    starts = None
    stops = None
    options = None

def get_symbol(options):
    return options['symbol']

start = comm.scatter(starts, root=0)
stop = comm.scatter(stops, root=0)
options = comm.bcast(options, root=0)

if rank < len(options):
    print(f"rank: {rank}, start: {start}, stop: {stop}")
    for i in range(start, stop + 1):
        print(f"rank: {rank}, option: {get_symbol(options[i])}")
else:
    print(f"process {rank} did no work")

