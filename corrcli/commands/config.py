import inspect
import corrcli
from corrcli import __version__
import os
from configparser import ConfigParser
import click


@click.group()
@click.version_option(__version__)
def cli():
    """The CoRR command line tool.
    """


@cli.command()
@click.option('--email', default=None, help="Add email address.", type=str)
@click.option('--name', default=None, help="Add email address.", type=str)
@click.option('--url', default=None, help="Set the remote API url", type=str)
@click.option('--port', default=None, help="Set the remote API port", type=str)
def config(email, name, url, port):
    entries = [('default', 'email', email),
               ('default', 'name', name),
               ('api', 'url', url),
               ('api', 'port', port)]

    for section, key, value in entries:
        if value:
            write_item(section, key, value)


def get_config_path():
    app_name = dict(inspect.getmembers(corrcli))['__name__']
    config_dir = click.get_app_dir(app_name)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'config.ini')
    return config_path


def write_item(section, key, value):
    parser = ConfigParser()
    config_path = get_config_path()
    parser.read(config_path)
    if not parser.has_section(section):
        parser.add_section(section)
    parser.set(section, key, str(value))
    click.echo("Write '{key} = {value}' to config.ini.".format(key=key, value=value))
    with open(config_path, 'w') as fp:
        parser.write(fp)
