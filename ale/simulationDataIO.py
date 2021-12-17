import json
import os

def outputGenericFromTraj(traj, out_file, name, f):
    """Creates and returns outputter function that dumps some data
    about atoms to json.

    The resulting file will be in the JSON Lines format, i.e. one JSON-document
    on each line.

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
        # Newline to generate JSON Lines data, one doc per line
        out_file.write('\n')

    return output

def outputGenericResultLazily(out_file, name, retrieve_result):

    def output():
        result = retrieve_result()
        data = {
            name : result
        }
        json.dump(data, fp=out_file)
        # Newline to generate JSON Lines data, one doc per line
        out_file.write('\n')

    return output

def inputSimulationData(out_file_name="out.json"):
    # TODO: Make this prettier...
    if not os.path.isfile(out_file_name):
        print(f"Couldn't find file {out_file_name} for visualization...")
        return None

    read_data = {}

    with open(out_file_name, "r") as f:
        for line in f:
            read_data.update(json.loads(line))

    return read_data

def outputSingleProperty(out_file, name, value) :
    """Writes single value to json file"""
    def output():
        data = {
            name : value
        }
        json.dump(data, fp=out_file)
        # Newline to generate JSON Lines data, one doc per line
        out_file.write('\n')

    return output
