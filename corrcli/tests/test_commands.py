"""Test the command line tool.
"""
from configparser import ConfigParser
from click.testing import CliRunner
from corrcli import cli
import os
from corrcli.corr_daemon import CoRRDaemon
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
        url = "www.test.com:80"
        arguments = ['--config-dir={0}'.format(test_dir),
                     'config',
                     '--email={0}'.format(email),
                     '--api={0}'.format(url)]
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        parser = ConfigParser()
        parser.read(test_ini)
        assert parser.get('default', 'email') == email
        assert parser.get('default', 'api') == url

        list_arguments = ['--config-dir={0}'.format(test_dir),
                          'config',
                          '--list']
        list_result = runner.invoke(cli, list_arguments)
        list_output = '[default]\nemail = {0}\napi = {1}\n\n\n'.format(email, url)
        assert list_result.exit_code == 0
        assert list_result.output == list_output


def start_daemon(config_dir):
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'start',
                 '--log']
    Popen(arguments)
    sleep(3)

def test_daemon_start():
    """Test `corrcli watch stop`
    """
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        start_daemon(config_path)
        daemon_df = CoRRDaemon.list(config_path)
        assert len(daemon_df) == 1
        stopped_df = CoRRDaemon.stop(config_path, all_daemons=True)
        assert stopped_df.daemon_id[0] == daemon_df.daemon_id[0]
        daemon_id = stopped_df.daemon_id[0]
        log_dir = os.path.join(config_path, 'corr_daemons')
        log_path = os.path.join(log_dir, daemon_id + '_daemon.log')
        with open(log_path, 'r') as fpointer:
            log_contents = fpointer.read()
        assert daemon_id in log_contents

def test_daemon_stop():
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        for _ in range(3):
            start_daemon(config_path)
        daemon_df = CoRRDaemon.list(config_path)
        daemon_id = daemon_df.daemon_id[0]
        assert len(daemon_df) == 3

        ## test stopping one daemon
        arguments = ['--config-dir={0}'.format(config_path),
                     'watch',
                     'stop',
                     '--watcher-id={0}'.format(daemon_id)]
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        daemon_df = CoRRDaemon.list(config_path)
        assert len(daemon_df) == 2

        ## test failing to supply daemon
        result = runner.invoke(cli, arguments[:3])
        assert result.exit_code == 0
        assert result.output == "Require a watcher ID to proceed.\n"

        ## test stopping multiple daemons
        arguments[3] = '--all'
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == 4
        sleep(3)
        daemon_df = CoRRDaemon.list(config_path)
        assert len(daemon_df) == 0

        ## test stopping with no daemons running
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        assert result.output == "No watchers stopped.\n"


def test_daemon_list():
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        start_daemon(config_path)
        arguments = ['--config-dir={0}'.format(config_path),
                     'watch',
                     'list']
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        CoRRDaemon.stop(config_path, all_daemons=True)
        sleep(3)
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        assert result.output == "No running daemons.\n"
