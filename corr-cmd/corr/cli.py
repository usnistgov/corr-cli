import os
import click
import corr
import server
import core
import api

# os.environ.get('USER', '')

@click.command()

# Config
@click.option('--config/--no-config', default=None, help="Configure corr.")
@click.option('--conx/--no-conx', default=None, help="Check the provided api connectivity.")

# Execution Management
@click.option('--register/--no-register', default=None, help="Register a software. Produces a marker.")
@click.option('--sync/--no-sync', default=None, help="Sync a registration with the CoRR cloud project associated.")
@click.option('--align/--no-align', default=None, help="Align registrations with api backend.")
@click.option('--unregister/--no-unregister', default=None, help="Unregister a software.")
@click.option('--name', default=None, help="Choosen unique name for a software.")
@click.option('--host', default=None, help="Backend api host.")
@click.option('--port', default=None, help="Backend api port.")
@click.option('--key', default=None, help="Backend api key.")
@click.option('--watch/--no-watch', default=None, help="Watch software processes.")
@click.option('--unwatch/--no-unwatch', default=None, help="Unwatch software processes.")
@click.option('--list/--no-list', default=None, help="Unwatch software processes.")
@click.option('--show/--no-show', default=None, help="Unwatch software processes.")
@click.option('--marker', default=None, help="An execution marker.")

# Files Management
@click.option('--upload/--no-upload', default=None, help="Upload process.")
@click.option('--file/--no-file', default=None, help="file to consider.")
@click.option('--env/--no-env', default=None, help="environment to consider.")
@click.option('--path', default=None, help="Path to a file.")
@click.option('--obj', default=None, help="object id")
@click.option('--group', default=None, help="object group [{0}]".format(','.join(["input", "output", "dependencie", "file", "descriptive", "diff", "resource-record", "resource-env", "resource-app", "attach-comment", "attach-message", "picture" , "logo-project" , "logo-app" , "resource", "bundle"])))

def handle(config, conx, register, sync, align, unregister, name, host, port, key, watch, unwatch, list, show, marker, upload, file, env, path, obj, group):
    if config:
        core.configure(host=host, port=port, key=key)

    if conx:
        config = core.read_config()
        if api.api_status(config=config):
            print "OK --- CoRR backend api[{0}:{1}] reached.".format(config['api']['host'], config['api']['port'])
        else:
            print "KO --- could not reach CoRR backend api[{0}:{1}].".format(config['api']['host'], config['api']['port'])

    if list:
        core.list()

    if show:
        core.show(name=name, marker=marker)

    if align:
        core.align()

    if register:
        core.register(name=name)

    if sync:
        core.sync(name=name, marker=marker)

    if unregister:
        core.unregister(name=name)

    if watch:
        core.watch(name=name, marker=marker)

    if unwatch:
        core.unwatch(name=name, marker=marker)

    if upload and file:
        core.push_file(path=path, obj=obj, group=group)

    if upload and env:
        core.push_env(name=name, marker=marker, path=path)

if __name__ == '__main__':
    handle()