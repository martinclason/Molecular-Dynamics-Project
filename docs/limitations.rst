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
obtain good predicition of material properties. Ale only supports potentias labeled to 
function with "any" simulator or with "asap" (which is used to accelerate calculations with
ale). 

A word of warning is that some potentials which are labeled in the 
openKIM_ library to function with any 
simulator are known to crash or not function anyway for an unkown reason. These non-function 
interatomic potentials have not been cataloged by the Ale team.

Built in Lennard Jones potential
********************************


Lattice constant calculation
----------------------------


Equilibrium check
-----------------

