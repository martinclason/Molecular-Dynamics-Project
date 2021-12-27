import yaml

def parse_config(config_file):
    return yaml.load(config_file, Loader=yaml.FullLoader)
