import daemon
import uuid
import logging
import daemon.pidfile
import os
import glob
import pandas
import signal


class Watcher(object):
    """Possible alternative to this class could be
    http://python-service.readthedocs.io/en/latest/.

    """
    pidext = 'pid'
    def __init__(self, callback, config_dir, logging_on=False):
        self.watcher_id = uuid.uuid4()
        self.daemon_dir = self.get_daemon_dir(config_dir)
        if not os.path.exists(self.daemon_dir):
            os.makedirs(self.daemon_dir)
        self.logging_on = logging_on
        self.log_file = os.path.join(self.daemon_dir, '{0}_daemon.log'.format(self.watcher_id))
        self.callback = callback

    @staticmethod
    def get_daemon_dir(config_dir):
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
            self._run(logger, daemon_context)

    @classmethod
    def stop(cls, config_dir, watcher_ids=[], all=False):
        watcher_df = cls.list(config_dir)
        if all:
            rows_df = watcher_df
        else:
            rows_df = watcher_df.loc[watcher_df['watcher_id'].isin(watcher_ids)]

        for index, row in rows_df.iterrows():
            os.kill(row.process_id, signal.SIGTERM)

        return rows_df

    @classmethod
    def list(cls, config_dir):
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


    def _run(self, logger, context):
        pid = context.pidfile.read_pid()
        if logger:
            logger.info("Start watcher with pid {0}".format(pid))
        self.callback(logger=logger)
        if logger:
            logger.info("Stop watcher with pid {1}".format(pid))
