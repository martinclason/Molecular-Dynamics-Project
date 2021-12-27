import json
import os


def input_simulation_data(out_file_path):
    """This function returns data found in file at out_file_path.
    If this file can't be read it will return None.

    :param str out_file_path: file path from which to read data.
    """
    # TODO: Make this prettier...
    if not os.path.isfile(out_file_path):
        print(f"Couldn't find file {out_file_path}")
        return None

    read_data = {}

    with open(out_file_path, "r") as f:
        for line in f:
            read_data.update(json.loads(line))

    return read_data


def output_generic_from_traj(traj, out_file, name, f):
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
            name: values
        }
        json.dump(data, fp=out_file)
        # Newline to generate JSON Lines data, one doc per line
        out_file.write('\n')

    return output


def output_generic_result_lazily(out_file, name, retrieve_result):
    """This function is used to output data to file. It doesn't do this straight away
    but instead returns a function which can be called when the data actually should
    be written.

    When the returned function is called a complete JSON-document containing data
    from retrieve_result will be written as one line to the JSON-file.

    :param out_file: file handle to write data to.
    :param name: name to store data under in file.
    :param retrieve_result: function that returns data to write. This should take
                            no arguments and is only called when calling the returned function.
    """

    def output():
        result = retrieve_result()
        data = {
            name: result
        }
        json.dump(data, fp=out_file)
        # Newline to generate JSON Lines data, one doc per line
        out_file.write('\n')

    return output


def output_single_property(out_file, name, value):
    """Returns a function which writes a single value to a JSON-file.

    When the returned function is called a complete JSON-document containing the value
    will be written as one line to the JSON-file.

    The resulting file will be in the JSON Lines format, i.e. one JSON-document
    on each line.

    :param out_file: file handle to write data to.
    :param str name: key that value should be stored under in file.
    :param value: value to write to file.
    """
    def output():
        data = {
            name: value
        }
        json.dump(data, fp=out_file)
        # Newline to generate JSON Lines data, one doc per line
        out_file.write('\n')

    return output
