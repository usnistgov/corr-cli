"""Base corrcli command for all subcommands.
"""
import os
import click
from ..tools import get_version
from ..tools import get_config_dir

DEFAULT_CONFIG_FILE = 'config.ini'
DEFAULT_WATCHER_DIR = 'watchers'
DEFAULT_JOB_DIR = 'jobs'
DEFAULT_WRITE_REFRESH_RATE = 5.0
DEFAULT_WATCH_REFRESH_RATE = 0.1

@click.group()
@click.version_option(get_version())
@click.option('--config-dir',
              'config_dir',
              default=None,
              help="Set the config directory for CoRR-cli.",
              type=click.Path())
@click.pass_context
def cli(ctx, config_dir):
    """The CoRR command line tool.
    """
    if config_dir is None:
        config_dir = get_config_dir('corrcli')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            click.echo('Creating config directory {0}.'.format(config_dir))
    else:
        if not os.path.exists(config_dir):
            click.echo('Config directory {0} does not exist'.format(config_dir))
            ctx.exit()
    ctx.params['config_dir'] = os.path.expanduser(os.path.abspath(config_dir))
