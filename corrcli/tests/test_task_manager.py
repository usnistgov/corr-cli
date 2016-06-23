"""Test the command line tool.
"""
from click.testing import CliRunner
import os
from corrcli.corr_daemon import CoRRDaemon
from subprocess import Popen
from time import sleep
from corrcli.task_manager import get_task_df
from corrcli.commands.cli import DEFAULT_REFRESH_RATE

def configure(config_dir, refresh_rate):
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'config',
                 'set',
                 '--email=test@test.com',
                 '--name="Test Person"',
                 '--refresh-rate={0}'.format(refresh_rate)]
    Popen(arguments).wait()
    sleep(3)

def start_daemon(config_dir):
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'start',
                 '--log',]
    Popen(arguments)
    sleep(4)

def stop_daemon(config_dir):
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'stop',
                 '--all']
    Popen(arguments)

def start_process(daemon_id, config_dir):
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
    refresh_rate = 1
    runner = CliRunner()
    with runner.isolated_filesystem() as config_path:
        configure(config_path, refresh_rate)
        start_daemon(config_path)
        daemon_df = CoRRDaemon.list(config_path)
        daemon_id = daemon_df.daemon_id[0]
        try:
            process = start_process(daemon_id, config_path)
            sleep(refresh_rate + 1)
            task_df = get_task_df(config_path)
        except: # pragma: no cover
            process.kill()
            raise
        process.kill()
        assert task_df is not None
        assert len(task_df) == 1
        assert task_df.status[0] != 'finished'
        sleep(refresh_rate + 1)
        task_df = get_task_df(config_path)
        assert len(task_df) == 1
        assert task_df.status[0] == 'zombie'
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
            sleep(DEFAULT_REFRESH_RATE * 2)
            task_df = get_task_df(config_path)
        except: # pragma: no cover
            process.kill()
            raise
        process.kill()
        assert task_df is not None
        assert len(task_df) == 1
        assert task_df.status[0] != 'finished'
        stop_daemon(config_path)
