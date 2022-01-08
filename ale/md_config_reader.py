import yaml

def parse_config(config_file):
    """Parses a config file written in the YAML-format.
    """

    return yaml.load(config_file, Loader=yaml.FullLoader)
