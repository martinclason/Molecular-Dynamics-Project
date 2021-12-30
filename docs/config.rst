The config files
================

Stand-alone config file:
------------------------
The stand-alone config file contains the following fields and an entire simulation and
analisys can be created from this file.

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
```
This field specifies which interatomic potential to use. The built in potentials are 

```

```


```

```


```

```


```

```


```

```


```

```


```

```


```

```


```

```

Multi-config:
-------------