"""Test the command line tool.
"""
from configparser import ConfigParser
from click.testing import CliRunner
from corrcli import cli
import os
from corrcli.watcher import Watcher
from time import sleep


def test_config():
    """Test `corrcli config`.

    Test writing to a config file with corrcli.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_dir = 'test_dir'
        test_ini = os.path.join(test_dir, 'config.ini')
        email = "test.test@test.com"
        url = "www.test.com"
        arguments = ['--config-dir={0}'.format(test_dir),
                     'config',
                     '--email={0}'.format(email),
                     '--url={0}'.format(url),
                     '--port=80']
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        parser = ConfigParser()
        parser.read(test_ini)
        assert parser.get('default', 'email') == email
        assert parser.get('api', 'url') == url


def test_watch_start():
    """Test starting a watcher.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_dir = 'test_dir'
        arguments = ['--config-dir={0}'.format(test_dir),
                     'watch',
                     'start']
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        watcher_df = Watcher.list(test_dir)
        assert len(watcher_df) == 1
        stopped_df = Watcher.stop(test_dir, all=True)
        assert stopped_df == watcher_df
