"""Test the command line tool.
"""
import os
from subprocess import Popen
from time import sleep

from click.testing import CliRunner

from corrcli.corr_daemon import CoRRDaemon
from corrcli.commands.cli import DEFAULT_WRITE_REFRESH_RATE
from corrcli.stores.file_store import FileStore
from corrcli.tools import start_daemon


def configure(config_dir, refresh_rate):
    """Configure CoRR

    """
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'config',
                 'set',
                 '--email=test@test.com',
                 '--author="Test Person"',
                 '--write-refresh-rate={0}'.format(refresh_rate)]
    Popen(arguments).wait()
    sleep(3)

def stop_daemon(config_dir):
    """Stop all daemons

    """
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'stop',
                 '--all']
    Popen(arguments)

def start_process(daemon_id, config_dir):
    """Launch a test process.

    """
    contents = """
import time
while True:
    time.sleep(10.0)
"""
    test_process_file = os.path.join(config_dir, 'test_process.py')
    with open(test_process_file, 'w') as fout:
        fout.write(contents)
    arguments = ['python',
                 test_process_file,
                 daemon_id]
    process = Popen(arguments)
    return process

def test_task_manager():
    """Test that tasks can be captured.
    """
    write_refresh_rate = 1
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        configure(config_path, write_refresh_rate)
        start_daemon(config_path)
        daemon_df = CoRRDaemon.list(config_path)
        daemon_id = daemon_df.daemon_id[0]
        try:
            process = start_process(daemon_id, config_path)
            sleep(write_refresh_rate + 1)
            tasks = FileStore.read_all(config_path)
        except: # pragma: no cover
            process.kill()
            raise
        process.kill()
        assert len(tasks) == 1
        assert tasks[0]['status'] != 'finished'
        sleep(write_refresh_rate + 1)
        tasks = FileStore.read_all(config_path)
        assert len(tasks) == 1
        assert tasks[0]['status'] == 'zombie'
        stop_daemon(config_path)


def test_noconfig():
    """Test that jobs are captured when no config set.
    """
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        start_daemon(config_path)
        daemon_df = CoRRDaemon.list(config_path)
        daemon_id = daemon_df.daemon_id[0]
        try:
            process = start_process(daemon_id, config_path)
            sleep(DEFAULT_WRITE_REFRESH_RATE * 2)
            tasks = FileStore.read_all(config_path)
        except: # pragma: no cover
            process.kill()
            raise
        process.kill()
        assert len(tasks) == 1
        assert tasks[0]['status'] != 'finished'
        stop_daemon(config_path)
