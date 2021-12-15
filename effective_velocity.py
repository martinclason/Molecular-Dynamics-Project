from shear_modulus import shear_modulus
from density import density

def longtitudinalSoundWaveVelocity(atoms_object, options) :
    """longtitudinalSoundWaveVelocity(atoms_object) takes two arguments,
    an atoms objects and options (config-file). It calculates and 
    returns the longitudinal velocity of a sound wave by calling bulk_modulus
    shear_modulus and density"""
    # TODO: Why is this commented out?
    #K = bulk_modulus(atoms_object)
    K = 24 * 1E9 #bulk modulus for NaCl
    G = shear_modulus(options)
    rho = density(atoms_object) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_l = ((K + 4/3 * G)/rho)**0.5 #longitudinal sound wave velocity
    return c_l

def transversalSoundWaveVelocity(atoms_object, options) :
    """transversalSoundWaveVelocity(atoms_object) takes two arguments,
    an atoms objects and options (config-file). It calculates and 
    returns the transversal velocity of a sound wave by calling 
    shear_modulus and density"""
    G = shear_modulus(options)
    rho = density(atoms_object) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_t = (G / rho)**0.5 #transversal sound wave velocity
    return c_t

def effectiveVelocity(atoms_object, options) :
    """effectiveVelocity calculates and returns the effective velocity
    by calling transversalSoundWaveVelocity and
    longtitudinalSoundWaveVelocity."""
    c_t = transversalSoundWaveVelocity(atoms_object, options)
    c_l = longtitudinalSoundWaveVelocity(atoms_object, options)
    #sonic velocity from longtitudinal and transversal sound waves
    c_eff = (1/3 * c_l**(-3) + 2/3 * c_t**(-3))**(-1/3)
    return c_eff

