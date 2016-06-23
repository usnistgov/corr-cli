import datetime
from .process_watcher import ProcessWatcher
from .platform_watcher import PlatformWatcher
import uuid
import os
import json
from .commands.cli import DEFAULT_TASK_DIR, DEFAULT_REFRESH_RATE
from .commands.config import parse_config
import time
import psutil
import glob
import pandas


class TaskManager(object):
    def __init__(self, pid, config_dir):
        self.label = str(uuid.uuid4())
        self.process_watcher = ProcessWatcher(pid)
        task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        self.datafile = os.path.join(task_dir, '{0}.json'.format(self.label))
        self.data_dict = dict()
        self.initialize_data(pid, config_dir)
        self.update_data()

    def initialize_data(self, pid, config_dir):
        config_data = parse_config(config_dir)
        email = config_data.get('default_email')
        name = config_data.get('default_name')
        data_dict = {'label' : self.label,
                     'process_id' : pid,
                     'created_time' : str(datetime.datetime.now()),
                     'email' : email,
                     'name' : name}
        PlatformWatcher().watch(data_dict)
        self.data_dict = data_dict

    def update_data(self):
        self.data_dict['update_time'] = str(datetime.datetime.now())
        self.process_watcher.watch(self.data_dict)

    def write_data(self):
        with open(self.datafile, 'w') as outfile:
            json.dump(self.data_dict, outfile)

def task_manager_callback(daemon_id, config_dir, logger=None):
    """Task manager control function for running in a Daemon.
    """
    task_manager_dict = dict()
    config_data = parse_config(config_dir)
    refresh_rate = float(config_data.get('tasks_refresh_rate', DEFAULT_REFRESH_RATE))
    while True:
        tstart = time.time()
        pids = get_pids_for_identifier(daemon_id)
        update_task_manager_dict(pids, task_manager_dict, config_dir, logger)
        while (time.time() - tstart) < refresh_rate:
            update_task_manager_data(task_manager_dict, logger)
        write_task_manager_data(task_manager_dict, logger)


def update_task_manager_dict(pids, task_manager_dict, config_dir, logger):
    for pid in pids:
        if not pid in task_manager_dict:
            task_manager_dict[pid] = TaskManager(pid, config_dir)
            if logger:
                label = task_manager_dict[pid].label
                logger.info("created task {0} with pid {1}".format(label, pid))

def update_task_manager_data(task_manager_dict, logger):
    for pid, task_manager in task_manager_dict.items():
        task_manager.update_data()

def write_task_manager_data(task_manager_dict, logger):
    pids = list(task_manager_dict.keys())
    for pid in pids:
        task_manager_dict[pid].write_data()
        status = task_manager_dict[pid].data_dict['status']
        if status in ('finished', 'zombie'):
            label = task_manager_dict[pid].label
            if logger:
                logger.info("finished task {0} with pid {1}".format(label, pid))
            del task_manager_dict[pid]

def get_pids_for_identifier(identifier):
    pid_list = []
    for pid in psutil.pids():
        if any(identifier in item for item in psutil.Process(pid).cmdline()):
            pid_list.append(pid)
    return pid_list

def get_task_df(config_dir):
    task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
    regex = os.path.join(task_dir, '*.json')
    task_list = []
    for jsonfile in glob.glob(regex):
        with open(jsonfile, 'r') as infile:
            task_list.append(json.load(infile))
    return pandas.DataFrame(task_list)
