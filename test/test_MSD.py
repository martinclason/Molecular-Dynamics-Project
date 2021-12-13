from MSD import self_diffusion_coefficient, lindemann_criterion
from ase.io.trajectory import Trajectory

cuTraj = Trajectory('test/Cu.traj')
cuLiquidTraj = Trajectory('test/Cu-liquid.traj')

#Tests if the slab of solid copper has no self-diffusion
def test_self_diffusion_coefficient() :
    SDC = self_diffusion_coefficient(cuTraj)
    assert SDC == 0

#Make sure copper at 300K has not melted at the final time step
def test_solid_lindemann_criterion() :
    melting = lindemann_criterion(cuTraj)
    assert melting == False

#Make sure copper at 3000K has melted at the final time step
def test_liquid_lindemann_criterion() :
    melting = lindemann_criterion(cuLiquidTraj)
    assert melting == True