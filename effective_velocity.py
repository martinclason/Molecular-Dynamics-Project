from shear_modulus import shear_modulus
from density import density

def longtitudinalSoundWaveVelocity(atoms_object) :
    """longtitudinalSoundWaveVelocity(atoms_object) takes one argument,
    a list of atoms objects. It calculates and returns the transversal
    velocity of a sound wave by calling shearModulus(atoms_object),
    bulkModulus(atoms_object) and density()"""
    # TODO: Why is this commented out?
    #K = bulk_modulus(atoms_object)
    K = 123 * 1E9 #bulk modulus for copper
    G = shear_modulus(atoms_object)
    rho = density(atoms_object) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_l = ((K + 4/3 * G)/rho)**0.5 #longitudinal sound wave velocity
    return c_l

def transversalSoundWaveVelocity(atoms_object) :
    """transversalSoundWaveVelocity(atoms_object) takes one argument,
    a list of atoms objects. It calculates and returns the transversal
    velocity of a sound wave by calling shearModulus(atoms_object) and
    density()"""
    G = shear_modulus(atoms_object)
    rho = density(atoms_object) #g/cm3
    rho = rho * 1E3 #kg/m3
    c_t = (G / rho)**0.5 #transversal sound wave velocity
    return c_t

def effectiveVelocity(atoms_object) :
    """effectiveVelocity() calculates and returns the effective velocity
    by calling transversalSoundWaveVelocity(atoms_object) and
    longtitudinalSoundWaveVelocity(atoms_object)."""
    c_t = transversalSoundWaveVelocity(atoms_object)
    c_l = longtitudinalSoundWaveVelocity(atoms_object)
    #sonic velocity from longtitudinal and transversal sound waves
    c_eff = (1/3 * c_l**(-3) + 2/3 * c_t**(-3))**(-1/3)
    return c_eff

