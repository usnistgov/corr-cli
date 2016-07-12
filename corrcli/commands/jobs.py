"""Manipulate job data in the file store

"""

import json

import click
import pandas

from .cli import cli
from ..stores.file_store import FileStore


@cli.group()
def jobs():
    """Manipulate job data in the file store
    """

@jobs.command('list')
@click.option('--number', '-n', type=int, default=None, help="The number of job records to list")
@click.argument('job_ids', nargs=-1)
@click.pass_context
def list_jobs(ctx, number, job_ids):
    """List jobs in the file data store.
    """
    config_dir = ctx.parent.parent.params['config_dir']

    if len(job_ids) == 0:
        list_job_df(config_dir, number)
    else:
        list_job_json(job_ids, config_dir, number)

@jobs.command()
@click.option('--force/--no-force',
              '-f',
              default=False,
              help="Whether to promt when removing job records.")
@click.argument('job_ids', nargs=-1)
@click.pass_context
def remove(ctx, force, job_ids):
    """Remove jobs in the file data store.
    """
    config_dir = ctx.parent.parent.params['config_dir']
    long_ids = FileStore.get_long_labels(config_dir, job_ids)
    for job_id in job_ids:
        long_id = long_ids.get(job_id)
        if long_id:
            confirm_string = "Remove job {0} from the file data store?".format(long_id[:8])
            if force or click.confirm(confirm_string):
                FileStore(long_id, config_dir).remove()
                click.echo("Job {0} removed.".format(long_id[:8]))
        else:
            click.echo("No such job as {0}.".format(job_id))

def datetime_func(item):
    """Reformat a datatime string.

    Turn a datatime string into a Pandas datetime object and then
    reformat if not a null object.

    >>> print(datetime_func('2016-06-25 21:53:19.71829'))
    2016-06-25 21:53:19
    >>> print(datetime_func(None))
    None

    Args:
      item: a datetime string or null object

    Returns:
      a reformatted datatime string

    """
    if not pandas.isnull(item):
        return pandas.to_datetime(item).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return item

def list_job_df(config_dir, number):
    """Print a condensed version of the job data frame.

    Args:
      config_dir: the CoRR configuration directory
      number: the number of most recent jobs to print

    Test with no jobs.

    >>> from click.testing import CliRunner
    >>> with CliRunner().isolated_filesystem() as config_dir:
    ...     list_job_df(config_dir, 10)
    No jobs in file data store

    """
    jobs_df = pandas.DataFrame(FileStore.read_all(config_dir))
    columns = ['label', 'status', 'created_time', 'process_id']
    if len(jobs_df) == 0:
        for column in columns:
            jobs_df[column] = []
    jobs_df['process_id'] = jobs_df['process_id'].where(~jobs_df['process_id'].isnull(), -1)
    jobs_df['process_id'] = jobs_df['process_id'].astype(int)
    pandas.options.mode.chained_assignment = None

    formatters = {'label' : lambda item: item[:8],
                  'created_time' : datetime_func}
    rename = {'created_time' : 'time stamp',
              'process_id' : 'pid'}
    reduced_df = jobs_df[columns]
    for column in columns:
        if column in formatters:
            reduced_df[column] = reduced_df[column].apply(formatters[column])
    reduced_df.rename(columns=rename, inplace=True)
    reduced_df.sort_values(by='time stamp', ascending=False, inplace=True)
    reduced_df.reset_index(drop=True, inplace=True)
    reduced_df.set_index('label', inplace=True)
    if len(jobs_df) == 0:
        click.echo("No jobs in file data store")
    else:
        click.echo(reduced_df[:number])

def list_job_json(job_ids, config_dir, number):
    """Print the JSON for a list of shortend job IDs.

    Args:
      job_ids: a list of short job IDs
      config_dir: the CoRR configuration directory
      number: the number of jobs to print

    """
    long_ids = FileStore.get_long_labels(config_dir, job_ids)
    for job_id in job_ids[:number]:
        long_id = long_ids.get(job_id)
        if long_id:
            job_dict = FileStore(long_id, config_dir).read()
            click.echo(json.dumps(job_dict, indent=2, sort_keys=True))
        else:
            click.echo("No such job as {0}.".format(job_id))
