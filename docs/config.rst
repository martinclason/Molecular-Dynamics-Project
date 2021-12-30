The config files
================

Stand-alone config file:
------------------------
The stand-alone config file contains the following fields and an entire simulation and
analisys can be created from this file.

Simulate:
*********
```
latticeconstant: <double [Å]>
guess_latticeconstant: <double>
```
The user can specify a `latticeconstant` to use for the simulation but is this is left 
empty Ale will compute a lattice constant with the `guess_latticeconstant` as the
initial value. If `guess_latticeconstant` is left empty Ale has a fallback value of 4
Å.

```
cell: <string or matrix>
```
The field `cell` specifies the unit cell structure. The user can specify fcc or bcc bravais 
lattices but other lattices has to be specified with a base matrix. Ale only support single
parameter cubic lattices.

```
scaled_positions: <array of 3D positions>
```
This field is the instruction on where to but different species of atoms relative to the 
origin of the unit cell and the length scale is normalized to the unit cell sixe. This 
paramater is only important for multi element systems and  `[[0,0,0]]` should be used when 
simulating single element sytems.

```
symbol: <string>
```
Symbol specifies the element or a string of elements to be simulated such as `"Au"` for gold 
or `"CuK"` for a copper and postassium alloy. These elements are then placed at the `scaled_positions`
in order.

```
pbc: <bool>
```
To use periodic boundary conditions enter `True` in the `pbc` field.

```
size: <int>
```
The field `size` specifies how many time to repeat the unit cell to a super cell in each 
dimension (e.g. 2 -> 2^3 = 8 times as large).

```
make_traj: <bool>
```
This field pecifies if Ale should output a trajectory file. A trajectory file is needed for 
Ale analyze to function.

```
run_MD: <bool>
```
This field specifies whether to run a simulation or not.

```
ensemble: <string>
```
This fied specifies which ensamble to simulate. Ale currently only supports `"NVT"` or 
`"NVE"` ensambles.

```
NVT_friction: <double>
```
This field specifies how hard the thermostat should correct the temperature. The friction
number is usualy `1E-4` to `1E-2`.

```
temperature_K: <double [K]>
```
This field specifies the initial temperature of the simulation. If the temperature should 
remain close to the specified value enter `"NVT"` in the `ensamble` field.

```
checkForEquilibrium: <bool>
```
This field specifies whether Ale should check that the simulated system has reached equilibrium 
before writing to the output trajectory file. This check either terminates when equilibrium is 
or when the check timeout is reached.

```
potential: <string>
sigma: <double>
epsilon: <double>
```
This field specifies which interatomic potential to use. The recomended potentials are those 
found in the openKIM <https://openkim.org/browse/models/by-species> _ library and these are designated with `"openKIM:<potential_name>"`, in this 
case sigma and epsilon aren't needed. Sigma and epsilon is only used if the built in Lennard 
Jones potential is used, this potential is potential is specified with `"LJ"`.

```
dt: <int [fs]> 
```
This field specifies the timestep for the simulation in femtoseconds.

```
iterations: <int>
```
This field specifies the number of timesteps that should be taken in the simulation. In case 
the equilibrium check is enabled this is the number of itterations after equilibrium is reached 
or equilibirium timeout has occurred. In the case the equilibrium check isn't enabled this is the 
total number of iterations in the simulation.

```
interval: <int>
```
This field specifies how many timesteps that will be taken between each save of the simulation
state to the trajectory file(s).

```
calculateCohesiveEnergy: <bool>
```
This field specifies if the Ale should calculate the cohesive energy of the system which is done
after the system has reached equilibirium, or equilibirium timeout as long as the equilibirium 
check is enabled.

```
max_iterations_coh_E:
```
This field specifies how many itterations the cohesive energy calculation should run at most.

Analyze:
********

```
output: <yaml list of strings>
```
This field specifies a list of properties that Ale will calculate in the analyse step. The 
properties that can be calculated are:
```
- Temperature
- Volume
- Specific Heat Capacity
- Density
- Instant Pressure
- Average Pressure
- MSD # Mean Square Displacement
- Self Diffusion Coefficient
- Self Diffusion Coefficient Array
- Lindemann criterion
- Optimal Lattice Constant
- Optimal Lattice Volume
- Bulk Modulus
- Debye Temperature
- Transversal Sound Wave Velocity
- Longitudinal Sound Wave Velocity
- Shear Modulus
- Cohesive Energy
```

Visualize:
**********

```
visualize:
```
This field specifies which properties to plot when `ale visualize` is run. The properties 
that can be visualized are:
```
- Temperature
- Scatter
```

```
scatter_type_d1: <string>
scatter_type_d2: <string>
```
These fields specify which two properties that will be plotted in a scatter plot with d1 on 
one axis and d2 on the other. The properties that can be shown in a scatterplot are:
```
- Temperature
- Volume
- Specific Heat Capacity
- Density
- Average Pressure
- Self Diffusion Coefficient
- Lindemann criterion
- Optimal Lattice Constant
- Optimal Lattice Volume
- Bulk Modulus
- Debye Temperature
- Transversal Sound Wave Velocity
- Longitudinal Sound Wave Velocity
- Shear Modulus
- Cohesive Energy
```

```
scatter_dir: <string>
```
This field specifies the path to the directory the output properties for the materials that will 
be included in the scatterplot are relative to where `ale visualize` is run.

```
scatter_files: <array of strings>
```
This field can be used to specified a subset of the files in the `scatter_dir` that should 
be used in the scatter plot. If this field is left empty `ale visualize` will look at all 
files.

```
run_MSD_plot: <bool>
```
This field specifies if the mean square displacement should be plotted against time for the 
entire simulation.

Multi-config:
-------------

