from command_line_arg_parser import parser

# asap option
def test_default_option():
    """Should default to use asap"""
    args = parser.parse_args([])
    assert args.use_asap

def test_asap_option():
    args = parser.parse_args(['--asap'])
    assert args.use_asap

def test_no_asap_option():
    args = parser.parse_args(['--no-asap'])
    assert not args.use_asap

# config file
def test_config_file_argument():
    args = parser.parse_args([])
    assert args.config_file.name == './config.yaml'

# TODO: Add test for custom config files
