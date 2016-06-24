"""Management tools for aggregating and controlling tasks.

"""
import os
import json
import uuid
import datetime
import time
import glob

import pandas
import psutil

from .watchers.process_watcher import ProcessWatcher
from .watchers.platform_watcher import PlatformWatcher
from .commands.cli import DEFAULT_TASK_DIR, DEFAULT_REFRESH_RATE
from .commands.config import parse_config


class TaskManager(object):
    """Task manager for a single process.

    Aggregates data from multiple process watchers and writes it to a
    JSON file.

    Attributes:
      watchers: a list of watcher objects
      label: the unique label associated with the task
      datafile: the local data file to record the JSON record
      data_dict: the dictionary to gather the data

    """
    def __init__(self, pid, config_dir):
        """Instantiate a TaskManager.

        Args:
          pid: the process ID to watch
          config_dir: the CoRR configuration directory

        """
        self.watchers = [ProcessWatcher(pid),
                         PlatformWatcher(pid)]
        self.label = str(uuid.uuid4())
        task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        self.datafile = os.path.join(task_dir, '{0}.json'.format(self.label))
        self.data_dict = self.initialize_data(pid, config_dir)
        self.update_data()

    def initialize_data(self, pid, config_dir):
        """Intialize the data.

        Args:
          pid: the process ID to watch
          config_dir: the CoRR configuration directory

        Returns:
          the data dictionary

        """
        data_dict = {}
        config_data = parse_config(config_dir)
        email = config_data.get('default_email')
        name = config_data.get('default_name')
        data_dict = {'label' : self.label,
                     'process_id' : pid,
                     'created_time' : str(datetime.datetime.now()),
                     'email' : email,
                     'name' : name}
        return data_dict

    def update_data(self):
        """Update the data with the watchers.

        """
        self.data_dict['update_time'] = str(datetime.datetime.now())
        for watcher in self.watchers:
            self.data_dict = watcher.watch(self.data_dict)

    def write_data(self):
        """Write the data to a JSON file.
        """
        with open(self.datafile, 'w') as outfile:
            json.dump(self.data_dict, outfile)

def task_manager_callback(daemon_id, config_dir, logger=None):
    """Task manager callback function for running in a Daemon.

    Creates and removes TaskManager's as processes start and
    finish. Prompts TaskManager's to update data as frequently as
    possible and prompts TaskManager's to save data based on
    `refresh_rate`.

    Args:
      daemon_id: the ID of the daemon launching the call back
      config_dir: the CoRR configuration directory
      logger: a logger object

    """
    task_manager_dict = dict()
    config_data = parse_config(config_dir)
    refresh_rate = float(config_data.get('tasks_refresh_rate', DEFAULT_REFRESH_RATE))
    while True:
        tstart = time.time()
        pids = get_pids_for_identifier(daemon_id)
        task_manager_dict = update_task_manager_dict(pids, task_manager_dict, config_dir, logger)
        while (time.time() - tstart) < refresh_rate:
            update_task_manager_data(task_manager_dict)
        task_manager_dict = write_task_manager_data(task_manager_dict, logger)


def update_task_manager_dict(pids, task_manager_dict, config_dir, logger):
    """Add tasks to the task_manager_dict.

    Args:
      pids: list of pids that associated with the daemon_id
      task_manager_dict: a pid: TaskManager dictionary
      config_dir: the CoRR configuration directory
      logger: a logger object

    Returns:
      an updated task_manager_dict

    """
    for pid in pids:
        if not pid in task_manager_dict:
            task_manager_dict[pid] = TaskManager(pid, config_dir)
            if logger:
                label = task_manager_dict[pid].label
                logger.info("created task {0} with pid {1}".format(label, pid))
    return task_manager_dict

def update_task_manager_data(task_manager_dict):
    """Update the data in each TaskManager

    Args:
      task_manager_dict: a pid: TaskManager dictionary

    """
    for task_manager in task_manager_dict.values():
        task_manager.update_data()

def write_task_manager_data(task_manager_dict, logger):
    """Prompt the TaskManager's to write to file.

    Also, remove TaskManager's from the task_manager_dict if the
    process is finished of a zombie process.

    Args:
      task_manager_dict: a pid: TaskManager dictionary
      logger: a logger object

    Returns:
      an updated task_manager_dict
    """
    pids = list(task_manager_dict.keys())
    for pid in pids:
        task_manager_dict[pid].write_data()
        status = task_manager_dict[pid].data_dict['status']
        if status in ('finished', 'zombie'):
            label = task_manager_dict[pid].label
            if logger:
                logger.info("finished task {0} with pid {1}".format(label, pid))
            del task_manager_dict[pid]
    return task_manager_dict

def get_pids_for_identifier(identifier):
    """Get process IDs for a given identifier

    Checks to see if the identifier is part of the command line string
    of each process in the process table. For example

    $ python myjob.py 0df1d25782e9

    >>> pids = get_pids_for_identifier('0df1d25782e9')

    Args:
      identifier: the string to search in the process table

    Returns:
      a list of process IDs

    """
    pid_list = []
    for pid in psutil.pids():
        if any(identifier in item for item in psutil.Process(pid).cmdline()):
            pid_list.append(pid)
    return pid_list

def get_task_df(config_dir):
    """Read in all the task JSON files and make a dataframe.

    Args:
      config_dir: the CoRR configuration directory

    """
    task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
    regex = os.path.join(task_dir, '*.json')
    task_list = []
    for jsonfile in glob.glob(regex):
        with open(jsonfile, 'r') as infile:
            task_list.append(json.load(infile))
    return pandas.DataFrame(task_list)
