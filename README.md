# How to run the software:

## Install dependencies

### Using conda
Conda can be used to create an environment suitable for ale to run in. This environment could be called `my-md-env` for example.
This oneliner could be executed to create the environment and install the packages in one go:
```
conda create -c conda-forge -n my-md-env python=3 ase asap3 kimpy kim-api openkim-models Cython numpy scipy matplotlib mpi4py pytest openmpi
```
Followed by:
```
conda activate my-md-env
```

Alternatively, the `requirements.txt` could be used instead:
```
conda create -c conda-forge -n my-md-env python=3
conda activate my-md-env
conda install -c conda-forge --file requirements.txt
```
### Using pip
Pip could be used instead of conda but we have stuck with conda in this project.

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
source /courses/TFYA74/software/bin/init.sh
```

## Install the software
To be able to run ale in the terminal in your current environment, download this git repository and navigate into it. Then run:
```
python -m pip install .
```

This will read the script `setup.py` and pip will install `ale` as a command line tool. It will also install its dependencies but for this to work your environment must have installed `kim-api`, `openkim-models` and `openmpi`. These can be installed with e.g. conda. To test if `ale` was installed you can now run:

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

### Running the software without installing it as a package
If you for some reason want to run the code without having to install it as a package with `pip` you can do the following this. Make sure you're in the project directory and run it as a python module with the following command:
```
python -m ale
```

This line can be followed by the arguments, e.g. `python -m ale -h`, as usual.

It's probably better to try to install it as a package using `pip` though. That way it will be possible to run `ale` from any directory (as long as you have activated your conda environment if you're using conda).

Running `ale multi` currently requires `ale` to be installed with `pip`.

## Running tests
To run the unit tests and integrations tests with pytest run:
```
make test
```

# Documentation


## Update the documentation
Navigate to the root directory and run:
```
sphinx-apidoc -o docs/source/ ale
sphinx-build . _build
```

or:
```
sphinx-apidoc -o docs/source/ ../ale
make html-doc
```

### Generate docs in PDF-format
navigate to docs directory and run:
```
make latexpdf
```
The pdf should then be found at `docs/_build/latex/ale_md.pdf`.


## Read documentation
To read the documentation open the html-page in the build directory by running:
```
<web-browser-name> docs/_build/html/index.html
```

