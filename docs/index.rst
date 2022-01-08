.. Molecular Dynamics Project documentation master file, created by
   sphinx-quickstart on Wed Nov  3 16:23:48 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _ASE: https://wiki.fysik.dtu.dk/ase/
.. _ASAP: https://wiki.fysik.dtu.dk/asap
.. _openKIM: https://openkim.org/browse/models/by-species
.. _limitations: limitations.html

Welcome to Molecular Dynamics Project's documentation!
======================================================

This is the documentation for the molecular dynamics program Ale. Ale is designed to 
be used in investigateing hypothetical materials and get a peak into their properties.
Ale is built upon the ASE_ (Atomic Simulation Enviroment) and ASAP_ (As Soon As Possible)
is used to speed up the calculations. Ale also supports importing openKIM_ interatomic 
potentials to further enhance the relevance of the simulation results.

As of now the program has been mostly tested on single element materials but does support 
multi element simulation in arbitrary cubic condifugartions. For more info consider reading
the limitations_.

Main functions
==============

Ale simulate
------------
Ale simulate runs the molecular dynamics simulation using classical mechanincs to evaluate 
the equations of motion for the system that is simulated. This does not limit the program 
to use only classical interatomic potentials in the simulations and it's highly encouraged 
to use the built in support to import interatomic potentials from openKIM_ which comes in a 
variaty of forms and is in most cases specific to the system that is simulated, which 
yields the best prediction of properties.

Ale analyze
-----------
Ale analyze is the module that calculates material properties from the behaivor of the atoms 
in the molecular dynamics simulation and stores them in a line .json file for easier analysis
in Ale visualize or in a third party software.

Ale visualize
-------------
Ale visualize allows the user to plot properties across the duration of the simulation or 
to create scatter plots of two properties in a large set of materials to compare large sets 
of materials or material categories.

Ale multi
---------
Ale multi allows the user to generate a combination of simulation setups and run them in 
parallel, either on a multi-core pc or on a supercomputer. This can be useful for 
investigateing large sets of materials or for researching differences between material 
categories. 

.. toctree::
    :maxdepth: 4
    :caption: Contents:

    install
    how_to_run
    config
    limitations
    output
    source/ale