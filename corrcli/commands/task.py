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

def list_task_df(config_dir, number):
    tasks_df = pandas.DataFrame(FileStore.read_all(config_dir))
    pandas.options.mode.chained_assignment = None
    columns = ['label', 'status', 'created_time', 'process_id']
    datetime_func = lambda item: pandas.to_datetime(item).strftime("%y-%m-%d %H:%M:%S")
    formatters = {'label' : lambda item: item[:8],
                  'created_time' : datetime_func}
    rename = {'created_time' : 'time stamp',
              'process_id' : 'pid'}
    out_df = tasks_df[columns]
    for column in columns:
        if column in formatters:
            out_df[column] = out_df[column].apply(formatters[column])
    out_df = out_df.rename(columns=rename).sort_values(by='time stamp', ascending=False).reset_index(drop=True)
    click.echo(out_df[:number])

def list_task_json(task_ids, config_dir, number):
    all_tasks = FileStore.read_all(config_dir)
    min_len = min([len(task_id) for task_id in task_ids])
    task_dict = {task_['label'][:min_len] : task_ for task_ in all_tasks}
    for task_id in task_ids[:number]:
        click.echo(json.dumps(task_dict[task_id], indent=2, sort_keys=True))
