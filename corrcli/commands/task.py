"""Manipulate task data in the file store

"""

import json

import click
import pandas

from .cli import cli
from ..stores.file_store import FileStore


@cli.group()
def task():
    """Manipulate task data in the file store
    """

@task.command('list')
@click.option('--number', '-n', type=int, default=None, help="The number of task records to list")
@click.argument('task_ids', nargs=-1)
@click.pass_context
def list_tasks(ctx, number, task_ids):
    """List tasks in the file data store.
    """
    config_dir = ctx.parent.parent.params['config_dir']

    if len(task_ids) == 0:
        list_task_df(config_dir, number)
    else:
        list_task_json(task_ids, config_dir, number)

@task.command()
@click.option('--force/--no-force', '-f', default=False, help="Whether to promt when removing task records.")
@click.argument('task_ids', nargs=-1)
@click.pass_context
def remove(ctx, force, task_ids):
    """Remove tasks in the file data store.
    """
    config_dir = ctx.parent.parent.params['config_dir']
    long_ids = FileStore.get_long_labels(config_dir, task_ids)
    for task_id in task_ids:
        long_id = long_ids.get(task_id)
        if long_id:
            if force or click.confirm("Remove task {0} from the file data store?".format(long_id[:8])):
                FileStore(long_id, config_dir).remove()
                click.echo("Task {0} removed.".format(long_id[:8]))
        else:
            click.echo("No such task as {0}.".format(task_id))


def list_task_df(config_dir, number):
    """Print a condensed version of the task data frame.

    Args:
      config_dir: the CoRR configuration directory
      number: the number of most recent tasks to print

    """
    tasks_df = pandas.DataFrame(FileStore.read_all(config_dir))
    tasks_df['process_id'] = tasks_df['process_id'].where(~tasks_df['process_id'].isnull(), -1)
    tasks_df['process_id'] = tasks_df['process_id'].astype(int)
    pandas.options.mode.chained_assignment = None
    columns = ['label', 'status', 'created_time', 'process_id']

    def datetime_func(item):
        if not pandas.isnull(item):
            return pandas.to_datetime(item).strftime("%y-%m-%d %H:%M:%S")
        else:
            return item

    formatters = {'label' : lambda item: item[:8],
                  'created_time' : datetime_func}
    rename = {'created_time' : 'time stamp',
              'process_id' : 'pid'}
    reduced_df = tasks_df[columns]
    for column in columns:
        if column in formatters:
            reduced_df[column] = reduced_df[column].apply(formatters[column])
    reduced_df.rename(columns=rename, inplace=True)
    reduced_df.sort_values(by='time stamp', ascending=False, inplace=True)
    reduced_df.reset_index(drop=True, inplace=True)
    click.echo(reduced_df[:number])

def list_task_json(task_ids, config_dir, number):
    """Print the JSON for a list of shortend task IDs.

    Args:
      task_ids: a list of short task IDs
      config_dir: the CoRR configuration directory
      number: the number of tasks to print

    """
    long_ids = FileStore.get_long_labels(config_dir, task_ids)
    for task_id in task_ids:
        long_id = long_ids.get(task_id)
        if long_id:
            task_dict = FileStore(long_id, config_dir).read()
            click.echo(json.dumps(task_dict, indent=2, sort_keys=True))
        else:
            click.echo("No such task as {0}.".format(task_id))
