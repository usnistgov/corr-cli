"""The config commands for `corrcli`
"""
import os
from configparser import ConfigParser
import click
from .cli import cli
from .cli import DEFAULT_CONFIG_FILE

@cli.group()
def config():
    """Configure the CoRR command line tool.
    """

@config.command('set')
@click.option('--email', default=None, help="Add email address.", type=str)
@click.option('--name', default=None, help="Add user's name.", type=str)
@click.option('--refresh-rate',
              default=None,
              help="The refresh rate for watching tasks.",
              type=float)
@click.pass_context
def set_config(ctx, email, name, refresh_rate):
    """Write data to the 'config.ini' file.
    """
    ini_file = os.path.join(ctx.parent.parent.params['config_dir'], DEFAULT_CONFIG_FILE)

    entries = [('default', 'email', email),
               ('default', 'name', name),
               ('tasks', 'refresh_rate', refresh_rate)]

    for section, key, value in entries:
        if value:
            write_item(section, key, value, ini_file)


@config.command('list')
@click.pass_context
def list_config(ctx):
    """List contents of the config file.
    """
    ini_file = os.path.join(ctx.parent.parent.params['config_dir'], DEFAULT_CONFIG_FILE)
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

def parse_config(config_dir):
    """Parse the configuration file.

    Using a dictionary is easier than using the ConfigParser directly.

    Args:
      config_dir: the CoRR configuration directory

    Returns:
      a dictionary of the form `section_option : value`.

    """
    parser = ConfigParser()
    parser.read(os.path.join(config_dir, DEFAULT_CONFIG_FILE))
    data = {}
    for section in parser.sections():
        for option in parser.options(section):
            data["{0}_{1}".format(section, option)] = parser.get(section, option)
    return data
