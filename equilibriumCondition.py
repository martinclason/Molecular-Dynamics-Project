from ase.io.trajectory import Trajectory
import numpy as np
from ase import atoms, units
import sys

def equilibiriumCheck(traj, numberOfAtoms, ensamble,checkInterval,tolerance):
    """This function determines if the system has reached an equilibrium which
    then determines if the simulation has reached equilibrium. This checks the 
    temperature if the NVE ensamble is used and the energy if the NVT ensamble
    is used. 
    
    The condition is to have a low variance in the temperature/energy in the last 
    batch of itterations which will depend on the size of the system."""

    if ensamble == "NVE":
        T1 = [atoms.get_temperature() for atoms in traj[-checkInterval:]]
        T2 = [atoms.get_temperature() for atoms in traj[-2*checkInterval:-checkInterval]]
        var_T1 = np.var(T1)
        var_T2 = np.var(T2)

        if np.abs(var_T1 - var_T2) < tolerance:
            eqState = True
        else:
            eqState = False
    
    elif ensamble == "NVT":
        total_energies1 = [atoms.get_total_energy() for atoms in traj[-checkInterval:]]
        total_energies1 = [energy / numberOfAtoms for energy in total_energies1] 
        var_E1 = np.var(total_energies1)

        total_energies2 = [atoms.get_total_energy() for atoms in traj[-2*checkInterval:-checkInterval]]
        total_energies2 = [energy / numberOfAtoms for energy in total_energies2] 
        var_E2 = np.var(total_energies2)

        if np.abs(var_E1 - var_E2) < tolerance:
            eqState = True
        else:
            eqState = False
    
    else:
        # Throws an exception if the specified ensamble isn't supported.
        raise Exception("Unknown ensamble: {}".format(ensamble))

    return eqState
    