def shear_modulus(atom_list) :
    """Calculates shearModulus from a simulation by taking
    the force on an atom and dividing by the unit cell length
    times the displacement of the atom. shearModulus(atom_list)
    takes one argument, a list of atoms objects. It return
    the shear modulus as a number."""
    last_atom = len(atom_list[0]) - 1 #Find the index of the last atom
    r0 = atom_list[10].get_positions()[last_atom]
    r1 = atom_list[11].get_positions()[last_atom]

    r_vec = r1 - r0
    r_len = (r_vec[0]**2 + r_vec[1]**2 + r_vec[2]**2)**(1/2) * 1E-10 #distance between last atoms (m)
    
    F_vec = atom_list[10].get_forces()[last_atom]
    F_len = (F_vec[0]**2 + F_vec[1]**2 + F_vec[2]**2)**(1/2)
    
    l = atom_list[0].get_cell_lengths_and_angles()[0] * 1E-10 #cubic unit cell length (m)

    # print("Force on last atom:", F_len)
    # print("Force_vector on last atom:", F_vec)
    # print("Displacement of last atom:", r_len)
    # print("Length of cell:", l)
    
    return F_len / (l * r_len)