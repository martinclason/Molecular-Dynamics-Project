from ale.bulk_modulus import calc_lattice_constant


class EoSResults:
    """EoSResults stores results from EoS equations lazily.
    The class can be instantiated without running the costly computation but when
    someone tries to access a value, the computation will be run if it hasn't
    been run yet."""

    def __init__(self, options):
        self.options = options
        self.__optimal_lattice_constant = None
        self.__bulk_modulus = None
        self.__optimal_lattice_volume = None
        self._counter = 0

    def _run_calculations(self):
        self._counter = self._counter + 1
        a0, B0, v0 = calc_lattice_constant(self.options)
        self.__optimal_lattice_constant = a0
        self.__bulk_modulus = B0
        self.__optimal_lattice_volume = v0

    def get_optimal_lattice_constant(self):
        if not self.__optimal_lattice_constant:
            self._run_calculations()
        assert self._counter <= 1
        return self.__optimal_lattice_constant

    def get_bulk_modulus(self):
        if not self.__bulk_modulus:
            self._run_calculations()
        assert self._counter <= 1
        return self.__bulk_modulus

    def get_bulk_optimal_lattice_volume(self):
        if not self.__optimal_lattice_volume:
            self._run_calculations()
        assert self._counter <= 1
        return self.__optimal_lattice_volume
