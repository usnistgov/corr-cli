"""The watch command for corrcli.

Launch a deamon that will watch for command line programs launched
with the given tag.

    $ corrcli watch start
    [tag]

Stop the deamon.

    $ corrcli watch stop [tag]

"""

import click
from ..watcher import Watcher
from .cli import cli


@cli.group()
def watch():
    """Launch a deamon process for watching processes.
    """

@watch.command()
def start():
    """Launch a Daemon to watch processes.
    """

    watcher = Watcher()
    click.echo(watcher.tag)
    watcher.start()

@watch.command()
@click.option('--all', is_flag=True, help="Stop all watcher daemons.")
@click.option('--tag', 'tags', multiple=True, help="Stop the given daeomon corresping to [tag]")
def stop(all, tags):
    """Shut down watching daemons.
    """
    if all:
        click.echo(Watcher.stop_all())
    for tag in tags:
        click.echo(Watcher.stop(tag))

@watch.command()
def clean():
    """Remove all defunct dead wathcher from list.
    """
    click.echo(Watcher.clean())

@watch.command()
def list():
    """List all daemons.
    """
    click.echo(Watcher.list())
