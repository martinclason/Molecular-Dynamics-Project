.. Molecular Dynamics Project documentation master file, created by
   sphinx-quickstart on Wed Nov  3 16:23:48 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Molecular Dynamics Project's documentation!
======================================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    ale:
        * :ref:`ale`
        * :ref:`analyse_main`
        * :ref:`ale_errors`    
        * :ref:`main`
        * :ref:`create_potential`
        * :ref:`create_atoms`
        * :ref:`simulation_data_IO`
   
    Property calculations:
        * :ref:`atomic_masses`
        * :ref:`bulk_modulus`
        * :ref:`cohesive_energy`
        * :ref:`debye_temperature`
        * :ref:`density`
        * :ref:`effective_velocity`
        * :ref:`MSD`
        * :ref:`pressure`
        * :ref:`shear_modulus`
        * :ref:`specific_heat_capacity`
    
    ale visualize:
        * :ref:`visualize_main`
        * :ref:`scatter`

    ale multi:
        * :ref:`multi`
        * :ref:`parallel_mpi_script`
        * :ref:`picle_options` 

This is the documentation for the molecular dynamics program .

.. Update the documentation
.. ========================
.. To add files to be tracked by the automatic documentation system run the following from the top directory::

..     sphinx-apidoc -o docs/ .
.. To make the documentation system regenerate the html documentation, run the following from the ``docs`` directory::

..     sphinx-build . _build

.. or::

..     make html

.. Read documentation
.. ==================
.. To read the documentation cd to the docs directory and run
.. '<web-browser-name> index.html>' in the terminal.

.. contents:: Table of contents

Indices and tables
==================

    ale::
    -----
        # :ref:`ale`
        # :ref:`analyse_main`
        # :ref:`ale_errors`    
        # :ref:`main`
        # :ref:`create_potential`
        # :ref:`create_atoms`
        # :ref:`simulation_data_IO`
   
    Property calculations::
    -----------------------
        # :ref:`atomic_masses`
        # :ref:`bulk_modulus`
        # :ref:`cohesive_energy`
        # :ref:`debye_temperature`
        # :ref:`density`
        # :ref:`effective_velocity`
        # :ref:`MSD`
        # :ref:`pressure`
        # :ref:`shear_modulus`
        # :ref:`specific_heat_capacity`
    
    ale visualize::
    ---------------
        # :ref:`visualize_main`
        # :ref:`scatter`

    ale multi::
    -----------
        # :ref:`multi`
        # :ref:`parallel_mpi_script`
        # :ref:`pickle_options` 
    
    other::
    -------
        # :ref:`genindex`
        # :ref:`modindex`
        # :ref:`search`
