import math 
from ase.data import atomic_masses, atomic_numbers
from shearModulus import shearModulus(atom_list)

def debyeTemperature(atom_list) :
    
    #Find the sonic velocity
    c_t = transversalSoundWaveVelocity(atom_list)
    c_l = longtitudinalSoundWaveVelocity(atom_list)
    c_eff = (1/3 * c_l**-3 + 2/3 * c_t**-3)**(-1/3) #sonic velocity from longtitudinal and transversal sound waves
    #print("The effective velocity is:", c_eff)
    
    #defining Planck-, Boltzmann- and Avogadro's constants
    h = 6.62607015E-34
    k = 1.38064852E-23
    pi = math.pi    
    N_a = 6.02214086E23
    
    #Retrieve material parameters
    symbol = 'Cu'
    atomic_number = atomic_numbers[symbol]
    density = 8.960E6 #g/m^3
    M_a = atomic_masses[atomic_number]

    debyeTemperature = h * c_eff / (2 * k) * (6/pi * N_a * density /M_a)**(1/3)
    return debyeTemperature

def longtitudinalSoundWaveVelocity(atom_list) :
    K = 0 #bulk modulus
    G = shearModulus(atom_list)
    density = 1 
    c_l = ((K + 4/3 * G)/density)**1/2
    return c_l
    
def transversalSoundWaveVelocity(atom_list) :
    G = shearModulus(atom_list)
    density = 1 
    c_t = (G / density)**1/2
    return c_t      
