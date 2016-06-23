"""Test the command line tool.
"""
from configparser import ConfigParser
from click.testing import CliRunner
from corrcli import cli
import os


def test_config():
    """Test `corrcli config`.

    Test writing to a config file with corrcli.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_dir = 'test_dir'
        test_ini = os.path.join(test_dir, 'config.ini')
        email = "test.test@test.com"
        arguments = ['--config-dir={0}'.format(test_dir),
                     'config',
                     'set',
                     '--email={0}'.format(email)]
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        parser = ConfigParser()
        parser.read(test_ini)
        assert parser.get('default', 'email') == email

        list_arguments = ['--config-dir={0}'.format(test_dir),
                          'config',
                          'list']
        list_result = runner.invoke(cli, list_arguments)
        list_output = '[default]\nemail = {0}\n\n\n'.format(email)
        assert list_result.exit_code == 0
        assert list_result.output == list_output
