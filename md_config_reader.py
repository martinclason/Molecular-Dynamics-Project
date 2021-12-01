import yaml

def config_parser(config_file):
    return yaml.load(config_file, Loader=yaml.FullLoader)
