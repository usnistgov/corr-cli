"""
---
corr:
  - label
  - comment
  - parameters
platform:
  - machine
  - processor
psutil:
  - name
  - exe
  - cwd
  - cmdline
  - status
  - username
  - create_time
  - memory_info
    - rss
"""
import datetime
from .pid_watcher import PIDWatcher
from .platform_watcher import PlatformWatcher



def TaskManager(object):
    def __init__(self, pid, config_dir):
        self.pid_watcher = PIDWatcher(pid)
        self.platform_data = PlatformWatcher().watch()
        self.datafile = datafile
        self.initialize_data()

    def initialize_data(self):
        task_data = {'label' : uuid.uuid4(),
                     'last_update' : str(datetime.datetime.now())}
        pid_data = {'process' : {'status' : None}}

    def update_data(self):
        data = self.read_data()
        pid_data = self.pid_watcher.watch()
        task_data = {'label' : self.task_id,
                     'update time' : str(datetime.datetime.now())}
        if pid_data:
            data = {'process' : pid_data,
                    'task' : task_data,
                    'platform' : platform_data}
        else:
            if data:
                data['process']['status'] = None
            else:
                data = {'task', task_data,
                        'process', process_data}

    def write_data(self):
        pass

    def read_data(self):
        pass





def task_watcher_control(daemon_id, logger=None):

    watcher = TaskWatcher(identifier)
    while True:
        watcher.update()
