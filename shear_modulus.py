from ase import Atoms
from ase.calculators.emt import EMT
from ase.calculators.kim.kim import KIM
import math

import yaml
from ase.md.velocitydistribution import (MaxwellBoltzmannDistribution,Stationary,ZeroRotation)
from asap3 import Trajectory
from ase import units
import numpy as np
from asap3.md.verlet import VelocityVerlet
from ase.lattice.cubic import FaceCenteredCubic
#https://docs.materialsproject.org/methodology/elasticity/
# https://www.nature.com/articles/sdata20159.pdf

def shear_modulus(atom_list) :
    all_symbols = atom_list[0].get_chemical_symbols()
    size = atom_list[0].get_tags()[0]
    size_cube = size**3
    number_of_atoms = int(len(all_symbols) / size_cube) # Number of atoms per molecule
    molecule_symbols = all_symbols[0:number_of_atoms] #Retrieve masses from one molecule
    symbols = ''.join(molecule_symbols)
    interatomic_positions = atom_list[0].get_positions()[0:number_of_atoms]
 
    old_cell = atom_list[0].get_cell() / size
    displacement_angle = math.radians(5)
    new_cell = old_cell
    for i in range(2):
        old_x = old_cell[i][0]
        old_z = old_cell[i][2]
        
        new_x = old_x + old_z * math.sin(displacement_angle)
        new_cell[i][0] = new_x
        
        new_z = old_z * math.cos(displacement_angle)
        new_cell[i][2] = new_z
 
    atoms = Atoms(symbols, positions = interatomic_positions, cell = new_cell, pbc = True)
    atoms = atoms.repeat([size,size,size]) 

    atoms.calc = KIM("LJ_ElliottAkerson_2015_Universal__MO_959249795837_003")

    stress_z = (atoms.get_stress()[3]**2 + atoms.get_stress()[4]**2)**(1/2)
    unit_conversion = 160.21766208 * 10**9 # ev/Anstrom^3 to GPa to Pascal
    
    # shear stress z-component divided by tan of displacement angle
    # ASE provides stress-component in ev/A^3 which is converted to
    # pascal by unit_conversion. The factor 0.5 comes from the
    # definition of engineering shear strain
    G = stress_z/(math.tan(displacement_angle)) * unit_conversion * 0.5 
    print("SHEAR MODULUS:", G)
    return G
    
    ###########################################################################

    
    # config_file = open("config.yaml")
    # options = yaml.load(config_file, Loader=yaml.FullLoader)

    # iterations = options["iterations"] if options["iterations"] else 200
    # interval = options["interval"] if options["interval"] else 10

    # # Set the momenta corresponding to T=300K
    # MaxwellBoltzmannDistribution(atoms, temperature_K=options["temperature_K"])
    # # Is this where the temperature is halfed??
    # Stationary(atoms)
    # ZeroRotation(atoms)
    # # We want to run MD with constant energy using the VelocityVerlet algorithm.
    # dyn = VelocityVerlet(atoms, options["dt"] * units.fs)  # 5 fs time step.

    # if options["make_traj"]:
    #     traj = Trajectory(options["symbol"]+"-test"+".traj", "w", atoms, properties="energy, forces")
    #     dyn.attach(traj.write, interval=interval)

    # def printenergy(a=atoms):  # store a reference to atoms in the definition.
    #     """Function to print the potential, kinetic and total energy."""
    #     epot = a.get_potential_energy() / len(a)
    #     ekin = a.get_kinetic_energy() / len(a)
    #     print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
    #             'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))

    # # Now run the dynamics
    
    # dyn.attach(printenergy, interval=interval)
    # dyn.run(iterations)
    # if options["make_traj"]:
    #     traj.close()
    #     traj_read = Trajectory(options["symbol"]+"-test"+".traj")
    #     return traj_read

    # #return G