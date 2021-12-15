from specificHeatCapacity import specificHeatCapacity
from asap3 import Trajectory
import sys
import os

arTraj = Trajectory('test/Ar.traj')
cuTraj = Trajectory('test/Cu.traj')

# Test if the calculated specific heat capacity of Argon is somewhat
# close to the real value.

def test_specificHeatCapacity_Ar():
    C_v_Ar = specificHeatCapacity("NVE",arTraj)
    assert (C_v_Ar >= 0.2) and (C_v_Ar <= 0.5)


def test_specificHeatCapacity_Cu():
    C_v_Cu = specificHeatCapacity("NVT",cuTraj)
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
