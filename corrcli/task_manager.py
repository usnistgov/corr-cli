import datetime
from .process_watcher import ProcessWatcher
from .platform_watcher import PlatformWatcher
import uuid
import os
import json
from .commands.cli import DEFAULT_TASK_DIR
from .commands.config import parse_config
import time
import psutil


class TaskManager(object):
    def __init__(self, pid, config_dir):
        self.label = str(uuid.uuid4())
        self.process_watcher = ProcessWatcher(pid)
        task_dir = os.path.join(config_dir, DEFAULT_TASK_DIR)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        self.datafile = os.path.join(task_dir, '{0}.json'.format(self.label))
        data_dict = self.initialize_data(pid, config_dir)
        self.write_data(data_dict)
        self.update_data()

    def initialize_data(self, pid, config_dir):
        config_data = parse_config(config_dir)
        email = config_data.get('default', 'email')
        name = config_data.get('default', 'name')
        data_dict = {'label' : self.label,
                     'process_id' : pid,
                     'create_time' : str(datetime.datetime.now()),
                     'email' : email,
                     'name' : name}
        PlatformWatcher().watch(data_dict)
        return data_dict

    def update_data(self):
        data_dict = self.read_data()
        data_dict['update_time'] = str(datetime.datetime.now())
        self.process_watcher.watch(data_dict)
        self.write_data(data_dict)
        return data_dict['status']

    def write_data(self, data_dict):
        with open(self.datafile, 'w') as outfile:
            json.dump(data_dict, outfile)

    def read_data(self):
        with open(self.datafile, 'r') as infile:
            data_dict = json.load(infile)
        return data_dict

def task_manager_callback(daemon_id, config_dir, logger=None):
    task_manager_dict = dict()
    config_data = parse_config(config_dir)
    refresh_rate = float(config_data.get('tasks', 'refresh_rate'))
    while True:
        pids = get_pids_for_identifier(daemon_id)
        update_task_manager_dict(pids, task_manager_dict, config_dir, logger)
        update_task_manager_data(task_manager_dict, logger)
        time.sleep(refresh_rate)

def update_task_manager_dict(pids, task_manager_dict, config_dir, logger):
    for pid in pids:
        if not pid in task_manager_dict:
            task_manager_dict[pid] = TaskManager(pid, config_dir)
            if logger:
                label = task_manager_dict[pid].label
                logger.info("created task {0} with pid {1}".format(label, pid))

def update_task_manager_data(task_manager_dict, logger):
    for pid, task_manager in task_manager_dict.items():
        status = task_manager.update_data()
        if status is 'finished':
            label = task_manager_dict[pid].label
            if logger:
                logger.info("deleting task {0} with pid {1}".format(label, pid))
            del task_manager_dict[pid]

def get_pids_for_identifier(identifier):
    pid_list = []
    for pid in psutil.pids():
        if any(identifier in item for item in psutil.Process(pid).cmdline()):
            pid_list.append(pid)
    return pid_list
