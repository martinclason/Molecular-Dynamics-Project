import bulk_modulus
import unittest

assert calc_lattice_constant('Ag.traj') >= 4.0853*0.9
assert calc_lattice_constant('Ag.traj') <= 4.0853*1.1
