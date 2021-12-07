from ase.io.trajectory import Trajectory
import numpy as np
from ase import atoms, units
import sys
import queue

def equilibiriumCheck(atomsTraj, numberOfAtoms, ensamble,checkInterval,tolerance):

    traj = Trajectory(atomsTraj)

    """This function determines if the system has reached an equilibrium which
    then determines if the simulation has reached equilibrium. This checks the 
    temperature if the NVE ensamble is used and the energy if the NVT ensamble
    is used. 
    
    The condition is to have a low variance in the temperature/energy in the last 
    batch of itterations which will depend on the size of the system."""    

    if ensamble == "NVE":
        # T1 = []
        # T2 = []
        
        # for i in range(checkInterval):
        #     T1.append(atomsArray.get().get_temperature())

        # for i in range(checkInterval,2*checkInterval):
        #     T2.append(atomsArray.get().get_temperature())

        T1 = [atoms.get_temperature() for atoms in traj[0:checkInterval]]
        T2 = [atoms.get_temperature() for atoms in traj[-checkInterval:]]

        var_T1 = np.var(T1)
        var_T2 = np.var(T2)

        if np.abs(var_T1 - var_T2) < tolerance:
            eqState = True
        else:
            eqState = False
    
    elif ensamble == "NVT":
        # E1 = []
        # E2 = []

        # for i in range(checkInterval):
        #     E1.append(atomsArray.get().get_total_energy())

        # for i in range(checkInterval,2*checkInterval):
        #     E2.append(atomsArray.get().get_total_energy())

        E1 = [atoms.get_temperature() for atoms in traj[0:checkInterval]]
        E1 = [energy / numberOfAtoms for energy in E1] 
        E2 = [atoms.get_temperature() for atoms in traj[-checkInterval:]]
        E2 = [energy / numberOfAtoms for energy in E2] 

        var_E1 = np.var(E1)
        var_E2 = np.var(E2)

        if np.abs(var_E1 - var_E2) < tolerance:
            eqState = True
        else:
            eqState = False
    
    else:
        # Throws an exception if the specified ensamble isn't supported.
        raise Exception("Unknown ensamble: {}".format(ensamble))

    return eqState
    