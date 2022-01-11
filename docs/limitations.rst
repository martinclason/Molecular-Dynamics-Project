Limitations
===========

.. _openKIM: https://openkim.org/browse/models/by-species

Supported unit cells
--------------------
Ale only supports cubic lattices with one parameter. There are two preprogrammed bravais
lattices, face centered cubic (FCC) and body centered cubic (BCC), but more importantly
Ale can handle base matrices as long as it only scales with one parameter. However the
simulations which are setup by a basis matrix has not been as thoroughly tested as the
simulations which uses the built in FCC and BCC support.

Ale also supports multi atom simulations although these have proven to be unstable under
certain starting conditions and especially when using the simple built in Lennard Jones
potential which can cause super lattices to explode and crash the simulation.

Interatomic potentials
----------------------
The development team behind Ale highly encourages the user to look for adequate potentials
on the openKIM_ web site since these are
designed to function for certain elements and combinations of elements, which is crucial to
obtain good prediction of material properties. Ale only supports potentials labeled to
function with "any" simulator or with "asap" (which is used to accelerate calculations with
ale).

A word of warning is that some potentials which are labeled in the
openKIM_ library to function with any
simulator are known to crash or not function anyway for an unknown reason. These non-function
interatomic potentials have not been cataloged by the Ale team.

Built in Lennard Jones potential
********************************
The built in Lennard Jones is a kind of back-up potential and for it to function properly it
needs to have the model parameters ``epsilon`` and ``sigma`` supplied. The simulation will start
without the model parameters but the fallback parameters are designed for solid argon and it's
not recommended to use for anything else if the user's goal is to make predictions on material
properties.

The fallback parameters for the Lennard Jones potential are:

::

  atomic_number = 1 # unit charge
  epsilon = 0.010323 # eV
  sigma = 3.40 # Å
  cutoff = 6.625 # Å

|

Lattice constant calculation
----------------------------
The lattice constant calculation is heavily dependent on the initial guess
made in the config file (``guess_latticeconstant``). If no lattice constant
is provided at all there is a fallback guess of 4 Å but ale only checks an
interval of guess +- 15%*guess. This means that if the real or expected
lattice constant lies above 4.6 Å or below 3.4 Å a guess should be provided
or undefined behavior might occur in the simulation.

The quality of the calculated lattice constant also improves as the distance
between the ``guess_latticeconstant`` and the real/expected lattice constant
decreases. This includes the case where the real/expected lattice constant is
included in the interval created from the guessed lattice constant.

Equilibrium check
-----------------
The built in equilibrium check has only proven effective for sufficiently large
systems (around 1000 atoms or a size of 10 for an FCC lattice). A smaller
number of atoms tends to generate more oscillative behavior in the temperature
and energy, which is used to calculate if the system has reached equilibrium.

If the system doesn't reach equilibrium within a certain time, depending on the
size of the system and the write-to-trajectory-file-interval (``interval:`` in the
config file), the simulation will continue anyway and start producing the output
file in case the system reaches equilibrium later or if the system has reached
equilibrium but it hasn't been detected by Ale.

The output ``<element(s)>.json`` file contains information on the equilibrium
check, if the system reached equilibrium and how long it took to reach
equilibrium or for the equilibrium check to timeout.
