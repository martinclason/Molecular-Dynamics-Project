# How to run the software:

## Install dependencies

### Using conda
This oneliner could be executed:
```
conda create -c conda-forge -n tfya99 python=3 ase asap3 kimpy kim-api openkim-models Cython numpy scipy matplotlib mpi4py
```
Followed by
```
conda activate tfya99
```

Alternatively, the `requirements.txt` could be used instead:
```
conda create -c conda-forge -n tfya99 python=3
conda install -c conda-forge --file requirements.txt
```
### Using pip
Install ASE:
```
pip install ase
```

Install ASAP:
```
pip install asap3
```


### On LiU Linux lab computer:

Install ASE and ASAP Python modules:
```
source/TFYA74/software/bin/init.sh
```

## Install the software
To be able to run ale in the terminal in your current environment, download this git repository and navigate into it. Then run:
```
python -m pip install .
```

This will read the script `setup.py` and pip will install `ale` as a command line tool. To test if this worked you can now run:

IMPORTANT:
To develop without having to reinstall ale all the time you can instead run:
```
python -m pip install --no-deps -e .
```
This will install `ale` without dependencies and in editable mode so the source code can be edited.

To test if this worked you can now run:
```
ale -h
```

If it shows the help message the installation worked!

## Running the software
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

# Documentation

## Update the documentation
Navigate to the docs directory and run:
```
sphinx-build . _build
```
or:
```
make html
```


## Read documentation
To read the documentation cd to the docs directory and run:
```
<web-browser-name> _build/index.html
```

