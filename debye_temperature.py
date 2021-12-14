import math 
from effective_velocity import longtitudinalSoundWaveVelocity, transversalSoundWaveVelocity, effectiveVelocity
from density import density
from atomic_masses import atomic_masses
from create_potential import create_potential, built_in_LennardJones

def debye_temperature(atoms_object, options) :
    """debyeTemperature(atoms_object) takes one argument, a list of atoms objects.
    It calculates and returns the debyeTemperature by calling effectiveVelocity()
    atomic_masses() and density()"""

    calc = create_potential(options)
    c_eff = effectiveVelocity(atoms_object, calc) #Find the sonic velocity (debye_temp. constant)
    
    #defining Planck-, Boltzmann- and Avogadro's constants
    h = 6.62607015E-34
    k = 1.38064852E-23
    pi = math.pi    
    N_a = 6.02214086E23
    
    #Retrieve material parameters
    rho = density(atoms_object) #g/cm3
    rho = rho * 1E6 #convert density to g/m3
    M_a = atomic_masses(atoms_object) #Sum of atom_masses per molecule
    debyeTemperature = h * c_eff / (2 * k) * (6/pi * N_a * rho / M_a)**(1/3)
    
    return debyeTemperature


