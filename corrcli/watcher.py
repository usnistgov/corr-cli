"""The Watcher class used to launch a daemon process.
"""
import uuid
import logging
import os
import glob
import signal
from subprocess import Popen
from time import sleep
from contextlib import contextmanager

import pandas
import daemon
import daemon.pidfile

from .commands.cli import DEFAULT_WATCHER_DIR


class Watcher(object):
    """Launch a callback function as a daemon process.

    Multiple `Watcher`s can launch multiple callback functions as
    daemon processes and keep track of running watchers as well as
    shutdown watchers.

    Attributes:
      watcher_id: a unique ID for each watcher
      watcher_dir: the directory for pid and log files
      logging_on: whether the watcher should log its output
      log_file: the path to the deaemon's log file
      callback: the callback function that's executed in the watcher
      pidext: the extension for pid files

    Note that a possible alternative to this class might be
    http://python-service.readthedocs.io/en/latest/.

    """
    pidext = 'pid'
    def __init__(self, callback, config_dir, watcher_on, logging_on=False):
        """Instantiate a `Watcher`.

        Args:
          callback: the callback function that's executed in the
            watcher
          config_dir: the CoRR config directory
          logging_on: whether the watcher should log its output

        """
        self.watcher_id = str(uuid.uuid4().hex)[:12]
        self.watcher_dir = self.get_watcher_dir(config_dir)
        if not os.path.exists(self.watcher_dir):
            os.makedirs(self.watcher_dir)
        self.logging_on = logging_on
        self.log_file = os.path.join(self.watcher_dir, '{0}.log'.format(self.watcher_id))
        self.callback = callback
        self.config_dir = config_dir
        self.watcher_on = watcher_on

    @staticmethod
    def get_watcher_dir(config_dir):
        """Get the watcher directory.

        Args:
          config_dir: the CoRR config directory

        Returns:
          A path like `/home/user/.config/corrcli/watchers`.
        """
        return os.path.join(config_dir, DEFAULT_WATCHER_DIR)

    def get_pidfile(self):
        """Get the PID file for the watcher process.

        The file is named something like
        `e6f14ae7-efef-435e-b9ce-db04982afc5c.pid`.

        Returns:
           a PIDLockFile instance
        """
        lock_file = os.path.join(self.watcher_dir,
                                 '{0}.{1}'.format(self.watcher_id, self.pidext))
        return daemon.pidfile.PIDLockFile(lock_file)

    def get_logger(self):
        """Get the logger for logging the deamon process.

        Returns:
          a tuple containing the logger and the file handler
        """
        logger = logging.getLogger("CoRRWatcher Log -- {0}".format(self.watcher_id))
        logger.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger, handler

    def start(self):
        """Start a process and detach as a daemon.
        """
        files_preserve = []
        logger = None
        if self.logging_on:
            logger, handler = self.get_logger()
            files_preserve.append(handler.stream)

        daemon_context = daemon.DaemonContext(pidfile=self.get_pidfile(),
                                              files_preserve=files_preserve)
        if self.watcher_on:
            with daemon_context:
                self._run(logger, daemon_context)
        else:
            self._run(logger, daemon_context)

    @classmethod
    def stop(cls, config_dir, watcher_ids=(), all_watchers=False):
        """Stop watcher processes base on watcher_ids.

        Args:
          config_dir: the CoRR config directory
          watcher_ids: the watcher IDs to stop
          all_watchers: shut down all watchers

        Returns:
          a data frame containing the watcher IDs and PIDs for all
          watchers shutdown

        """
        watcher_df = cls.list(config_dir)
        if all_watchers:
            rows_df = watcher_df
        else:
            rows_df = watcher_df.loc[watcher_df['watcher_id'].isin(watcher_ids)]

        for _, row in rows_df.iterrows():
            os.kill(row.process_id, signal.SIGTERM)

        return rows_df

    @classmethod
    def list(cls, config_dir):
        """List all running watchers.

        Args:
          config_dir: the CoRR config directory

        Returns:
          a data frame containing the deamon IDs and PIDs for all
          running watchers
        """
        watcher_dir = cls.get_watcher_dir(config_dir)
        pidfile_regex = os.path.join(watcher_dir, '*.{0}'.format(cls.pidext))
        watcher_ids = []
        pids = []
        for pidfile in glob.glob(pidfile_regex):
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
        try:
            self.callback(self.watcher_id, self.config_dir, logger=logger)
        except Exception:
            if logger:
                logger.exception("Exception in watcher callback function.")
            raise

        if logger:
            logger.info("Stop watcher with pid {0}".format(pid))


@contextmanager
def start_watcher(config_dir, callback_func=None):
    """CoRR Watcher context manager.

    Only used for tests.

    Args:
      config_dir: the CoRR configuration directory
      callback_func: the name of the callback function

    Yields:
      the watcher ID

    """
    watcher_ids_before = set(Watcher.list(config_dir).watcher_id)
    process_ids_before = set(Watcher.list(config_dir).watcher_id)
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'start',
                 '--log']
    if callback_func is not None:
        arguments.append('--callback-func={0}'.format(callback_func))
    Popen(arguments).communicate()
    sleep(1)
    watcher_id = (set(Watcher.list(config_dir).watcher_id) - watcher_ids_before).pop()
    process_id = (set(Watcher.list(config_dir).process_id) - process_ids_before).pop()
    yield watcher_id, process_id
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'stop',
                 '{0}'.format(watcher_id)]
    Popen(arguments).communicate()
