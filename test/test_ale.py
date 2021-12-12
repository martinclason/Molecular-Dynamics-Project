import subprocess
import os
import signal
import pytest
# from time import sleep

small_test_config = "test/config_small_test.yaml"

@pytest.mark.integration
def test_ale_help():
    try:
        process = subprocess.run(
                        f"./ale -h",
                        shell=True,
                        check=True)
    except:
        assert False, "ale couldn't display help message"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_small_simulation_ase():

    try:
        process = subprocess.run(
                        f"./ale --no-asap -c {small_test_config}",
                        shell=True,
                        check=True)
    except:
        assert False, "ale couldn't run with ase"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_small_simulation():
    try:
        process = subprocess.run(
                        f"./ale -c {small_test_config}",
                        shell=True,
                        check=True)
    except:
        assert False, "ale couldn't run"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_simulate():
    try:
        process = subprocess.run(
                    f"./ale simulate -c {small_test_config}",
                    shell=True,
                    check=True)
    except:
        assert False, "ale simulate couldn't run"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_analyze():
    out_test_file = './out_test.json'
    if os.path.isfile(out_test_file):
        os.remove(out_test_file)

    assert not os.path.isfile(out_test_file), "Remove this file to run tests"

    try:
        process = subprocess.run(
                    f"./ale analyze -c {small_test_config} --out {out_test_file}",
                    shell=True,
                    check=True)
    except:
        assert False, "ale analyze couldn't run"

    assert os.path.isfile(out_test_file), "Out file wasn't created by analyze"
    os.remove(out_test_file)


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_visualize():
    try:
        process = subprocess.Popen(
                    f"./ale visualize",
                    shell=True,
                    preexec_fn=os.setsid)
        # sleep(1)
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except:
        assert False, "ale visualize couldn't run"

