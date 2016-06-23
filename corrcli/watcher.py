import abc


class Watcher(object):
    __metaclass__ = abc.ABCMeta
    schema_dict = {}
    def __init__(self, pid):
        """Instantiate a ProcessWatcher.

        Args:
          pid: the process ID to watch
        """
        self.pid = pid

    @abc.abstractmethod
    def watch(self, data_dict=None):
        pass

    @abc.abstractmethod
    def get_watch_dict(self):
        pass

    def ini_data_dict(self, data_dict):
        if data_dict is None:
            data_dict = dict()
        for key in self.schema_dict.keys():
            data_dict[key] = data_dict.get(key, None)
        return data_dict

    def update_data_dict(self, watch_dict, data_dict):
        for key, value in self.schema_dict.items():
            if isinstance(value, str):
                data_dict[key] = watch_dict[value]
            else:
                func = value
                data_dict[key] = func(watch_dict, data_dict)
        return data_dict
