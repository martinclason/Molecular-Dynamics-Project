from pickle_options import pickle_options
from subprocess import Popen, PIPE
import os
import pytest


# TODO: Add tests

@pytest.mark.skip
def test_parallel_proof_of_concept():
    pickle_options()

    parallel_script = 'parallel_execution_trial.py'

    assert os.path.isfile('options_pickle')

    process = Popen(['mpirun', 'python3', parallel_script])

