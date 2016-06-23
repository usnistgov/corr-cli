"""Watcher that uses psutil to gather proces data.


"""
import psutil
from .watcher import Watcher

class ProcessWatcher(Watcher):
    """Watcher that uses psutil to gather data.

    A process is returned with 'status' finished if it can't be found.

    >>> large_int = 100000000000000
    >>> watcher = ProcessWatcher(large_int)
    >>> print(watcher.watch()['status'])
    finished

    Attributes:
      pid: the process ID to watch
      schema_dict: the mapping from psutil to the CoRR schema

    """
    memory_parse = lambda process_dict, data_dict: \
                   max(int(process_dict['memory_info'].rss), data_dict['memory'] or 0)

    schema_dict = {'process_name' : 'name',
                   'executable' : 'exe',
                   'process_created' : 'create_time',
                   'cwd' : 'cwd',
                   'memory' : memory_parse,
                   'username' : 'username',
                   'status' : 'status',
                   'cmdline' : 'cmdline'}


    def watch(self, data_dict=None):
        """Gather data about a process.

        Data is updated based what would intuitvely be the most useful
        to record. For example, 'memory' is calculated from the max
        value of the data passed in and the new data. However,
        'status' is the latest value. The 'status' is changed to
        'finished' in the evernt that the process is not in the
        process table (when psutil.NoSuchProcess is raised).

        Args:
          data_dict: the dictionary to update

        Returns:
          an updated data_dict

        """
        watch_dict = self.get_watch_dict()
        data_dict = self.ini_data_dict(data_dict)
        if watch_dict is not None:
            return self.update_data_dict(watch_dict, data_dict)
        else:
            data_dict['status'] = 'finished'
            return data_dict

    def get_watch_dict(self):
        """Get the dict for the watcher.

        The format is that of the psutil module.

        Returns:
          a psutil.Process as a dict
        """
        try:
            process = psutil.Process(self.pid)
            value_dict = process.as_dict()
        except psutil.NoSuchProcess:
            value_dict = None
        return value_dict
