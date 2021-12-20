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
sphinx-apidoc -o docs/source/ ..
sphinx-build . _build
```

or:
```
sphinx-apidoc -o docs/source/ ..
make html
```

## Read documentation
To read the documentation cd to the docs directory and run:
```
<web-browser-name> _build/index.html
```

