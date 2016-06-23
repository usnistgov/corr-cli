"""Watcher that uses psutil to gather proces data.


"""
import psutil

class ProcessWatcher(object):
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
    memory_parse = lambda process_dict, data_dict_old: \
                   max(int(process_dict['memory_info'].rss), data_dict_old.get('memory', 0.))

    schema_dict = {'process_name' : 'name',
                   'executable' : 'exe',
                   'process_created' : 'create_time',
                   'cwd' : 'cwd',
                   'memory' : memory_parse,
                   'username' : 'username',
                   'status' : 'status',
                   'cmdline' : 'cmdline'}

    def __init__(self, pid):
        """Instantiate a ProcessWatcher.

        Args:
          pid: the process ID to watch
        """
        self.pid = pid

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

        if data_dict is None:
            data_dict = dict()
        data_dict_old = data_dict.copy()
        for key in self.schema_dict.keys():
            data_dict[key] = data_dict.get(key, None)

        if watch_dict is not None:
            for key, value in self.schema_dict.items():
                if isinstance(value, str):
                    data_dict[key] = watch_dict[value]
                else:
                    data_dict[key] = value(watch_dict, data_dict_old)
            return data_dict
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
