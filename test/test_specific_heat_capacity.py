from ale.specificHeatCapacity import specificHeatCapacity
from asap3 import Trajectory
import sys
import os
import pytest

@pytest.fixture()
def ar_traj():
    ar_traj = Trajectory('test/Ar.traj')
    yield ar_traj

@pytest.fixture()
def cu_traj():
    cu_traj = Trajectory('test/Cu.traj')
    yield cu_traj

# Test if the calculated specific heat capacity of Argon is somewhat
# close to the real value.

def test_specificHeatCapacity_Ar(ar_traj):
    C_v_Ar = specificHeatCapacity("NVE",ar_traj)
    assert (C_v_Ar >= 0.2) and (C_v_Ar <= 0.5)


def test_specificHeatCapacity_Cu(cu_traj):
    C_v_Cu = specificHeatCapacity("NVT",cu_traj)
    assert (C_v_Cu >= 0.1) and (C_v_Cu <= 0.6)

# Tests if the function throws an exception when an unsupported
# ensemble is specified.
def test_ensemble_exception():
   try:
       specificHeatCapacity("Not an ensemble","Ar.traj")
   except:
       pass

# Tests if the function throws an exception when an unsupported
# ensemble is specified.
def test_trajectory_file_exception():
   try:
       specificHeatCapacity("NVE","not_a_file.file")
   except:
       pass
