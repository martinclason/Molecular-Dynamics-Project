import math 
from ale.effective_velocity import effective_velocity
from ale.density import density
from ale.atomic_masses import atomic_masses

def debye_temperature(atoms_object, options, bulk_modulus) :
    """debyeTemperature(atoms_object) takes two argument, an atoms objects and
    options (a config-file). It calculates and returns the Debye temperature by 
    calling effectiveVelocity atomic_masses and density"""
    
    c_eff = effective_velocity(atoms_object, options, bulk_modulus) #Find the sonic velocity (debye_temp. constant)
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


