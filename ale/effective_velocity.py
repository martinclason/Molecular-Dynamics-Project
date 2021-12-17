from shear_modulus import shear_modulus
from density import density
from bulk_modulus import calc_lattice_constant

def longitudinal_sound_wave_velocity(atoms_object, options, bulk_modulus) :
    """longitudinal_sound_wave_velocity takes two arguments,
    an atoms objects and options (config-file). It calculates and 
    returns the longitudinal velocity of a sound wave by calling bulk_modulus
    shear_modulus and density"""
    K = bulk_modulus * 1E9 #(1E9 since bulk modulus is returned in GPa)
    G = shear_modulus(options)
    rho = density(atoms_object) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_l = ((K + 4/3 * G)/rho)**0.5 #longitudinal sound wave velocity
    return c_l

def transversal_sound_wave_velocity(atoms_object, options) :
    """transversa_sound_wave_velocity takes two arguments,
    an atoms objects and options (config-file). It calculates and 
    returns the transversal velocity of a sound wave by calling 
    shear_modulus and density"""
    G = shear_modulus(options)
    rho = density(atoms_object) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_t = (G / rho)**0.5 #transversal sound wave velocity
    return c_t

def effective_velocity(atoms_object, options, bulk_modulus) :
    """effective-Velocity calculates and returns the effective velocity
    by calling transversa_sound_wave_velocity and
    longitudinal_sound_wave_velocity."""
    c_l = longitudinal_sound_wave_velocity(atoms_object, options, bulk_modulus)
    c_t = transversal_sound_wave_velocity(atoms_object, options)
    #sonic velocity from longtitudinal and transversal sound waves
    c_eff = (1/3 * c_l**(-3) + 2/3 * c_t**(-3))**(-1/3)
    return c_eff

