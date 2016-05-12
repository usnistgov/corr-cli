import click
from corr.main import core

@click.command()

# Config
@click.option('--config/--no-config', default=None, help="Configure corr.")
@click.option('--conx/--no-conx', default=None, help="Check the provided api connectivity.")

# Execution Management
@click.option('--register/--no-register', default=None,
              help="Register a software. Produces a tag.")
@click.option('--sync/--no-sync', default=None,
              help="Sync a registration with the CoRR cloud project associated.")
@click.option('--align/--no-align', default=None, 
              help="Align registrations with api backend.")
@click.option('--unregister/--no-unregister', default=None,
              help="Unregister a software.")
@click.option('--name', default=None,
              help="Choosen unique name for a software.")
@click.option('--host', default=None,
              help="Backend api host.")
@click.option('--port', default=None,
              help="Backend api port.")
@click.option('--key', default=None,
              help="Backend api key.")
@click.option('--watch/--no-watch', default=None,
              help="Watch software processes.")
@click.option('--unwatch/--no-unwatch', default=None,
              help="Unwatch software processes.")
@click.option('--list/--no-list', default=None,
              help="Unwatch software processes.")
@click.option('--show/--no-show', default=None,
              help="Unwatch software processes.")
@click.option('--tag', default=None,
              help="An execution tag.")
@click.option('--force/--no-force', default=None,
              help="Bypass some conditions.")
@click.option('--newtag/--no-newtag', default=None,
              help="An execution newtag.")

# Extension
@click.option('--extend/--no-extend', default=None,
              help="Manage extensions.")
@click.option('--add/--no-add', default=None,
              help="Add an extension.")
@click.option('--delete/--no-delete', default=None,
              help="Delete an extension.")
@click.option('--all/--no-all', default=None,
              help="Show all extensions.")
@click.option('--alias', default=None,
              help="Extension short name.")
@click.option('--impl', default=None,
              help="Extension implementation.")
@click.option('--clnk/--no-clnk', default=None,
              help="A CoreLink extension.")
@click.option('--api/--no-api', default=None,
              help="API extension.")
@click.option('--elnk/--no-elnk', default=None,
              help="A ExecLink extension.")
@click.option('--ctsk/--no-ctsk', default=None,
              help="A CorrTask extension.")

# Files Management
@click.option('--upload/--no-upload', default=None,
              help="Upload process.")
@click.option('--file/--no-file', default=None,
              help="file to consider.")
@click.option('--env/--no-env', default=None,
              help="environment to consider.")
@click.option('--path', default=None,
              help="Path to a file.")
@click.option('--obj', default=None,
              help="object id")
@click.option('--group', default=None,
              help="object group [{0}]".format(','.join(
                  ["input", "output", "dependencie", "file",
                   "descriptive", "diff", "resource-record",
                   "resource-env", "resource-app", "attach-comment",
                   "attach-message", "picture", "logo-project",
                   "logo-app", "resource", "bundle"])))

def handle(config, conx, register, sync, align, unregister,
           name, host, port, key, watch, unwatch, list, show, tag,
           newtag, upload, file, env, path, obj, group, force, extend,
           add, delete, all, alias, impl, clnk, api, elnk, ctsk):

    def paths(clnk=None, api=None, elnk=None, ctsk=None):
      extensions = core.read_extend()
      if clnk:
        clnk_path = extensions['coreLink'][clnk]['path']
      else:
        clnk_path = 'corr.main.coreLink'
      clnk_module = core.extend_load(clnk_path)
      if api:
        api_path = extensions['api'][api]['path']
      else:
        api_path = 'corr.main.api'
      if elnk:
        elnk_path = extensions['execLink'][elnk]['path']
      else:
        elnk_path = 'corr.main.execLink'
      if ctsk:
        ctsk_path = extensions['corrTask'][ctsk]['path']
      else:
        ctsk_path = 'corr.main.corrTask'
      return [clnk_module, api_path, elnk_path, ctsk_path]

    if extend:
      extensions = core.read_extend()
      if add:
        if clnk:
          core.extension_add(extensions, 'coreLink')
        elif api:
          core.extension_add(extensions, 'api')
        elif elnk:
          core.extension_add(extensions, 'execLink')
        elif ctsk:
          core.extension_add(extensions, 'corrTask')
        else:
          # # print "Unknown extension group -- interoerate not supported yet."
          pass
      if delete:
        if clnk:
          core.extension_delete(extensions, 'coreLink', alias)
        elif api:
          core.extension_delete(extensions, 'api', alias)
        elif elnk:
          core.extension_delete(extensions, 'execLink', alias)
        elif ctsk:
          core.extension_delete(extensions, 'corrTask', alias)
      if all:
        core.extension_all(extensions)
    elif newtag and name:
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        extends[0].tag(name=name, api=extends[1], elnk=extends[2], ctsk=extends[3])
    elif list:
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        regs = extends[0].list(api=extends[1], elnk=extends[2], ctsk=extends[3])
        for reg in regs:
          print "{0}\t{1}\t{2}\t{3}".format(
              reg['name'], str(reg['tags']), reg['status']['stamp'],
              reg['status']['value'])
    elif show and (name or tag):
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        print extends[0].show(name=name, tag=tag, api=extends[1], elnk=extends[2], ctsk=extends[3])
    elif align:
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        extends[0].align(api=extends[1], elnk=extends[2], ctsk=extends[3])
    elif register and name:
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        extends[0].register(name=name, api=extends[1], elnk=extends[2], ctsk=extends[3])
    elif sync:
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        extends[0].sync(name=name, tag=tag, force=force, api=extends[1], elnk=extends[2], ctsk=extends[3])
    elif unregister:
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        extends[0].unregister(name=name, api=extends[1], elnk=extends[2], ctsk=extends[3])
    elif watch and (name or tag):
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        extends[0].watch(name=name, tag=tag, api=extends[1], elnk=extends[2], ctsk=extends[3])
    elif unwatch and (name or tag):
        extends = paths(clnk=clnk, api=api, elnk=elnk, ctsk=ctsk)
        extends[0].unwatch(name=name, tag=tag, api=extends[1], elnk=extends[2], ctsk=extends[3])
    else:
        if clnk:
          extensions = core.read_extend()
          clnk_path = extensions['coreLink'][alias]['path']
        else:
          clnk_path = 'corr.main.coreLink'
        clnk_module = core.extend_load(clnk_path)
        clnk_module.handle()

if __name__ == '__corr.main__':
    handle()
