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

def TaskWatcher(object):
    def __init__(self, identifier):
        self.identifier = identifier


    def watch(self):
        pids =
        psutils_process = psutil.Process(self.pid)
        import ipdb; ipdb.set_trace()
        return None


def task_watcher(identifier, logger=None):
    watcher = TaskWatcher(identifier)
    while True:
        watcher.update()
