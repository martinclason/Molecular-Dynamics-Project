import json

def outputGenericFromTraj(traj, out_file, name, f):
    """Creates and returns outputter function that dumps some data
    about atoms to json.

    :param traj: traj object containing atoms objects.
    :param outfile: open file handle that the data should be appended to.
    :param str name: name of data, this will be the name of the json-field.
    :param function f: lambda used to extract some data from an atoms object.
    """
    def output():
        values = [f(atoms) for atoms in traj]
        data = {
            name : values
        }
        json.dump(data, fp=out_file)
    return output