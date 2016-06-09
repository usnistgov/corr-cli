"""Test the command line tool.
"""
from configparser import ConfigParser
from click.testing import CliRunner
from corrcli.commands.config import config


def test_config():
    """Test `corrcli config`.

    Test writing to a config file with corrcli.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_ini = 'test.ini'
        email = "test.test@test.com"
        url = "www.test.com"
        arguments = ['--ini_file={0}'.format(test_ini),
                     '--email={0}'.format(email),
                     '--url={0}'.format(url),
                     '--port=80']
        result = runner.invoke(config, arguments)
        assert result.exit_code == 0
        parser = ConfigParser()
        parser.read(test_ini)
        assert parser.get('default', 'email') == email
        assert parser.get('api', 'url') == url
