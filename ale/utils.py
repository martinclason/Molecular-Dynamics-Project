import functools

def call_only_once(f):
    """Wrapper that makes sure a function is called only once.
    This is useful for example if it's known that a very 
    expensive function is run many times but with the same 
    parameters and return value. It's not memoization since
    this wrapper doesn't take the paramters into consideration.
    The parameters used on the first call dictates what value is 
    stored and returned upon all future calls. 

    This is thus not the same as memoization where the cache 
    takes parameter values into consideration. The reason this was 
    used instead of memoization was that the parameters to a target
    function weren't hashable and able to be used in memoization.
    """
    result = None
    
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        nonlocal result
        if not result:
            result = f(*args, **kwds)
        return result

    return wrapper


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
        from ale.bulk_modulus import calc_lattice_constant
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
