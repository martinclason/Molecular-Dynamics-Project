from cohesive_energy import cohesive_energy, retrieve_cohesive_energy
from md_config_reader import config_parser
from createAtoms import createAtoms
from main import create_potential



#Creates an atom object and run cohesive energy simulation and 
# then checks with the real value for cohesive energy for copper.
def test_cohesive_energy():
    parsed_config_file = config_parser(open("config_Cu.yaml"))
    atoms = createAtoms(parsed_config_file)
    calc = create_potential(parsed_config_file, True)
    atoms.calc = calc
    iterations = 2000
    cohesive_energy(atoms,iterations)
    coh_E = retrieve_cohesive_energy("coh_E.traj")
    coh_E_Cu = 3.6
    assert coh_E < coh_E_Cu
    assert coh_E > 3.4
