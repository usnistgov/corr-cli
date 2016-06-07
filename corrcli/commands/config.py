import inspect
import corrcli
import os


@corrcli.cli.command()
@corrcli.cli.option('--email', default=None, help="Add email address.", type=str)
@corrcli.cli.option('--port', '-p', default=None, help="Add API port number", type=int)
@corrcli.cli.option('--key', '-k', default=None, help="Add API key", type=str)
def config():
    app_name = dict(inspect.getmembers(corrcli))['__name__']



    import os

    import click
    import ConfigParser

    APP_NAME = 'My Application'

def read_config():
    cfg = os.path.join(click.get_app_dir(APP_NAME), 'config.ini')
    parser = ConfigParser.RawConfigParser()
    parser.read([cfg])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    return rv
