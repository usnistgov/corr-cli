import platform

class PlatformWatcher(object):
    schema = {'name' : 'node',
              'platform' ; 'platform'}

    def watch(self):
        return dict((key, getattr(platform, value)()) for key, value in self.schema)
