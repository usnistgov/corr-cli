"""Test the CoRR-cli task command.
"""
import json
import os

from click.testing import CliRunner

from corrcli.stores.file_store import FileStore
from corrcli import cli


LIST_OUTPUT = """      label    status         time stamp    pid
0  f561910e  finished  16-06-25 21:53:19  18879
1  137a30eb  finished  16-06-24 23:21:53  10405
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
        print(result.output)
        assert result.exit_code == 0
        assert result.output == LIST_OUTPUT
