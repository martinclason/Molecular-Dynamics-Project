import subprocess

def test_ale_small_simulation_ase():
    try:
        process = subprocess.run("./ale --no-asap config_small_test.yaml", shell=True, check=True)
    except:
        assert False, "ale couldn't run with ase"


def test_ale_small_simulation():
    try:
        process = subprocess.run("./ale config_small_test.yaml", shell=True, check=True)
    except:
        assert False, "ale couldn't run"