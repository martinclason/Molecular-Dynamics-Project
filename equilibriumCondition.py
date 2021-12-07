from ase.io.trajectory import Trajectory
import numpy as np
from ase import atoms, units
import sys

def equilibiriumCheck(atomsTraj, numberOfAtoms, ensamble,checkInterval):

    traj = Trajectory(atomsTraj)

    """This function determines if the system has reached an equilibrium which
    then determines if the simulation has reached equilibrium. This checks the 
    temperature if the NVE ensamble is used and the energy if the NVT ensamble
    is used. 
    
    The condition is to have a low variance in the temperature/energy in the last 
    batch of itterations which will depend on the size of the system."""    

    if ensamble == "NVE":

        T1 = [atoms.get_temperature() for atoms in traj[-2*checkInterval:-checkInterval]]
        T2 = [atoms.get_temperature() for atoms in traj[-checkInterval:]]
        meanT = np.sum(T2)/checkInterval

        var_T1 = np.var(T1)
        var_T2 = np.var(T2)

        # After some tests the following formula was derived to determine the 
        # equilibirium condition.
        tolerance = meanT / 80 + 0.7

        if (np.abs(var_T1 - var_T2) < tolerance):
            eqState = True
        else:
            eqState = False
    
    elif ensamble == "NVT":

        E1 = [atoms.get_temperature() for atoms in traj[-2*checkInterval:-checkInterval]]
        E1 = [energy / numberOfAtoms for energy in E1] 
        E2 = [atoms.get_temperature() for atoms in traj[-checkInterval:]]
        E2 = [energy / numberOfAtoms for energy in E2] 

        var_E1 = np.var(E1)
        var_E2 = np.var(E2)

        tolerance = 10

        print(var_E1)
        print(var_E2)

        print(tolerance)

        if (np.abs(var_E1 - var_E2) < tolerance):
            eqState = True
        else:
            eqState = False
    
    else:
        # Throws an exception if the specified ensamble isn't supported.
        raise Exception("Unknown ensamble: {}".format(ensamble))

    return eqState
    