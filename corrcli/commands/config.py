import inspect
import corrcli
import os
from configparser import ConfigParser
import click


@corrcli.cli.command()
@click.option('--email', default=None, help="Add email address.", type=str)
@click.option('--name', default=None, help="Add email address.", type=str)
@click.option('--url', default=None, help="Set the remote API url", type=str)
@click.option('--port', default=None, help="Set the remote API port", type=str)
def config(email, name, url, port):
    """Write data to the 'config.ini' file.
    """
    entries = [('default', 'email', email),
               ('default', 'name', name),
               ('api', 'url', url),
               ('api', 'port', port)]

    for section, key, value in entries:
        if value:
            write_item(section, key, value)


def get_config_path():
    """Get the path to CoRR's config.ini

    The path is platform independent.

    Returns:
      the path to config.ini
    """
    app_name = dict(inspect.getmembers(corrcli))['__name__']
    config_dir = click.get_app_dir(app_name)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    config_path = os.path.join(config_dir, 'config.ini')
    return config_path


def write_item(section, key, value):
    """Write a key value pair to an ini file.

    Write to a file such that

    ```
    [section]
    key = value
    ```

    Args:
      section: the `[section]` to write to
      key: the key in `key = value`
      value: the value in `key = value`
    """
    parser = ConfigParser()
    config_path = get_config_path()
    parser.read(config_path)
    if not parser.has_section(section):
        parser.add_section(section)
    parser.set(section, key, str(value))
    click.echo("Write '{key} = {value}' to config.ini.".format(key=key, value=value))
    with open(config_path, 'w') as fp:
        parser.write(fp)
