Running the software
====================
Run ale help for ale and its various subcommands:
::

  $ ale -h
  $ ale simulate -h
  $ ale analyze -h
  $ ale visualize -h
  $ ale multi -h
|

Run ale (both simulation and analyzation) using the default config file ``config.yaml``:
::

  $ ale

|

Without asap and with a special config (``--config`` can also be used):
::

  $ ale --no-asap -c my_config.yaml

|

All ale modules can be handed an output directory as a command line argument using the ``-d``
or ``--dir`` flag together with the path to the output directory relative to the current
working directory. The output files are named the symbol(s) (the elements) in the simulation
with either ``.traj`` or ``.json`` depending on the data. The names of the output file with the
flag ``-t`` or ``--traj`` to name the trajectory output files and the flags ``-o`` or ``--out`` to
name the output data files (``.json``).

To only run a simulation:
::

  $ ale simulate -c my_config.yaml

|

Only run analyzation and calculate properties from existing output files. The user doesn't
have to specify a trajectory file if ``ale analyze`` is started from a directory where both
the config file and the corresponding trajectory file are located. The command looks
as follows:
::

  $ ale analyze -c my_config.yaml

|

However a safer approach is to specify both the config file and the corresponding trajectory
file. Then the command is:
::

  $ ale analyze -c my_config.yaml -t symbol.traj

|

In the config file the user can specify which quantities that should be plotted and in which
directory the properties files for the scatter plot are located. The config file is specified
with the flag ``-c``. The directory for the output files can be specified with the flag ``-d``. The
directory containing the properties for the scatter can be specified with the flag ``-s``. To
run visualization:
::

  $ ale visualize -c my_config.yaml -d out_dir -s scatter_dir

|

Running the software without installing it as a package
-------------------------------------------------------
If you for some reason want to run the code without having to install it as a package with ``pip`` you can do the following this. Make sure you're in the project directory and run it as a python module with the following command:
::

  $ python -m ale

|

This line can be followed by the arguments, e.g. ``python -m ale -h``, as usual.

It's probably better to try to install it as a package using ``pip`` though. That way it will
be possible to run ``ale`` from any directory (as long as you have activated your conda
environment if you're using conda).

Running ``ale multi`` currently requires ``ale`` to be installed with ``pip``.

Running ale multi
-----------------

Ale multi needs two config files to be run, one base config file and one multi config file,
which specifies which simulations to generate from the multi config with the config file as
the template or base. Ale multi requires the user to specify an output directory to store the
output files in. To run ale multi, ``multi_config.yaml`` is the multi config file and ``out_dir``
is the name of the output directory for the generated files:
::

  ale multi multi_config.yaml -c base_config.yaml out_dir

|

Running tests
-----------------

To run the unit tests and integrations tests with pytest run:
::

  make test

|



