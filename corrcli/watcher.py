import daemon
# import daemon.pidlockfile
import uuid
from time import sleep
import logging
import daemon.pidfile
import corrcli
from .tools import get_config_dir
import os


class Watcher(object):
    def __init__(self, refresh=10.0, config_dir=None, tag=None, logging=True):
        if tag is None:
            tag = uuid.uuid4()
        self.tag = tag
        self.refresh = refresh
        self.logging = logging
        if config_dir is None:
            config_dir = get_config_dir(corrcli)
        self.daemon_dir = os.path.join(config_dir, 'corr_daemons')
        if not os.path.exists(self.daemon_dir):
            os.makedirs(self.daemon_dir)

    def get_pidfile(self):
        lock_file = os.path.join(self.daemon_dir,
                                 '{0}.pid'.format(self.tag))
        return daemon.pidfile.PIDLockFile(lock_file)

    def get_logger(self):
        logger = logging.getLogger("DaemonLog")
        logger.setLevel(logging.INFO)
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        log_file = os.path.join(self.daemon_dir, '{0}_daemon.log'.format(self.tag))
        handler = logging.FileHandler(log_file)
        logger.addHandler(handler)
        return logger, handler

    def start(self):

        logger, handler = self.get_logger()
        daemon_context = daemon.DaemonContext(pidfile=self.get_pidfile(),
                                              files_preserve=[handler.stream])
        with daemon_context:
            self.run(logger, daemon_context)

    def stop(self):
        pass

    @staticmethod
    def list():
        pass

    @staticmethod
    def clean():
        pass

    def run(self, logger, context):
        while True:
            # print("Running watcher with tag {0} and pid {1}".format(self.tag, self.pid))
            logger.info('Running {0} and pid {1}'.format(self.tag, context.pidfile))
            sleep(10.0)

# import logging
# import daemon
# import daemon.pidlockfile
# import sys

# logger = logging.getLogger("DaemonLog")
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter(
# "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# handler = logging.FileHandler("log.file")
# logger.addHandler(handler)

# pid = daemon.pidlockfile.TimeoutPIDLockFile(
# "/tmp/dizazzo-daemontest.pid", 10)

# daemon_context = daemon.DaemonContext(
# pidfile=pid,
# files_preserve=[handler.stream])

# with daemon_context:
# logger.info("POO")
