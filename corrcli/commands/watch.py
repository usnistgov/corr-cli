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
import daemon
from corrcli.watcher_deamon import WatcherDaemon


@corrcli.cli.command()
@click.option('--list', help="list all the exisiting watcher deamons", is_flag=True)
def watch(list):
    """Launch a deamon process for watching processes.
    """
    if list:
        click.echo(WatcherDaemon.get_daemon_dataframe())

@watch.command()
def start():
    watcher = WatcherDaemon()
    watcher.run()
    click.echo(watcher.tag)

@watch.command()
@click.option('--all', is_flag=True, help="Stop all watcher daemons.")
@click.option('--tag', 'tags', multiple=True, help="Stop the given daeomon corresping to [tag]")
def stop(all, tags):
    if all:
        click.echo(WatcherDaemon.stop_all())
    for tag in tags:
        click.echo(WatcherDaemon.stop(tag))
