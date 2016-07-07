"""Management tools for aggregating and controlling tasks.

"""
import uuid
import datetime
import time

import psutil

from .watchers.process_watcher import ProcessWatcher
from .watchers.platform_watcher import PlatformWatcher
from .commands.cli import DEFAULT_WRITE_REFRESH_RATE, DEFAULT_WATCH_REFRESH_RATE
from .commands.config import parse_config
from .stores.file_store import FileStore


class TaskManager(object):
    """Task manager for a single process.

    Aggregates data from multiple process watchers and writes it to
    the data stores.

    Attributes:
      watchers: a list of watcher objects
      label: the unique label associated with the task
      stores: store objects to store the task records
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
        self.label = str(uuid.uuid4().hex)
        self.stores = [FileStore(self.label, config_dir)]
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
        email = config_data.get('global_email') or config_data.get('default_email')
        author = config_data.get('global_author') or config_data.get('default_author')
        data_dict = {'label' : self.label,
                     'process_id' : pid,
                     'created_time' : str(datetime.datetime.now()),
                     'email' : email,
                     'author' : author}
        return data_dict

    def update_data(self):
        """Update the data with the watchers.

        """
        self.data_dict['update_time'] = str(datetime.datetime.now())
        for watcher in self.watchers:
            self.data_dict = watcher.watch(self.data_dict)

    def write_data(self):
        """Write the data to the record stores
        """
        for store in self.stores:
            store.write(self.data_dict)

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
    watch_refresh_rate = float(config_data.get('tasks_watch_refresh_rate',
                                               DEFAULT_WATCH_REFRESH_RATE))
    write_refresh_rate = float(config_data.get('tasks_write_refresh_rate',
                                               DEFAULT_WRITE_REFRESH_RATE))
    while True:
        tstart = time.time()
        pids = get_pids_for_identifier(daemon_id)
        task_manager_dict = update_task_manager_dict(pids, task_manager_dict, config_dir, logger)
        if len(task_manager_dict) > 0:
            while (time.time() - tstart) < write_refresh_rate:
                update_task_manager_data(task_manager_dict)
                time.sleep(watch_refresh_rate)
        else:
            time.sleep(write_refresh_rate)
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
