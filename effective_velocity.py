from shear_modulus import shear_modulus
from density import density

def longtitudinalSoundWaveVelocity(atom_list) :
    """longtitudinalSoundWaveVelocity(atom_list) takes one argument, 
    a list of atoms objects. It calculates and returns the transversal
    velocity of a sound wave by calling shearModulus(atom_list),
    bulkModulus(atom_list) and density()"""
    #K = bulk_modulus(atom_list)
    K = 123 * 1E9 #bulk modulus for copper 
    G = shear_modulus(atom_list)
    G = 44.7 * 1E9 #shear modulus for copper
    rho = density(atom_list, 0) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_l = ((K + 4/3 * G)/rho)**0.5 #longitudinal sound wave velocity
    return c_l
    
def transversalSoundWaveVelocity(atom_list) :
    """transversalSoundWaveVelocity(atom_list) takes one argument, 
    a list of atoms objects. It calculates and returns the transversal
    velocity of a sound wave by calling shearModulus(atom_list) and
    density()"""
    G = shear_modulus(atom_list)
    G = 44.7 * 1E9 #shear modulus for copper
    rho = density(atom_list, 0) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_t = (G / rho)**0.5 #transversal sound wave velocity
    return c_t

def effectiveVelocity(atom_list) :
    """effectiveVelocity() calculates and returns the effective velocity
    by calling transversalSoundWaveVelocity(atom_list) and 
    longtitudinalSoundWaveVelocity(atom_list)."""
    c_t = transversalSoundWaveVelocity(atom_list)
    c_l = longtitudinalSoundWaveVelocity(atom_list)
    print("Transversal velocity:", c_t)
    print("Longitudinal velocity:", c_l)
    #sonic velocity from longtitudinal and transversal sound waves
    c_eff = (1/3 * c_l**-3 + 2/3 * c_t**-3)**(-1/3) 
    return c_eff