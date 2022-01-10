The config files
================

.. _openKIM: https://openkim.org/browse/models/by-species

Single run config file:
------------------------
The stand-alone config file contains the following fields and an entire simulation and
analisys can be created from this file.

Simulate:
*********

The user can specify a `latticeconstant` to use for the simulation but is this is left 
empty Ale will compute a lattice constant with the `guess_latticeconstant` as the
initial value. If `guess_latticeconstant` is left empty Ale has a fallback value of 4
Å. 
::

  latticeconstant: <double [Å]>
  guess_latticeconstant: <double>

|

The field `cell` specifies the unit cell structure. The user can specify fcc or bcc bravais 
lattices but other lattices has to be specified with a base matrix. Ale only support single
parameter cubic lattices.
::

  cell: <string or matrix>

|

The field `cell` is the instruction on where to but different species of atoms relative to the 
origin of the unit cell and the length scale is normalized to the unit cell size (to the lattice 
constant). This paramater is only important for multi element systems and  `[[0,0,0]]` should 
be used when simulating single element sytems.
::

  scaled_positions: <array of 3D positions>

|

The field `symbol` specifies the element or a string of elements to be simulated such as `"Au"` for gold 
or `"CuK"` for a copper and postassium alloy. These elements are then placed at the `scaled_positions`
in order.
::

  symbol: <string>

|

To use periodic boundary conditions enter `True` in the `pbc` field.
::

  pbc: <bool>

|

The field `size` specifies how many time to repeat the unit cell to a super cell in each 
dimension (e.g. 2 -> 2^3 = 8 times as large).
::

  size: <int>

|

This field pecifies if Ale should output a trajectory file. A trajectory file is needed for 
Ale analyze to function.
::

  make_traj: <bool>

|

This field specifies whether to run a simulation or not.
::

  run_MD: <bool>

|

This fied specifies which ensamble to simulate. Ale currently only supports `"NVT"` or 
`"NVE"` ensambles.
::

  ensemble: <string>

|

This field specifies how hard the thermostat should correct the temperature. The friction
number is usualy `1E-4` to `1E-2`.
::

  NVT_friction: <double>

|

This field specifies the initial temperature of the simulation. If the temperature should 
remain close to the specified value enter `"NVT"` in the `ensamble` field.
::

  temperature_K: <double [K]>

|

This field specifies whether Ale should check that the simulated system has reached equilibrium 
before writing to the output trajectory file. This check either terminates when equilibrium is 
or when the check timeout is reached.
::

  checkForEquilibrium: <bool>

|

This field specifies which interatomic potential to use. The recomended potentials are those 
found in the openKIM_ library and these are designated with `"openKIM:<potential_name>"`, in 
this case sigma and epsilon aren't needed. Atomic number, sigma, epsilon (model parameters) 
and cutoff is only used if the built in Lennard Jones potential is used, this potential is 
specified with `"LJ"`.
::

  potential: <string>
  sigma: <double [Å]>
  epsilon: <double [Å]>
  cutoff: <double [Å]>
  atomic_number: <int [unit charge]>

|

This field specifies the timestep for the simulation in femtoseconds.
::

  dt: <int [fs]> 

|

This field specifies the number of timesteps that should be taken in the simulation. In case 
the equilibrium check is enabled this is the number of itterations after equilibrium is reached 
or equilibirium timeout has occurred. In the case the equilibrium check isn't enabled this is the 
total number of iterations in the simulation.
::

  iterations: <int>

|

This field specifies how many timesteps that will be taken between each save of the simulation
state to the trajectory file(s).
::

  interval: <int>

|

This field specifies if the Ale should calculate the cohesive energy of the system which is done
after the system has reached equilibirium, or equilibirium timeout as long as the equilibirium 
check is enabled.
::

  calculateCohesiveEnergy: <bool>

|

This field specifies how many itterations the cohesive energy calculation should run at most.
::

  max_iterations_coh_E:

|

Analyze:
********

This field specifies a list of properties that Ale will calculate in the analyse step.
::

  output:
    - <yaml list of strings>

|

The properties that can be calculated are:
::

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

|

Visualize:
**********

This field specifies which properties to plot when `ale visualize` is run.
::

  visualize:
    - <yaml list of strings>

|

The properties that can be visualized are:
::

  - Temperature
  - Scatter

|

These fields specify which two properties that will be plotted in a scatter plot with d1 on 
one axis and d2 on the other. 
::

  scatter_type_d1: <string>
  scatter_type_d2: <string>

|

The properties that can be shown in a scatterplot are:
::
  
  Temperature
  Volume
  Specific Heat Capacity
  Density
  Average Pressure
  Self Diffusion Coefficient
  Lindemann criterion
  Optimal Lattice Constant
  Optimal Lattice Volume
  Bulk Modulus
  Debye Temperature
  Transversal Sound Wave Velocity
  Longitudinal Sound Wave Velocity
  Shear Modulus
  Cohesive Energy

|
 
This field specifies the path to the directory the output properties for the materials that will 
be included in the scatterplot are relative to where `ale visualize` is run.
::

  scatter_dir: <string>

|

This field can be used to specified a subset of the files in the `scatter_dir` that should 
be used in the scatter plot. If this field is left empty `ale visualize` will look at all 
files.
::

  scatter_files: <array of strings>

|

This field specifies if the mean square displacement should be plotted against time for the 
entire simulation.
::

  run_MSD_plot: <bool>

|

Multi-config:
-------------

Ale supports using several processes to start multiple simulations in parallel which can be 
run locally (on a machine with a multi core processor) or on a supercomputer. 

.. This is run using
.. `multi` command such as 
.. ```
.. ale multi <multi_config> <output_dir> -c <base_config>
.. ```

The multi program then takes the fields in the `<multi_config>` and generates serveral simulations
with the `<base_config>` as the base and substitutes the fields specified in the `<multi_config>`.

For example:

`base_config.yaml`
::

  #-----------Atoms Setup------------#
  guess_latticeconstant: 5
  cell: # Given by m_config 
  scaled_positions : # Given by multi_config
  symbol : # Given by multi_config
  pbc : True 
  size : 22

  #-----------Simulation Setup------------#
  make_traj: True
  run_MD: True
  ensemble: "NVE" 
  temperature_K : # Given by multi_config
  checkForEquilibrium : True
  potential: # Given by multi_config.yaml
  dt: 5 # simulation time step [fs]
  iterations: 5000
  interval: 50

  #-----------Analyse------------#
  output:
    - Temperature
    - Volume
    - Debye Temperature
    - Self Diffusion Coefficient
    - Density
    - Pressure
    - MSD
    - Self Diffusion Coefficient Array
    - Specific Heat Capacity
    - Lindemann criterion

  #-----------Visualize------------#
  visualize:
    - Temperature
    - Scatter
  scatter_type_d1: "Density" 
  scatter_type_d2: "Specific Heat Capacity" 
  scatter_files: [] 
  run_MSD_plot: False

|

`multi_config.yaml`
::

  elements:
    - ["AlCu", "CuZr"] 

  potentials:
    AlCu: "openKIM:EAM_Dynamo_CaiYe_1996_AlCu__MO_942551040047_005"
    CuZr: "openKIM:EAM_Dynamo_BorovikovMendelevKing_2016_CuZr__MO_097471813275_000"
    default: "LJ"

  temperatures:
    AlCu: 17
    default: 600

  cells:
    CuZr: "BCC"
    default: "FCC"

  scaled_positions:
    AlCu: [[0, 0, 0], [0.17, 0.17, 0.17]]
    default: [[0, 0, 0], [0.5, 0.5, 0.5]]

|

With these input files `ale multi` will read the `multi_config.yaml` and create as many 
simulations as there are entries in the `elements` list and substitute the fields in the 
`base_config.yaml` with the fields specified in the `multi_config.yaml`. This allows the 
user to specify certain configurations for certain simulations and have a default setting 
in other cases to ease the configuration of a large number of simulations. The user can 
also define default values by specifying a value in the corresponding field in the 
`base_config.yaml`. 

The fields map as follows:

================ ================
multi_config     base_config
================ ================
elements         element
temperatures     temperature_K
cells            cell 
scaled_positions scaled_positions
================ ================

These two files will therefore create two simulations when run with `ale multi`, one with an 
aluminium and copper alloy at 17 K set in an FCC bravais lattice with the aluminium atoms place 
in the origin of the unit cell and repeated from there and the copper atoms shiftet inwards in 
the cell and and repeated in an FCC bravais lattice from there. The other simulation will be 
copper and zirconium placed in two BCC bravias lattices with the copper lattice beginning at 
the origin and the zirconium lattice being shifted a half unit cell in all directions and all 
of this will be simulated at 600 K.
