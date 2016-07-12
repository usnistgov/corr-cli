"""File store for job JSON records.
"""

import json
import os
import glob

import fasteners

from ..commands.cli import DEFAULT_JOB_DIR


class FileStore(object):
    """File store for job JSON records.

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
          label: a unique job label
          config_dir: the CoRR configuration directory

        """
        job_dir = os.path.join(config_dir, DEFAULT_JOB_DIR)
        if not os.path.exists(job_dir):
            os.makedirs(job_dir)
        self.datafile = os.path.join(job_dir, '{0}.json'.format(label))
        self.lockfile = os.path.join(job_dir, '{0}.lock'.format(label))

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

    def remove(self):
        """Remove the data store for a job.

        Removes both the JSON file and the lock file.

        """
        os.remove(self.datafile)
        if os.path.isfile(self.lockfile):
            os.remove(self.lockfile)

    @staticmethod
    def read_all(config_dir):
        """Read in all the jobs in the store.

        Args:
          config_dir: the CoRR configuration directory

        Returns:
          a list of jobs dictionaries
        """
        job_dir = os.path.join(config_dir, DEFAULT_JOB_DIR)
        regex = os.path.join(job_dir, '*.json')
        job_list = []
        for jsonfile in glob.glob(regex):
            label = os.path.splitext(os.path.split(jsonfile)[1])[0]
            store = FileStore(label, config_dir)
            job_list.append(store.read())
        return job_list

    @staticmethod
    def get_long_labels(config_dir, short_labels):
        """Find the long labels corresponding to short labels.

        Args:
          config_dir: the CoRR configuration directory
          short_labels: a list of short labels

        Returns:
          a dictionary of long IDs
        """
        job_dir = os.path.join(config_dir, DEFAULT_JOB_DIR)
        regex = os.path.join(job_dir, '*.json')
        long_labels = {}
        for jsonfile in glob.glob(regex):
            long_label = os.path.splitext(os.path.split(jsonfile)[1])[0]
            for short_label in short_labels:
                if short_label in long_label:
                    long_labels[short_label] = long_label
        return long_labels
