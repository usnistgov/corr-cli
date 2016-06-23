import platform
from .watcher import Watcher


class PlatformWatcher(Watcher):
    schema_dict = {'node_name' : 'node',
                   'platform' : 'platform'}

    def __init__(self, pid):
        super(PlatformWatcher, self).__init__(pid)
        self.watch_dict = {}
        for value in self.schema_dict.values():
            self.watch_dict[value] = getattr(platform, value)()

    def get_watch_dict(self):
        return self.watch_dict

    def watch(self, data_dict=None):
        watch_dict = self.get_watch_dict()
        data_dict = self.ini_data_dict(data_dict)
        return self.update_data_dict(watch_dict, data_dict)
