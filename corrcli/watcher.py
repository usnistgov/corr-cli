import daemon
import uuid
from time import sleep
import logging
import daemon.pidfile
from corrcli import default_config_dir
import os
import glob
import pandas
import signal


class Watcher(object):
    """Possible alternative to this class could be
    http://python-service.readthedocs.io/en/latest/.

    """
    pidext = 'pid'
    def __init__(self, refresh_rate=10.0, config_dir=None, watcher_id=None, logging_on=False):
        if watcher_id is None:
            watcher_id = uuid.uuid4()
        self.watcher_id = watcher_id
        self.refresh_rate = refresh_rate
        self.daemon_dir = self.get_daemon_dir(config_dir)
        if not os.path.exists(self.daemon_dir):
            os.makedirs(self.daemon_dir)
        self.logging_on = logging_on
        self.log_file = os.path.join(self.daemon_dir, '{0}_daemon.log'.format(self.watcher_id))

    @staticmethod
    def get_daemon_dir(config_dir):
        if config_dir is None:
            config_dir = default_config_dir
        return os.path.join(config_dir, 'corr_daemons')

    def get_pidfile(self):
        lock_file = os.path.join(self.daemon_dir,
                                 '{0}.{1}'.format(self.watcher_id, self.pidext))
        return daemon.pidfile.PIDLockFile(lock_file)

    def get_logger(self):
        logger = logging.getLogger("CoRR Watcher Log -- {0}".format(self.watcher_id))
        logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger, handler

    def start(self):
        files_preserve = []
        logger = None
        if self.logging_on:
            logger, handler = self.get_logger()
            files_preserve.append(handler.stream)

        daemon_context = daemon.DaemonContext(pidfile=self.get_pidfile(),
                                              files_preserve=files_preserve)
        with daemon_context:
            self.run(logger, daemon_context)

    @classmethod
    def stop(cls, watcher_ids=[], config_dir=None, all=True):
        watcher_df = cls.list(config_dir=config_dir)
        if all:
            rows_df = watcher_df
        else:
            rows_df = watcher_df.loc[watcher_df['watcher_id'].isin(watcher_ids)]
        if len(rows_df) == 0:
            raise RuntimeError('No processes found with watcher ids in {0}'.format(watcher_ids))

        for index, row in rows_df.iterrows():
            os.kill(row.process_id, signal.SIGTERM)

        return rows_df

    @classmethod
    def list(cls, config_dir=None):
        daemon_dir = cls.get_daemon_dir(config_dir)
        pidfile_exp = os.path.join(daemon_dir, '*.{0}'.format(cls.pidext))
        watcher_ids = []
        pids = []
        for pidfile in glob.glob(pidfile_exp):
            with open(pidfile, 'r') as fpointer:
                pids.append(int(fpointer.read()))
            watcher_id = os.path.splitext(os.path.split(pidfile)[1])[0]
            watcher_ids.append(watcher_id)
        return pandas.DataFrame({'watcher_id' : watcher_ids,
                                 'process_id' : pids})


    def run(self, logger, context):
        while True:
            if logger:
                logger.info('Refresh watcher with pid {1}'.format(self.watcher_id, context.pidfile.read_pid()))
            sleep(self.refresh_rate)
