"""The config commands for `corrcli`
"""
import os
from configparser import ConfigParser
import click
from .cli import cli
from corrcli import default_config_file



@cli.command()
@click.option('--email', default=None, help="Add email address.", type=str)
@click.option('--name', default=None, help="Add user's name.", type=str)
@click.option('--url', default=None, help="Set the remote API url", type=str)
@click.option('--port', default=None, help="Set the remote API port", type=str)
@click.option('--list', default=False, is_flag=True, help="List contents of the config file")
@click.pass_context
def config(ctx, email, name, url, port, list):
    """Write data to the 'config.ini' file.
    """
    ini_file = os.path.join(ctx.parent.params['config_dir'], default_config_file)

    entries = [('default', 'email', email),
               ('default', 'name', name),
               ('api', 'url', url),
               ('api', 'port', port)]

    for section, key, value in entries:
        if value:
            write_item(section, key, value, ini_file)

    if list:
        with open(ini_file, 'r') as fpointer:
            click.echo(fpointer.read())


def write_item(section, key, value, ini_file):
    """Write a key value pair to an ini file.

    Write the following to a file.

    ```
    [section]
    key = value
    ```

    Args:
      section: the `[section]` to write to
      key: the key in `key = value`
      value: the value in `key = value`
      ini_file: the config file to write to
    """
    parser = ConfigParser()
    parser.read(ini_file)
    if not parser.has_section(section):
        parser.add_section(section)
    parser.set(section, key, str(value))
    click.echo("Write '{key} = {value}' to config.ini.".format(key=key, value=value))
    with open(ini_file, 'w') as fpointer:
        parser.write(fpointer)
