"""Manipulate task data in the file store

"""

import click
import pandas

from .cli import cli
from ..stores.file_store import FileStore


@cli.group()
def task():
    """Manipulate task data in the file store
    """

@task.command('list')
@click.pass_context
def list_tasks(ctx):
    """List tasks in the file data store.
    """
    config_dir = ctx.parent.parent.params['config_dir']
    tasks_df = pandas.DataFrame(FileStore.read_all(config_dir))

    pandas.options.mode.chained_assignment = None
    columns = ['label', 'status', 'update_time', 'process_id']
    datetime_func = lambda item: pandas.to_datetime(item).strftime("%y-%m-%d %H:%M:%S")
    formatters = {'label' : lambda item: item[:8],
                  'update_time' : datetime_func}
    rename = {'update_time' : 'time stamp',
              'process_id' : 'pid'}
    out_df = tasks_df[columns]
    for column in columns:
        if column in formatters:
            out_df[column] = out_df[column].apply(formatters[column])
    out_df = out_df.rename(columns=rename).sort_values(by='time stamp', ascending=False)
    click.echo(out_df)
