import pytest
from ale.command_line_arg_parser import CreateParser

nop = lambda: None
# Dummy parser used for testing
parser = CreateParser(nop, nop, nop, nop, nop)

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


@pytest.fixture()
def subcommands_parser():
    print("Setup parser")

    nop = lambda: None

    args_parser = CreateParser(
                    default=lambda: 'default',
                    multi=lambda: 'multi',
                    simulate=lambda: 'simulate',
                    analyze=lambda: 'analyze',
                    visualize=lambda: 'visualize',
                    )
    yield args_parser
    print("Tear down parser")

class TestParserSubcommands():
    def test_default_option(self, subcommands_parser):
        args = subcommands_parser.parse_args([])
        assert args.sub_command() == 'default'

    def test_multi_option(self, subcommands_parser):
        """Makes shure multi subcommand crashes if no multi config file is passed"""
        with pytest.raises(SystemExit):
            args = subcommands_parser.parse_args(['multi'])

    def test_simulate_option(self, subcommands_parser):
        args = subcommands_parser.parse_args(['simulate'])
        assert args.sub_command() == 'simulate'

    def test_analyze_option(self, subcommands_parser):
        args = subcommands_parser.parse_args(['analyze'])
        assert args.sub_command() == 'analyze'

    def test_visualize_option(self, subcommands_parser):
        args = subcommands_parser.parse_args(['visualize'])
        assert args.sub_command() == 'visualize'

    def test_subcommands_with_config(self, subcommands_parser):
        args = subcommands_parser.parse_args(['simulate'])
        assert args.config_file.name == './config.yaml'

        args = subcommands_parser.parse_args(['simulate', '-c', 'test/config_small_test.yaml'])
        assert args.sub_command() == 'simulate'
        assert args.config_file.name == 'test/config_small_test.yaml'

    def test_with_asap(self, subcommands_parser):
        args = subcommands_parser.parse_args(['--no-asap', 'simulate', '-c', 'test/config_small_test.yaml'])
        assert args.sub_command() == 'simulate'
        assert args.use_asap == False
        assert args.config_file.name == 'test/config_small_test.yaml'

        args = subcommands_parser.parse_args(['simulate', '--no-asap', '-c', 'test/config_small_test.yaml'])
        assert args.sub_command() == 'simulate'
        assert args.use_asap == False
        assert args.config_file.name == 'test/config_small_test.yaml'

def test_traj_file_argument():
    args = parser.parse_args(['-t', 'test/Cu.traj'])
    assert args.traj_file_name == 'test/Cu.traj'

    args = parser.parse_args(['--traj', 'test/Cu.traj'])
    assert args.traj_file_name == 'test/Cu.traj'

def test_out_file_argument():
    args = parser.parse_args([])
    assert args.out_file_name == None

    args = parser.parse_args(['-o', 'my_out.json'])
    assert args.out_file_name == 'my_out.json'

    args = parser.parse_args(['--out', 'my_out.json'])
    assert args.out_file_name == 'my_out.json'

    args = parser.parse_args(['-d', 'my_dir'])
    assert args.out_dir == 'my_dir'

    args = parser.parse_args(['--dir', 'my_dir'])
    assert args.out_dir == 'my_dir'



# TODO: Add test for custom config files
