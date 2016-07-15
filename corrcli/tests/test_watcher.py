"""Test the command line tool.
"""
import os
from time import sleep

from click.testing import CliRunner

from corrcli import cli
from corrcli.watcher import Watcher
from corrcli.watcher import start_watcher


WATCHER_OUTPUT = """              process_id
watcher_id              \n{watcher_id}      {process_id}\n"""

def test_watcher_start():
    """Test `corrcli watch stop`
    """
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        with start_watcher(config_path, callback_func='test_callback') as (watcher_id_start, _):
            watcher_df = Watcher.list(config_path)
            assert len(watcher_df) == 1
            stopped_df = Watcher.stop(config_path, all_watchers=True)
            assert stopped_df.watcher_id[0] == watcher_df.watcher_id[0]
            watcher_id = stopped_df.watcher_id[0]
            log_dir = os.path.join(config_path, 'watchers')
            log_path = os.path.join(log_dir, watcher_id + '.log')
            with open(log_path, 'r') as fpointer:
                log_contents = fpointer.read()
            assert watcher_id in log_contents
            assert watcher_id == watcher_id_start

def test_watcher_stop():
    """Test stopping deamons

    """
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        with start_watcher(config_path, callback_func='test_callback'), \
             start_watcher(config_path, callback_func='test_callback'), \
             start_watcher(config_path, callback_func='test_callback'):

            watcher_df = Watcher.list(config_path)
            watcher_id = watcher_df.watcher_id[0]
            assert len(watcher_df) == 3

            ## test stopping one watcher
            arguments = ['--config-dir={0}'.format(config_path),
                         'watch',
                         'stop',
                         '{0}'.format(watcher_id)]
            result = runner.invoke(cli, arguments)
            assert result.exit_code == 0
            sleep(3)
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
            assert len(result.output.split('\n')) == 4
            sleep(3)
            watcher_df = Watcher.list(config_path)
            assert len(watcher_df) == 0

            ## test stopping with no watchers running
            result = runner.invoke(cli, arguments)
            assert result.exit_code == 0
            assert result.output == "No watchers stopped.\n"

def test_watcher_list():
    """Test listing running watchers

    """
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        with start_watcher(config_path, 'test_callback') as (watcher_id, process_id):
            arguments = ['--config-dir={0}'.format(config_path),
                         'watch',
                         'list']
            result = runner.invoke(cli, arguments)
            assert result.exit_code == 0
            process_id = str(process_id).rjust(6, ' ')
            assert result.output == WATCHER_OUTPUT.format(watcher_id=watcher_id, process_id=process_id)
            Watcher.stop(config_path, all_watchers=True)
            sleep(3)
            result = runner.invoke(cli, arguments)
            assert result.exit_code == 0
            assert result.output == "No running watchers.\n"

def test_no_watcher():
    """Test running the watcher as an attached process.

    """
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        arguments = ['--config-dir={0}'.format(config_path),
                     'watch',
                     'start',
                     '--no-daemon',
                     '--callback-func=test_callback_nosleep',
                     '--log']
        result = runner.invoke(cli, arguments)
        assert "Launch watcher with ID:" in result.output
        assert result.exit_code == 0
