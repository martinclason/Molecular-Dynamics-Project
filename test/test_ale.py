import subprocess
import os

small_test_config = "config_small_test.yaml"

def test_ale_small_simulation_ase():
    try:
        process = subprocess.run(f"./ale --no-asap -c {small_test_config}", shell=True, check=True)
    except:
        assert False, "ale couldn't run with ase"


def test_ale_small_simulation():
    try:
        process = subprocess.run(f"./ale -c {small_test_config}", shell=True, check=True)
    except:
        assert False, "ale couldn't run"

def test_ale_analyze():
    out_test_file = './out_test.json'
    if os.path.isfile(out_test_file):
        os.remove(out_test_file)

    assert not os.path.isfile(out_test_file), "Remove this file to run tests"

    try:
        process = subprocess.run(f"./ale simulate -c {small_test_config}", shell=True, check=True)
        process = subprocess.run(f"./ale analyze -c {small_test_config} --out {out_test_file}", shell=True, check=True)
    except:
        assert False, "ale couldn't run"

    assert os.path.isfile(out_test_file), "Out file wasn't created by analyze"
    os.remove(out_test_file)
