"""The config commands for `corrcli`
"""
import os
import inspect
from configparser import ConfigParser
import click
import corrcli


def get_config_path(module):
    """Get the path to CoRR's config.ini

    The path is platform independent.

    Args:
      app: a module to obtain the app name from

    Returns:
      the path to config.ini
    """
    app_name = dict(inspect.getmembers(module))['__name__']
    config_dir = click.get_app_dir(app_name)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'config.ini')
    return config_path


@corrcli.cli.command()
@click.option('--email', default=None, help="Add email address.", type=str)
@click.option('--name', default=None, help="Add email address.", type=str)
@click.option('--url', default=None, help="Set the remote API url", type=str)
@click.option('--port', default=None, help="Set the remote API port", type=str)
@click.option('--ini_file',
              default=get_config_path(corrcli),
              help="Set the config file to write to",
              type=str)
def config(email, name, url, port, ini_file):
    """Write data to the 'config.ini' file.
    """
    entries = [('default', 'email', email),
               ('default', 'name', name),
               ('api', 'url', url),
               ('api', 'port', port)]

    for section, key, value in entries:
        if value:
            write_item(section, key, value, ini_file)


def write_item(section, key, value, config_file):
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
      config_file: the config file to write to
    """
    parser = ConfigParser()
    parser.read(config_file)
    if not parser.has_section(section):
        parser.add_section(section)
    parser.set(section, key, str(value))
    click.echo("Write '{key} = {value}' to config.ini.".format(key=key, value=value))
    with open(config_file, 'w') as fpointer:
        parser.write(fpointer)
