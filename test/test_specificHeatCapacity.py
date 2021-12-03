from specificHeatCapacity import specificHeatCapacity
import sys
import os

def test_file():
    assert os.path.isfile('test/Ar.traj')

# Test if the calculated specific heat capacity of Argon is somewhat 
# close to the real value.
C_v_Ar = specificHeatCapacity("NVE",'test/Ar.traj')

def test_specificHeatCapacity_Ar():
    assert (C_v_Ar >= 0.5) and (C_v_Ar <= 3) 

C_v_Cu = specificHeatCapacity("NVE",'test/Cu.traj')

def test_specificHeatCapacity_Cu():
    assert (C_v_Cu >= 0.1) and (C_v_Cu <= 0.7)

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

test_specificHeatCapacity_Ar()
test_specificHeatCapacity_Cu()
test_ensamble_exception()
test_trajectory_file_exception()