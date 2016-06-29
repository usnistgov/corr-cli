"""Base corrcli command for all subcommands.
"""
import os
import click
from ..tools import get_version
from ..tools import get_config_dir

DEFAULT_CONFIG_FILE = 'config.ini'
DEFAULT_DAEMON_DIR = 'daemons'
DEFAULT_TASK_DIR = 'tasks'
DEFAULT_WRITE_REFRESH_RATE = 5.0
DEFAULT_WATCH_REFRESH_RATE = 0.1

@click.group()
@click.version_option(get_version())
@click.option('--config-dir',
              'config_dir',
              default=get_config_dir('corrcli'),
              help="Set the config directory for CoRR.",
              type=click.Path())
@click.pass_context
def cli(ctx, config_dir):
    """The CoRR command line tool.
    """
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    ctx.params['config_dir'] = os.path.abspath(config_dir)
