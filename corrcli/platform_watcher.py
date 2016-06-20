import platform

class PlatformWatcher(object):
    schema = {'node_name' : 'node',
              'platform' : 'platform'}

    def watch(self, data_dict=dict()):
        for key, value in self.schema.items():
            data_dict[key] = getattr(platform, value)()
        return data_dict
