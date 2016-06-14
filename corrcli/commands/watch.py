"""The watch command for corrcli.

Launch a deamon that will watch for command line programs launched
with the given ID.

    $ corrcli watch start
    [ID]

Stop the deamon.

    $ corrcli watch stop [ID]

"""

import click
from ..watcher import Watcher
from .cli import cli


@cli.group()
def watch():
    """Launch a deamon for watching other processes.
    """

@watch.command()
@click.option('--log/--no-log', default=False, help="Whether to record the output of the watcher daemon")
@click.option('--refresh-rate', 'refresh_rate', default=10.0, help="Frequency that watcher should check for processes.")
def start(log, refresh_rate):
    """Launch a Daemon to watch processes.
    """

    watcher = Watcher(logging_on=log, refresh_rate=refresh_rate)
    click.echo("Launch daemon with ID: {0}".format(watcher.watcher_id))
    if log:
        click.echo("Writing logs to {0}".format(watcher.log_file))
    watcher.start()

@watch.command()
@click.option('--all', is_flag=True, help="Stop all watcher daemons.")
@click.option('--watcher-id', 'watcher_ids', multiple=True, help="Stop the given daeomon corresping to [tag]")
def stop(all, watcher_ids):
    """Shut down watching daemons.
    """
    if (not all) and len(watcher_ids) == 0:
        click.echo("Require a watcher ID to proceed.")
    else:
        click.echo("Stopping watchers.")
        stopped_df = Watcher.stop(watcher_ids=watcher_ids, all=all)
        for index, row in stopped_df.iterrows():
            click.echo("Stopped {0} with pid {1}".format(row.watcher_id, row.process_id))

@watch.command()
def list():
    """List all daemons.
    """
    watcher_df = Watcher.list()
    if len(watcher_df) == 0:
        click.echo("No running daemons.")
    else:
        click.echo(watcher_df.to_string(index=False))
