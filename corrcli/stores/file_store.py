"""File store for task JSON records.
"""

import json
import os
import glob

import fasteners

from ..commands.cli import DEFAULT_TASK_DIR


class FileStore(object):
    """File store for task JSON records.

    Reads and writes to JSON files based on the label and the
    config_dir. Files are locked when reading and writing, only one
    process can read or write to a file.

    >>> from click.testing import CliRunner
    >>> runner = CliRunner()
    >>> label = 'test'
    >>> data = {'test' : 0}
    >>> with runner.isolated_filesystem() as config_dir:
    ...     file_store = FileStore(label, config_dir)
    ...     file_store.write(data)
    ...     data_in = file_store.read()
    >>> assert data == data_in

    Attributes:
      datafile: the datafile to write to and read from
      lockfile: the file used for locking reads and writes

    """
    def __init__(self, label, config_dir):
        """Instantiate a FileStore.

        Args:
          label: a unique task label
          config_dir: the CoRR configuration directory

        """
        task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        self.datafile = os.path.join(task_dir, '{0}.json'.format(label))
        self.lockfile = os.path.join(task_dir, '{0}.lock'.format(label))

    def read(self):
        """Read from the data nfile.

        Returns:
          the contents of the data file as a dictionary

        """
        with fasteners.InterProcessLock(self.lockfile):
            with open(self.datafile, 'r') as infile:
                return json.load(infile)

    def write(self, data):
        """Write to the data file
        """
        with fasteners.InterProcessLock(self.lockfile):
            with open(self.datafile, 'w') as outfile:
                json.dump(data, outfile, indent=2, sort_keys=True)

    @staticmethod
    def read_all(config_dir):
        """Read in all the tasks in the store.

        Args:
          config_dir: the CoRR configuration directory

        Returns:
          a list of task dictionaries
        """
        task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
        regex = os.path.join(task_dir, '*.json')
        task_list = []
        for jsonfile in glob.glob(regex):
            label = jsonfile[:-5]
            store = FileStore(label, config_dir)
            task_list.append(store.read())
        return task_list

    @staticmethod
    def get_long_labels(config_dir, short_labels):
        """Find the long labels corresponding to short labels.

        Args:
          config_dir: the CoRR configuration directory
          short_labels: a list of short labels

        Returns:
          a list of long IDs
        """
        task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
        regex = os.path.join(task_dir, '*.json')
        long_labels = []
        for jsonfile in glob.glob(regex):
            long_label = jsonfile[:-5]
            for short_label in short_labels:
                if short_label in long_label:
                    long_labels.append(long_label)
            if len(long_labels) == len(short_labels):
                break
        return long_labels
