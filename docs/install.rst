Installation
============

Install dependencies
--------------------

Using conda
^^^^^^^^^^^
Conda can be used to create an environment suitable for ale to run in. This environment could be called ``my-md-env`` for example.
This oneliner could be executed to create the environment and install the packages in one go:
::

  $ conda create -c conda-forge -n my-md-env python=3 ase asap3 kimpy kim-api openkim-models Cython numpy scipy matplotlib mpi4py pytest openmpi


Followed by:
::

  $ conda activate my-md-env


Alternatively, the ``requirements.txt`` could be used instead:
::

  $ conda create -c conda-forge -n my-md-env python=3
  $ conda activate my-md-env
  $ conda install -c conda-forge --file requirements.txt


Using pip
^^^^^^^^^
Pip could be used instead but conda has been used during development in this project.

Install ASE:
::

  $ pip install ase


Install ASAP:
::

  pip install asap3


Other packages will need to be installed. See contents of ``requirements.txt``.

.. On LiU Linux lab computer:
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Install ASE and ASAP Python modules:
.. ::

..   $ source /courses/TFYA74/software/bin/init.sh

.. |

Install the software
--------------------
To be able to run ale in the terminal in your current environment, download this git repository and navigate into it. Then run:
::

  $ python -m pip install .


This will read the script ``setup.py`` and pip will install ``ale`` as a command line tool. To test if this worked you can now run:

IMPORTANT:
To develop without having to reinstall ale all the time you can instead run:
::

  $ python -m pip install --no-deps -e .


This will install ``ale`` without dependencies and in editable mode so the source code can be edited
without having to reinstall ale for the changes to take effect.

To test if ale is installed correctly you can now run:
::

  $ ale -h


If it shows the help message the installation worked!

