import math 
from effective_velocity import longtitudinalSoundWaveVelocity, transversalSoundWaveVelocity, effectiveVelocity
from density import density
from atomic_masses import atomic_masses

def debye_temperature(atom_list) :
    """debyeTemperature(atom_list) takes one argument, a list of atoms objects.
    It calculates and returns the debyeTemperature by calling effectiveVelocity()
    atomic_masses() and density()"""
  
    c_eff = effectiveVelocity(atom_list) #Find the sonic velocity (debye_temp. constant)

    #defining Planck-, Boltzmann- and Avogadro's constants
    h = 6.62607015E-34
    k = 1.38064852E-23
    pi = math.pi    
    N_a = 6.02214086E23
    
    #Retrieve material parameters
    rho = density(atom_list, 0) #g/cm-3
    rho = rho * 1E6 #convert density to g/m-3
    M_a = atomic_masses(atom_list) #Sum of atom_masses per molecule

    print("Density:",rho)
    print("Atomic masses:",M_a)
    print("Effective velocity:", c_eff)
    c_eff = 2612

    debyeTemperature = h * c_eff / (2 * k) * (6/pi * N_a * rho / M_a)**(1/3)
    
    return debyeTemperature


