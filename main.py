"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import SimpleCubic, BodyCenteredCubic, FaceCenteredCubic,Diamond
from ase.lattice.tetragonal import SimpleTetragonal, CenteredTetragonal
from ase.lattice.orthorhombic import SimpleOrthorhombic, BaseCenteredOrthorhombic,FaceCenteredOrthorhombic, BodyCenteredOrthorhombic
from ase.lattice.monoclinic import SimpleMonoclinic, BaseCenteredMonoclinic
from ase.lattice.triclinic import Triclinic
from ase.lattice.hexagonal import Hexagonal, HexagonalClosedPacked, Graphite

from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin
from asap3 import Trajectory
from ase import units
from numpy import Statistics

import argparse


# Adds parser so user can choose if to use asap or not with flags from terminal
parser = argparse.ArgumentParser()
parser.add_argument('--asap', dest='asap', action='store_true')
parser.add_argument('--no-asap', dest='asap', action='store_false')
parser.set_defaults(feature=True)
args = parser.parse_args()

import yaml

config_file = open("config_ar.yaml")
parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

# Use Asap for a huge performance increase if it is installed

def density():
    atoms = createAtoms() #
    Element = parsed_config_file["Element"]
    #Properties for element
    Z = parsed_config_file["Z"] #Number of atoms
    M = parsed_config_file["M"] #Molar mass
    Na = parsed_config_file["Na"] #avogadros constant
    a = parsed_config_file["a"] # Lattice constant
    unitCellVolume = a**3
    density = Z * M / (Na * unitCellVolume)

    print('The density of ' + Element + ' is: ' + str(density) + " g/cm^3")

    return density

#Calculates the square of the kinetic energy diff for one time step
#from .traj file
# def calcHeatCapacity(t,time,atom_list):
#     kineticEnergies = atom_list.get_kinetic_energy()
#     N = len(kineticEnergies)
#     T = atom_list.get_temperature()
#     T = numpy.mean(T)
#     stdDevKE = numpy.std(kineticEnergies)
#     kB = ase.units.kB
    
#     heatCapacity = ((3*N*kB)/2)*(1-(2/(3*kB^2*T^2))*stdDevKE^2)^(-1)
# #     N = len(r0)
# #     diff= rt-r0
# #     squareddiff = diff**2
# #     summ = sum(sum(squareddiff))
# #     normsum = (1/N) * summ
#     #return math.sqrt(normsum[0]**2 + normsum[1]**2 + normsum[2]**2)
#     return heatCapacity

def MD():
    use_asap = args.asap

    use_asap = True

    atomic_number = parsed_config_file["atomic_number"]
    epsilon = parsed_config_file["epsilon"] * units.eV
    sigma = parsed_config_file["sigma"] * units.Ang
    cutoff = parsed_config_file["cutoff"] * units.Ang
    iterations = parsed_config_file["iterations"] if parsed_config_file["iterations"] else 200
    interval = parsed_config_file["interval"] if parsed_config_file["interval"] else 10

    if use_asap:
        print("Running with asap")
        from asap3 import EMT
        from asap3 import LennardJones
        size = parsed_config_file["size"]
    else:
        print("Running with ase")
        from ase.calculators.emt import EMT
        from ase.calculators.emt import LennardJones
        size = parsed_config_file["size"]
    # Set up a crystal
    atoms = createAtoms()

    # Describe the interatomic interactions with the Effective Medium Theory

    potential = parsed_config_file["potential"]
    known_potentials = {
      'EMT' : EMT(),
      'LJ' : LennardJones([atomic_number], [epsilon], [sigma],
                    rCut=cutoff, modified=True,),
    }

    atoms.calc = known_potentials[potential] if potential else EMT()

    # Set the momenta corresponding to T=300K
    t = parsed_config_file["temperature_K"]

    MaxwellBoltzmannDistribution(atoms, temperature_K=t)
    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    # dyn = VelocityVerlet(atoms, 5 * units.fs)  # 5 fs time step.
    # Langevin dynamics for NVT dynamics
    friction = 0.002
    dyn = Langevin(atoms, 5 * units.fs, temperature_K=t, friction=friction)

    if parsed_config_file["make_traj"]:
        traj = Trajectory(parsed_config_file["symbol"]+".traj", "w", atoms)
        dyn.attach(traj.write, interval=interval)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))


    # Now run the dynamics
    dyn.attach(printenergy, interval=interval)
    printenergy()
    dyn.run(iterations)
    if parsed_config_file["make_traj"]:
        traj.close()
        traj_read = Trajectory(parsed_config_file["symbol"]+".traj")
        print(traj_read[0].get_positions()[0])


def main():
    run_density = parsed_config_file["run_density"]
    run_MD = parsed_config_file["run_MD"]
    if run_density :
        density()
    if run_MD :
        MD()

def createAtoms() :
     directions=parsed_config_file["directions"]
     symbol=parsed_config_file["symbol"]
     size=(parsed_config_file["size"],
     parsed_config_file["size"],parsed_config_file["size"])
     pbc= parsed_config_file["pbc"]
     latticeconstants = parsed_config_file.get("latticeconstants")
     structure = parsed_config_file["structure"]
     if(structure == "SC") :
        return SimpleCubic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = latticeconstants[0] if latticeconstants else None)
     if(structure == "BCC") :
        return BodyCenteredCubic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = latticeconstants[0] if latticeconstants else None)
     if(structure == "FCC") :
        return FaceCenteredCubic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = latticeconstants[0] if latticeconstants else None)
     if(structure == "ST") :
        return SimpleTetragonal(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'c' : latticeconstants[2]})
     if(structure == "CT") :
        return CenteredTetragonal(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'c' : latticeconstants[2]})
     if(structure == "SO") :
        return SimpleOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
     if(structure == "BaCO") :
        return BaseCenteredOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
     if(structure == "FCO") :
        return FaceCenteredOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
     if(structure == "BCO") :
        return BodyCenteredOrthorhombic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2]})
     if(structure == "SM") :
        return SimpleMonoclinic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2],
                                                   'alpha' : latticeconstants[3]})
     if(structure == "BCM") :
        return BaseCenteredMonoclinic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2],
                                                   'alpha' : latticeconstants[3]})
     if(structure == "T") :
        print("Triclinic")
        return Triclinic(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'b' : latticeconstants[1],
                                                   'c' : latticeconstants[2],
                                                   'alpha' : latticeconstants[3],
                                                   'beta' : latticeconstants[4],
                                                   'gamma' : latticeconstants[5]})
     if(structure == "H") :
        if(len(directions) != 4) :
            print("Incorrect number of directional indices for hexagonal structure, use the 4" +
            "-index Miller-Bravais notation, creating SC-lattice instead")
            return SimpleCubic(directions = directions,
                                    symbol = symbol,
                                    size = size, pbc = pbc,
                                    latticeconstant = latticeconstants[0])
        return Hexagonal(directions = directions,
                                symbol = symbol,
                                size = size, pbc = pbc,
                                latticeconstant = {'a' : latticeconstants[0],
                                                   'c' : latticeconstants[2]})
     if(structure == "HCP") :
        if(len(directions) != 4) :
             print("Incorrect number of directional indices for hexagonal structure, use the 4" +
             "-index Miller-Bravais notation, creating SC-lattice instead")
             return SimpleCubic(directions = directions,
                                     symbol = symbol,
                                     size = size, pbc = pbc,
                                     latticeconstant = latticeconstants[0])
        return HexagonalClosedPacked(directions = directions,
                                        symbol = symbol,
                                        size = size, pbc = pbc,
                                        latticeconstant = {'a' : latticeconstants[0],
                                                           'c' : latticeconstants[2]})


main()
