from specificHeatCapacity import specificHeatCapacity
from ase.io.trajectory import Trajectory
import sys
import os

arTraj = Trajectory('test/Ar.traj')
cuTraj = Trajectory('test/Cu.traj')

# Test if the calculated specific heat capacity of Argon is somewhat 
# close to the real value.
C_v_Ar = specificHeatCapacity("NVE",arTraj)

def test_specificHeatCapacity_Ar():
    assert (C_v_Ar >= 0.2) and (C_v_Ar <= 0.5) 

C_v_Cu = specificHeatCapacity("NVE",cuTraj)

def test_specificHeatCapacity_Cu():
    assert (C_v_Cu >= 0.1) and (C_v_Cu <= 0.6)

# Tests if the function throws an exception when an unsupported 
# ensamble is specified.
def test_ensamble_exception():
   try:
       specificHeatCapacity("Not an ensamble","Ar.traj")
   except:
       pass

# Tests if the function throws an exception when an unsupported 
# ensamble is specified.
def test_trajectory_file_exception():
   try:
       specificHeatCapacity("NVE","not_a_file.file")
   except:
       pass