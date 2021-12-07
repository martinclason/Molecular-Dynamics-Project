.. Molecular Dynamics Project documentation master file, created by
   sphinx-quickstart on Wed Nov  3 16:23:48 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Molecular Dynamics Project's documentation!
======================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This is the documentation for the Molecular Dynamics Project in the course 
TFYA99 CDIO Project in Applied Physics.

Update the documentation
========================
To add files to be tracked by the automatic documentation system run the following from the top directory::

    sphinx-apidoc -o docs/source/ .
To make the documentation system regenerate the html documentation, run the following from the ``docs`` directory::

    sphinx-build . _build

or::

    make html

Read documentation
==================
To read the documentation cd to the docs directory and run
'<web-browser-name> index.html>' in the terminal.

.. contents:: Table of contents

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
