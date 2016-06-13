import daemon
import uuid
from time import sleep

http://www.gavinj.net/2012/06/building-python-daemon-process.html
class Watcher(object):
    def __init__(self, refresh=10.0):
        self.tag = uuid.uuid4()
        self.refresh = refresh
        self.pid = None

    def start(self):
        with daemon.DaemonContext():
            self.run()

    def stop(self):
        pass

    @staticmethod
    def list():
        pass

    @staticmethod
    def clean():
        pass

    def run():
        while True:
            # print("Running watcher with tag {0} and pid {1}".format(self.tag, self.pid))
            print('hi')
            sleep(10.0)
