"""The watch command for corrcli.

Launch a deamon that will watch for command line programs launched
with the given tag.

    $ corrcli watch start
    [tag]

Stop the deamon.

    $ corrcli watch stop [tag]

"""

import click
import corrcli
from corrcli.watcher import Watcher


@corrcli.cli.command()
@click.option('--list', help="list all the exisiting watcher deamons", is_flag=True)
def watch(list):
    """Launch a deamon process for watching processes.
    """
    if list:
        click.echo(Watcher.get_all())

@watch.command()
def start():
    """Launch a Daemon to watch processes.
    """
    watcher = Watcher()
    watcher.run()
    click.echo(watcher.tag)

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
    """Remove
    """
    click.echo(Watcher.clean())
