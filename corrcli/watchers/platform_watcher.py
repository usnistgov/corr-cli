"""Gather data about the platform.
"""
import platform
from .watcher import Watcher


class PlatformWatcher(Watcher):
    """Gather data about the platform

    >>> keys = list(PlatformWatcher(None).watch().keys())
    >>> keys.sort()
    >>> print(keys)
    ['node_name', 'platform']

    Attributes:
      pid: the process ID to watch
      schema_dict: mapping from the observed data to the output data
      watch_dict: the cached observed data

    """
    schema_dict = {'node_name' : 'node',
                   'platform' : 'platform'}

    def __init__(self, pid):
        super(PlatformWatcher, self).__init__(pid)
        self.observed_dict = {}
        for value in self.schema_dict.values():
            self.observed_dict[value] = getattr(platform, value)()

    def get_observed_dict(self):
        return self.observed_dict

    def watch(self, data_dict=None):
        observed_dict = self.get_observed_dict()
        data_dict = self.ini_data_dict(data_dict)
        return self.update_data_dict(observed_dict, data_dict)
