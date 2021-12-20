from ase.calculators.kim.kim import KIM
from ase import units
from ale.errors import ConfigError

def built_in_LennardJones(options) :
    use_asap = options["use_asap"]
    # Fallback/default values if not present in config
    fallback_atomic_number = 1
    fallback_epsilon = 0.010323 # eV
    fallback_sigma = 3.40 # Å
    fallback_cutoff = 6.625 # Å

    if use_asap:
        print("Running LJ potential with asap")
        from asap3 import LennardJones

        atomic_number = options.get("atomic_number", fallback_atomic_number)
        epsilon = options.get("epsilon", fallback_epsilon) * units.eV
        sigma = options.get("sigma", fallback_sigma) * units.Ang
        cutoff = options.get("cutoff", fallback_cutoff) * units.Ang
        
        keys = ("atomic_number", "epsilon", "sigma", "cutoff")
        if not all (key in options for key in keys):
            print(f"Warning, using fallback values for some values in: {keys}")

        print("Using following parameters for LJ:")
        print(f"atomic_number: {atomic_number}")
        print(f"epsilon: {epsilon}")
        print(f"sigma: {sigma}")
        print(f"cutoff: {cutoff}")

        return LennardJones(
                [atomic_number],
                [epsilon],
                [sigma],
                rCut=cutoff,
                modified=True,
            )
    else:
        print("Running LJ potential with ase")
        from ase.calculators.lj import LennardJones

        epsilon = options.get("epsilon", fallback_epsilon) * units.eV
        sigma = options.get("sigma", fallback_sigma) * units.Ang
        
        keys = ("epsilon", "sigma")
        if not all (key in options for key in keys):
            print(f"Warning, using fallback values for some values in: {keys}")

        return LennardJones(
                epsilon=epsilon,
                sigma=sigma,
            )

def create_potential(options) :
    use_asap = options["use_asap"]
    potential_str = options["potential"]
    if potential_str.lower() in ("lj", "LennardJones".lower()):
        # return built in LennardJones
        return built_in_LennardJones(options)
    if "openkim:" in potential_str.lower():
        # extract openKIM id from string prefixed with 'openkim:'
        openKIMpotential_str = potential_str.split(":")[1]
        try:
            return KIM(openKIMpotential_str)
        except:
            raise ConfigError(
                    message=f"A openKIM potential couldn't be created from given config: {openKIMpotential_str}",
                    config_properties=["potential"],
                  )
    raise ConfigError(
                message=f"No potential could be created from given config: {potential_str}",
                config_properties=["potential"],
          )
