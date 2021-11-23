import argparse

# Adds parser so user can choose if to use asap or not with flags from terminal
parser = argparse.ArgumentParser()
parser.add_argument('--asap', dest='use_asap', action='store_true')
parser.add_argument('--no-asap', dest='use_asap', action='store_false')
parser.set_defaults(use_asap=True)
