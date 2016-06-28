"""Miscellaneous functions for corr-cli.
"""
from subprocess import Popen
from time import sleep
import os

import click


def get_version():
    """Get the version of the code from egg_info.

    Returns:
      the package version number
    """
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__.split('.')[0]).version # pylint: disable=no-member
    except DistributionNotFound: # pragma: no cover
        version = "unknown, try running `python setup.py egg_info`"

    return version

def get_config_dir(app_name): # pragma: no cover
    """Get the path to CoRR's config directory

    The path is platform independent.

    Args:
      app_name: name of the app

    Returns:
      the path to the config directory
    """
    config_dir = click.get_app_dir(app_name)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir

def start_daemon(config_dir, callback_func=None):
    """Start a daemon from a separate process.

    Args:
      config_dir: the CoRR configuration directory
      callback_func: the name of the callback function
    """
    arguments = ['corrcli',
                 '--config-dir={0}'.format(config_dir),
                 'watch',
                 'start',
                 '--log']
    if callback_func is not None:
        arguments.append('--callback-func={0}'.format(callback_func))
    Popen(arguments)
    sleep(3)
