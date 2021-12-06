from shear_modulus import shearModulus
from density import density

def longtitudinalSoundWaveVelocity(atom_list) :
    """longtitudinalSoundWaveVelocity(atom_list) takes one argument, 
    a list of atoms objects. It calculates and returns the transversal
    velocity of a sound wave by calling shearModulus(atom_list),
    bulkModulus(atom_list) and density()"""
    K = 0 #bulk modulus
    G = shearModulus(atom_list)
    density = 1 
    c_l = ((K + 4/3 * G)/density)**1/2 #longitudinal sound wave velocity
    return c_l
    
def transversalSoundWaveVelocity(atom_list) :
    """transversalSoundWaveVelocity(atom_list) takes one argument, 
    a list of atoms objects. It calculates and returns the transversal
    velocity of a sound wave by calling shearModulus(atom_list) and
    density()"""
    G = shearModulus(atom_list)
    density = 1 
    c_t = (G / density)**1/2 #transversal sound wave velocity
    return c_t

def effectiveVelocity(atom_list) :
    """effectiveVelocity() calculates and returns the effective velocity
    by calling transversalSoundWaveVelocity(atom_list) and 
    longtitudinalSoundWaveVelocity(atom_list)."""
    c_t = transversalSoundWaveVelocity(atom_list)
    c_l = longtitudinalSoundWaveVelocity(atom_list)
    #sonic velocity from longtitudinal and transversal sound waves
    c_eff = (1/3 * c_l**-3 + 2/3 * c_t**-3)**(-1/3) 
    return c_eff