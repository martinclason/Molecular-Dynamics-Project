def shearModulus(atom_list) :
    """Calculates shearModulus"""
    r0 = atom_list[0].get_positions()[0]
    r1 = atom_list[1].get_positions()[0]
    r_vec = r1 - r0
    r_len = (r_vec[0]**2 + r_vec[1]**2 + r_vec[2]**2)**(1/2)
    F = atom_list[0].get_forces()
    l = atom_list[0].get_cell_lengths_and_angles()[0] #cubic unit cell length
    return F / (l * r_len)