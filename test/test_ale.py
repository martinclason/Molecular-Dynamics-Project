import subprocess
import os
from os.path import join as joinPath
from os.path import isfile
import shutil
import signal
import pytest
# from time import sleep
from ale.md_config_reader import config_parser as config_file_parser

small_test_config = "test/config_small_test.yaml"
small_test_config_builtin_lj = "test/config_small_test_builtin_lj.yaml"
small_test_config_universal = "test/small_test_config_universal.yaml"
short_test_config = "test/config_extra_short.yaml"

@pytest.mark.integration
def test_test() :
    pass

@pytest.mark.integration
@pytest.mark.openkim
def test_ale_help():
    try:
        process = subprocess.run(
                        f"ale -h",
                        shell=True,
                        check=True)
    except:
        assert False, "ale couldn't display help message"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_small_simulation_ase():

    try:
        process = subprocess.run(
                        f"ale --no-asap -c {small_test_config}",
                        shell=True,
                        check=True)
    except:
        assert False, "ale couldn't run with ase"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_small_simulation_builtin_LJ():
    """Test built in LJ potential that doesn't depend on openKIM"""
    # TODO: This test should also test that analyze works. Currently it gives error:
    # AsapError: The height of the cell (1.96299) must be larger than 13.25
    try:
        process = subprocess.run(
                        f"ale simulate -c {small_test_config_builtin_lj}",
                        shell=True,
                        check=True)
    except:
        assert False, "ale couldn't run with built in LJ potential"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_short_multi():
    """Tests that multi runs and creates traj files in specified output directory"""

    output_dir = 'out_test'
    multi_config_file = 'test/multi_config_Cu_Ar.yaml'
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    os.mkdir(output_dir)

    assert os.path.isdir(output_dir)

    with open(multi_config_file, 'r') as f:
        multi_config = config_file_parser(f)
    print(multi_config['elements'])
    elements = multi_config['elements'][0]

    try:
        process = subprocess.run(
                        f"ale multi {multi_config_file} {output_dir} -c {short_test_config}",
                        shell=True,
                        check=True)

        for element in elements:
            assert isfile(joinPath(output_dir, f'{element}.traj')), \
                   f"Out file wasn't created by multi simulation run for {element}"
    except:
        assert False, "ale multi couldn't run"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_small_simulation():
    try:
        process = subprocess.run(
                        f"ale -c {small_test_config}",
                        shell=True,
                        check=True)
    except:
        assert False, "ale couldn't run"


@pytest.mark.integration
@pytest.mark.openkim
def test_ale_simulate():
    try:
        process = subprocess.run(
                    f"ale simulate -c {small_test_config}",
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
                    f"ale analyze -c {small_test_config} --out {out_test_file}",
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
                    f"ale visualize",
                    shell=True,
                    preexec_fn=os.setsid)
        # sleep(1)
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except:
        assert False, "ale visualize couldn't run"

