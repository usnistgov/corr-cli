import click
from ..tools import get_version

@click.group()
@click.version_option(get_version())
def cli():
    """The CoRR command line tool.
    """
