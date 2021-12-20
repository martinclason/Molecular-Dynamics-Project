Running the software
====================
Run ale (both simulation and analyzation):
```
./ale
```

Without asap and with a special config:
```
./ale --no-asap -c my_config.yaml
```

Only run simulation:
```
./ale simulate -c my_config.yaml
```

Only run analyzation:
```
./ale analyze
```

Run visualization:
```
./ale visualize
```

Running the software without installing it as a package
-------------------------------------------------------
If you for some reason want to run the code without having to install it as a package with `pip` you can do the following this. Make sure you're in the project directory and run it as a python module with the following command:
```
python -m ale
```

This line can be followed by the arguments, e.g. `python -m ale -h`, as usual.

It's probably better to try to install it as a package using `pip` though. That way it will be possible to run `ale` from any directory (as long as you have activated your conda environment if you're using conda).

Running `ale multi` currently requires `ale` to be installed with `pip`.