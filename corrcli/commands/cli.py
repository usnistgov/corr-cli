import click
from ..tools import get_version
from corrcli import default_config_dir
import os


@click.group()
@click.version_option(get_version())
@click.option('--config-dir',
              'config_dir',
              default=default_config_dir,
              help="Set the config directory for CoRR.",
              type=str)
@click.pass_context
def cli(ctx, config_dir):
    """The CoRR command line tool.
    """
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    ctx.params['config_dir'] = os.path.abspath(config_dir)
