from ase.io.trajectory import Trajectory
import numpy as np
from ase import atoms, units
import sys

def equilibiriumCheck(traj, numberOfAtoms, checkNumber):
    """This function determines if the system has reached an equilibrium which
    then determines if the simulation """

    # First draft.
    eqState = True

    return eqState