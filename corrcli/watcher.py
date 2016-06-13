import daemon
import uuid


class Watcher(object):
    def __init__(self):
        self.tag = uuid.uuid4()

    def run(self):
        with daemon.DaemonContext():
            self._run()

    def start(self):
        pass

    def stop(self):
        pass

    def get_all(self):
        pass

    def clean(self):
        pass
