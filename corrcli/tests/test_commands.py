"""Test the command line tool.
"""
from configparser import ConfigParser
from click.testing import CliRunner
from corrcli import cli
import os
from corrcli.watcher import Watcher
from subprocess import Popen
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
        port = 80
        arguments = ['--config-dir={0}'.format(test_dir),
                     'config',
                     '--email={0}'.format(email),
                     '--url={0}'.format(url),
                     '--port={0}'.format(port)]
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        parser = ConfigParser()
        parser.read(test_ini)
        assert parser.get('default', 'email') == email
        assert parser.get('api', 'url') == url

        list_arguments = ['--config-dir={0}'.format(test_dir),
                          'config',
                          '--list']
        list_result = runner.invoke(cli, list_arguments)
        list_output = '[default]\nemail = {0}\n\n[api]\nurl = {1}\nport = {2}\n\n\n'.format(email, url, port)
        assert list_result.exit_code == 0
        assert list_result.output == list_output


def start_watcher(config_dir):
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'start',
                 '--log']
    Popen(arguments)
    sleep(3)

def test_watch_start():
    """Test `corrcli watch stop`
    """
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        start_watcher(config_path)
        watcher_df = Watcher.list(config_path)
        assert len(watcher_df) == 1
        stopped_df = Watcher.stop(config_path, all=True)
        assert stopped_df.watcher_id[0] == watcher_df.watcher_id[0]
        watcher_id = stopped_df.watcher_id[0]
        log_dir = os.path.join(config_path, 'corr_daemons')
        log_path = os.path.join(log_dir, watcher_id + '_daemon.log')
        with open(log_path, 'r') as fpointer:
            log_contents = fpointer.read()
        assert watcher_id in log_contents

def test_watch_stop():
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        for _ in range(3):
            start_watcher(config_path)
        watcher_df = Watcher.list(config_path)
        watcher_id = watcher_df.watcher_id[0]
        assert len(watcher_df) == 3

        ## test stopping one watcher
        arguments = ['--config-dir={0}'.format(config_path),
                     'watch',
                     'stop',
                     '--watcher-id={0}'.format(watcher_id)]
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        watcher_df = Watcher.list(config_path)
        assert len(watcher_df) == 2

        ## test failing to supply watcher
        result = runner.invoke(cli, arguments[:3])
        assert result.exit_code == 0
        assert result.output == "Require a watcher ID to proceed.\n"

        ## test stopping multiple watchers
        arguments[3] = '--all'
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        watcher_df = Watcher.list(config_path)
        assert len(watcher_df) == 0

        ## test stopping with no watchers running
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        assert result.output == "No watchers stopped.\n"


def test_watch_list():
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        start_watcher(config_path)
        arguments = ['--config-dir={0}'.format(config_path),
                     'watch',
                     'list']
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        Watcher.stop(config_path, all=True)
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        assert result.output == "No running daemons.\n"
