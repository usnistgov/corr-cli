"""Test the CoRR-cli task command.
"""
import json
import os

from click.testing import CliRunner

from corrcli.stores.file_store import FileStore
from corrcli import cli


LIST_OUTPUT = """      label    status           time stamp    pid
0  68ede088  finished  2016-06-25 21:51:39  18879
1  6b3c991f  finished  2016-06-24 23:20:13  10405
2  19c8f844       NaN                  NaN     -1
"""

JSON_OUTPUT = """{
  "author": null,
  "cmdline": [
    "python",
    "ttt.py",
    "0bfdd24bb4fb"
  ],
  "created_time": "2016-06-25 21:51:39.702208",
  "cwd": "/home/dwheeler/git/corr-cli",
  "email": "daniel.wheeler2@gmail.com",
  "executable": "/home/dwheeler/anaconda/bin/python2.7",
  "label": "68ede088fe214c028dbfd1d197a3b378",
  "memory": 6488064,
  "node_name": "sinjin",
  "platform": "Linux-4.4.0-24-generic-x86_64-with-debian-stretch-sid",
  "process_created": 1466905897.09,
  "process_id": 18879,
  "process_name": "python",
  "status": "finished",
  "update_time": "2016-06-25 21:53:19.718295",
  "username": "dwheeler"
}
No such task as xxxxxxxx.
"""

REMOVE_OUTPUT = """Task 68ede088 removed.
No such task as xxxxxxxx.
"""

def test_list_tasks():
    """Test listing tasks.

    """
    datafile = os.path.join(os.path.dirname(__file__), 'test_data.json')
    with open(datafile, 'r') as infile:
        data = json.load(infile)
    runner = CliRunner()
    with runner.isolated_filesystem() as config_dir:
        for task in data:
            FileStore(task['label'], config_dir).write(task)
        arguments = ['--config-dir={0}'.format(config_dir),
                     'task',
                     'list']
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        assert result.output == LIST_OUTPUT


def test_list_json():
    """Test listing tasks as JSON.

    """
    datafile = os.path.join(os.path.dirname(__file__), 'test_data.json')
    with open(datafile, 'r') as infile:
        data = json.load(infile)
    runner = CliRunner()
    with runner.isolated_filesystem() as config_dir:
        for task in data:
            FileStore(task['label'], config_dir).write(task)
        arguments = ['--config-dir={0}'.format(config_dir),
                     'task',
                     'list',
                     '68ede088',
                     'xxxxxxxx']
        result = runner.invoke(cli, arguments)
        print(result.output)
        print(JSON_OUTPUT)
        assert result.exit_code == 0
        assert result.output.replace(' ', '') == JSON_OUTPUT.replace(' ', '')

def test_remove():
    """Test removing task records from the data store.
    """
    datafile = os.path.join(os.path.dirname(__file__), 'test_data.json')
    with open(datafile, 'r') as infile:
        data = json.load(infile)
    runner = CliRunner()
    with runner.isolated_filesystem() as config_dir:
        for task in data:
            FileStore(task['label'], config_dir).write(task)
        arguments = ['--config-dir={0}'.format(config_dir),
                     'task',
                     'remove',
                     '--force',
                     '68ede088',
                     'xxxxxxxx']
        result = runner.invoke(cli, arguments)
        assert result.exit_code == 0
        assert result.output == REMOVE_OUTPUT
        assert len(FileStore.read_all(config_dir)) == 2
