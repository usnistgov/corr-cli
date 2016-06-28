import sys
import os
import datetime
import traceback
import getpass
import json
import click
from corr.main import core

@click.command()

# Config
@click.option('--config/--no-config', default=None, help="Configure corr.")
@click.option('--conx/--no-conx', default=None, help="Check the provided api connectivity.")

@click.option('--api/--no-api', default=None,
              help="A CoreLink extension.")

# Execution Management
@click.option('--name', default=None,
              help="Choosen unique name for a software.")
@click.option('--host', default=None,
              help="Backend api host.")
@click.option('--port', default=None,
              help="Backend api port.")
@click.option('--key', default=None,
              help="Backend api key.")
@click.option('--tag', default=None,
              help="An execution tag.")

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

def handle(config, conx, name, host, port, key, tag,
           upload, file, env, path, obj, group, api):
    if config:
        print configure(host=host, port=port, key=key)

    if conx:
        config = core.read_config('default')
        if api:
          api_path = extensions['api'][alias]['path']
        else:
          api_path = 'corr.main.api'
        api_module = core.extend_load(api_path)
        if api_module.api_status(config=config):
            ## print "OK --- CoRR backend api[{0}:{1}] reached.".format(
            #    config['api']['host'], config['api']['port'])
            print "OK"
        else:
            ## print "KO --- could not reach CoRR backend api[{0}:{1}].".format(
            #    config['api']['host'], config['api']['port'])
            print "KO"

    if upload and file:
        push_file(path=path, obj=obj, group=group)

    if upload and env:
        push_env(name=name, tag=tag, path=path)

def whois():
    return "CoreLink"

# change the way you configure access to the backend API.
# Make sure you specify your configuration tag.
# coreLink uses the default one.
def configure(host=None, port=None, key=None):
    config = core.read_config('default')
    if host is None and port is None and key is None:
        return core.pretty_json(core.read_config())
        # # print core.pretty_json(core.read_config())
    else:
        if host:
            config['api']['host'] = host
        if port:
            config['api']['port'] = port
        if key:
            config['api']['key'] = key
        core.write_config('default', config)
        return core.pretty_json({'default':config})

# Change the way you access registrations.
def find_by(regs=[], name=None, tag=None):
    # Todo: Allow research based on records.
    reg_fs = []
    index = 0
    for reg in regs:
        try:
            if name != None and name in reg['name']:
                reg_fs.append(index)
            if tag != None and tag in reg['tags']:
                reg_fs.append(index)
        except:
            # # print reg
            pass
        index += 1
    return reg_fs

# Change the way you want to display the registration.
def list(api=None, elnk=None, ctsk=None):
    ## print "# corr registrations"
    ## print "#"
    registrations = core.read_reg('default')
    # for reg in registrations:
        # print "{0}\t{1}\t{2}\t{3}".format(
        #     reg['name'], str(reg['tags']), reg['status']['stamp'],
        #     reg['status']['value'])
    return registrations

# Change the way you want to show a registration
def show(name=None, tag=None, api=None, elnk=None, ctsk=None):
    registrations = core.read_reg('default')
    investigations = find_by(regs=registrations, name=name, tag=tag)
    if len(investigations) > 0:
        for investigation in investigations:
            # print core.pretty_json(registrations[investigation])
            return core.pretty_json(registrations[investigation])
    else:
        # print "Could not found name/tag registered."
        return None

# Change the way to controll our watcher processes.
def subprocess_cmd(command=[]):
    try:
        import subprocess
        process = subprocess.Popen(command)
        return process
    except:
        return None

# Change the way we sync our local repo with the API
def align(api=None, elnk=None, ctsk=None):
    config = core.read_config('default')
    registrations = core.read_reg('default')
    # # print core.read_reg()
    # # print registrations
    api_module = core.extend_load(api)
    api_response = api_module.project_all(config=config)
    if api_response[0] == True:
        projects_json = api_response[1]
        # # print "--> Backend has {0} projects".format(
            # projects_json['total_projects'])
        projects = projects_json['projects']
        for project in projects:
            name = project['name']
            tags = project['tags']
            investigations = find_by(regs=registrations, name=name)
            if len(investigations) == 0:
                # # print "--> Aligning with remote project [{0}]...".format(name)
                investigation = {}
                stamp = core.formated_stamp()
                investigation['name'] = name
                investigation['tags'] = tags
                investigation['status'] = {'value':'registered', 'stamp':stamp}
                investigation['consistency'] = True
                investigation['project'] = project['id']
                investigation['history'] = []
                investigation['watcher'] = None
                registrations.append(investigation)
                core.ensure_repo(investigation['name'])
                # # print registrations
                core.write_reg('default', registrations)
                # # print "--> Done."
        # # print core.read_reg()
        return True 
    else:
        ## print "Registrations alignment failed."
        # print api_response[1]
        return False

# Change the way we register an investigation.
def register(name=None, api=None, elnk=None, ctsk=None):
    ## print ""
    ## print "Registering the investigation..."
    config = core.read_config('default')
    registrations = core.read_reg('default')
    investigations = find_by(regs=registrations, name=name)
    if len(investigations) > 0 and registrations[investigations[0]]['status']['value'] != 'unregistered':
        ## print "An investigation with this name/tag has already been registered."
        ## print "Its name and tag are: [{0}|{1}]".format(registrations[investigations[0]]['name'], registrations[investigations[0]]['tags'])
        return registrations[investigations[0]]
    else:
        if len(investigations) > 0 and registrations[investigations[0]]['status']['value'] == 'unregistered':
            stamp = core.formated_stamp()
            registrations[investigations[0]]['history'].append(registrations[investigations[0]]['status'])
            registrations[investigations[0]]['status'] = {'value':'registered', 'stamp':stamp}
            registrations[investigations[0]]['consistency'] = False
            core.ensure_repo(registrations[investigations[0]]['name'])
            core.write_reg('default', registrations)
            ## print "An investigation with this name/tag was\
            # unregistered and is now registered back again."
            if not registrations[investigations[0]]['consistency']:
                api_module = core.extend_load(api)
                api_response = api_module.project_create(config=config,
                                                  name=registrations[investigations[0]]['name'],
                                                  description='no description provided.',
                                                  goals='no goals set.',
                                                  tags=registrations[investigations[0]]['tags'])
                if api_response[0] == True:
                    registrations[investigations[0]]['consistency'] = True
                    registrations[investigations[0]]['project'] = api_response[1]['id']
                    core.ensure_repo(registrations[investigations[0]]['name'])
                    core.write_reg('default', registrations)
                    ## print "The associated project metadata is now consistent."
                    return registrations[investigations[0]]
                else:
                    ## print "Consistency alignment between registration and project metadat failed. \
                    #Please check connectivity and try to sync the investigation again later."
                    # print api_response[1]
                    return registrations[investigations[0]]
            else:
                return None
        else:
            investigation = {}
            stamp = core.formated_stamp()
            investigation['tags'] = ["%s-tag-%s"%(name, stamp)]
            if name != None:
                investigation['name'] = name
            else:
                investigation['name'] = "name_%s"%stamp
            investigation['status'] = {'value':'registered', 'stamp':stamp}
            investigation['consistency'] = False
            investigation['history'] = []
            investigation['watcher'] = None
            exists = False
            if not investigation['name'].isalnum():
                ## print "Registration failed. name has to be alphanumberial."
                return None
            else:
                for reg in registrations:
                    if reg['name'] == investigation['name']:
                        exists = True
                        break
                if not exists:
                    registrations.append(investigation)
                    core.ensure_repo(investigation['name'])
                    core.write_reg('default', registrations)
                    ## print "Registration produced tag: {0}".format(investigation['tags'])
                    api_module = core.extend_load(api)
                    api_response = api_module.project_create(
                        config=config,
                        name=investigation['name'],
                        description='no description provided.',
                        goals='no goals set.',
                        tags=investigation['tags'])
                    if api_response[0] == True:
                        investigation['consistency'] = True
                        investigation['project'] = api_response[1]['id']
                        core.ensure_repo(investigation['name'])
                        core.write_reg('default', registrations)
                        ## print "The associated project metadata is now\
                        #consistent with the registration."
                        return "Consistent"
                    else:
                        ## print "Consistency alignment between registration\
                        #and project metadat failed. Please check connectivity\
                        #and try to sync the investigation later."
                        # print api_response[1]
                        return investigation
                else:
                    ## print "Registration failed. A registration already exists\
                    #with the name: {0}".format(investigation['name'])
                    return investigation

# Change the way tag an investigation.
def tag(name=None, api=None, elnk=None, ctsk=None):
    ## print ""
    ## print "Taging the investigation..."
    config = core.read_config('default')
    registrations = core.read_reg('default')
    investigations = find_by(regs=registrations, name=name)
    if len(investigations) > 0 and registrations[investigations[0]]['status']['value'] != 'unregistered':
        ## print "An investigation with this name/tag has already been registered."
        ## print "Its name and tag are: [{0}|{1}]".format(registrations[investigations[0]]['name'], registrations[investigations[0]]['tags'])
        stamp = core.formated_stamp()
        tag = "{0}-tag-{1}".format(name, stamp)
        registrations[investigations[0]]['tags'].append(tag)
        core.ensure_repo(registrations[investigations[0]]['name'])
        core.write_reg('default', registrations)
        api_module = core.extend_load(api)
        api_response = api_module.project_update(
            config=config,
            project=registrations[investigations[0]]['project'],
            description=None,
            goals=None,
            tags=registrations[investigations[0]]['tags'])
        # # print api_response[1]
        return [tag, api_response[1]]
    else:
       ## print "No investigation with this name/tag has been registered."
       return None

# Change the way we sync our local copy with the API.
# Maybe move align also into sync so that it is both ways.
def sync(name=None, tag=None, force=False, api=None, elnk=None, ctsk=None):
    config = core.read_config()
    registrations = core.read_reg('default')
    if name is None and tag is None:
        ## print "Syncing all inconsistent registrations..."
        for idx, reg in enumerate(registrations):
            if not reg['consistency'] or force:
                ## print "Syncing the registration [{0}]...".format(reg['name'])
                api_module = core.extend_load(api)
                api_response = api_module.project_create(
                    config=config,
                    name=reg['name'],
                    description='no description provided.',
                    goals='no goals set.',
                    tags=reg['tags'])
                if api_response[0] == True:
                    reg['consistency'] = True
                    reg['project'] = api_response[1]['id']
                    core.ensure_repo(reg['name'])
                    registrations[idx] = reg
                    core.write_reg('default', registrations)
                    ## print "--> This associated project metadata is now consistent."
                    # return api_response[1]
                # else:
                    ## print "--> Consistency alignment between registration\
                    #and project metada failed. Please check connectivity\
                    #and try to sync the investigation again later."
                    ## print api_response[1]
                    # return api_response[1]
            # else:
                ## print "Registration [{0}] is already consistent.".format(reg['name'])
        return registrations
    else:
        ## print "Syncing the registration..."
        investigations = find_by(regs=registrations, name=name, tag=tag)
        if len(investigations) > 0 and (not registrations[investigations[0]]['consistency'] or force):
            api_module = core.extend_load(api)
            api_response = api_module.project_create(
                config=config,
                name=registrations[investigations[0]]['name'],
                description='no description provided.',
                goals='no goals set.',
                tags=[registrations[investigations[0]]['tags']])
            if api_response[0] == True:
                registrations[investigations[0]]['consistency'] = True
                registrations[investigations[0]]['project'] = api_response[1]['id']
                core.ensure_repo(registrations[investigations[0]]['name'])
                core.write_reg('default', registrations)
                ## print "The associated project metadata is now consistent."
                return api_response[1]
            else:
                ## print "--> Consistency alignment between registration\
                #    and project metada failed. Please check connectivity\
                #    and try to sync the investigation again later."
                ## print api_response[1]
                return None
        else:
            if len(investigations) > 0:
                ## print "The associated project metadata is already consistent."
                return registrations[investigations[0]]
            else:
                ## print "Error: No registration with this name."
                return None

# Change the way you unregister an investigation.
def unregister(name=None, tag=None, api=None, elnk=None, ctsk=None):
    ## print "Unregistering the investigation..."
    registrations = core.read_reg('default')
    investigations = find_by(regs=registrations, name=name, tag=tag)
    if len(investigations) > 0 and registrations[investigations[0]]['status']['value'] != 'unregistered':
        registrations[investigations[0]]['history'].append(registrations[investigations[0]]['status'])
        stamp = core.formated_stamp()
        registrations[investigations[0]]['history'].append(registrations[investigations[0]]['status'])
        registrations[investigations[0]]['status'] = {'value':'unregistered', 'stamp':stamp}
        core.write_reg('default', registrations)
        # Delete the .source
        # Delete investigation repo and section from registrations.
        ## print "investigation unregistered."
        return True
    else:
        ## print "Could not found a investigation with\
        # this name/tag to unregister."
        return False

# Change the way you launch a watcher.
def watcher_launch(name=None, tag=None, api=None, elnk=None, ctsk=None):
    # from subprocess import call
    task_cmd = []
    if ctsk:
        if '.py' in ctsk:
            task_cmd.append("python")
            task_cmd.append(ctsk)
        else:
            task_cmd.append("python")
            task_cmd.append("-m")
            task_cmd.append(ctsk)
    else:
        task_cmd.append("python")
        task_cmd.append("-m")
        task_cmd.append("corr.main.corrTask")
    if name:
        task_cmd.append("--name")
        task_cmd.append(name)
    if tag:
        task_cmd.append("--tag")
        task_cmd.append(tag)
    task_cmd.append("--elnk")
    task_cmd.append(elnk)
    task_cmd.append("--api")
    task_cmd.append(api)
    # call(task_cmd)
    try:
        import subprocess
        process = subprocess.Popen(task_cmd)
        return process
    except:
        print traceback.print_exc(file=sys.stdout)
        return None

# Change the way you stop a watcher.
def watcher_stop(reg=None, api=None, elnk=None, ctsk=None):
    task_cmd = []
    task_cmd.append("sudo")
    task_cmd.append("-S")
    task_cmd.append("kill")
    task_cmd.append("-9")
    task_cmd.append(str(reg['watcher']))
    ## print "Unwatching on task-[{0}]...".format(str(reg['watcher']))
    sudo_password = ''
    try:
        import subprocess
        sudo_password = getpass.getpass('Password:')
        process = subprocess.Popen(task_cmd, universal_newlines=True)
        process.communicate(sudo_password + '\n')
        return process
    except:
        print traceback.print_exc(file=sys.stdout)
        return None

# Change the way you watch an investigation.
def watch(name=None, tag=None, api=None, elnk=None, ctsk=None):
    registrations = core.read_reg('default')
    investigations = find_by(regs=registrations, name=name, tag=tag)
    # # print str(registrations[investigations[0]])
    if len(investigations) > 0 and registrations[investigations[0]]['status']['value'] != 'unregistered':
        if registrations[investigations[0]]['status']['value'] == 'watching':
            ## print "Already watching this entry."
            return [True, None]
        else:
            registrations[investigations[0]]['history'].append(registrations[investigations[0]]['status'])
            stamp = core.formated_stamp()
            registrations[investigations[0]]['history'].append(registrations[investigations[0]]['status'])
            registrations[investigations[0]]['status'] = {'value':'watching', 'stamp':stamp}
            task_process = watcher_launch(
                name=registrations[investigations[0]]['name'],
                tag=tag,
                api=api, elnk=elnk, ctsk=ctsk)
            if task_process:
                ## print "Watching on task-[{0}]...".format(int(task_process.pid))
                registrations[investigations[0]]['watcher'] = int(task_process.pid) + 4
                core.write_reg('default', registrations)
                ## print "Watching the investigation..."
                return [True, task_process]
            else:
                ## print "Error: Could not start this watcher."
                return [False, None]
    else:
        ## print "Could not found this investigation to watch."
        return [False, None]

# Change the way you unwatch an investigation.
def unwatch(name=None, tag=None, api=None, elnk=None, ctsk=None):
    registrations = core.read_reg('default')
    investigations = find_by(regs=registrations, name=name, tag=tag)
    if len(investigations) > 0 and registrations[investigations[0]]['status']['value'] != 'unregistered':
        if registrations[investigations[0]]['status']['value'] == 'watching':
            registrations[investigations[0]]['history'].append(registrations[investigations[0]]['status'])
            stamp = core.formated_stamp()
            registrations[investigations[0]]['history'].append(registrations[investigations[0]]['status'])
            registrations[investigations[0]]['status'] = {'value':'unwatched', 'stamp':stamp}
            stop_process = watcher_stop(reg=registrations[investigations[0]], api=api, elnk=elnk, ctsk=ctsk)
            if stop_process:
                registrations[investigations[0]]['watcher'] = None
                core.write_reg('default', registrations)
                ## print "investigation unwatched"
                return [True, stop_process]
            else:
                ## print "Error: Could not stop this watcher."
                return [False, None]
        elif registrations[investigations[0]]['status']['value'] == 'unwatched':
            ## print "Already unwatched this entry."
            return [True, None]
    else:
        ## print "Could not found this investigation to unwatch."
        return [False, None]

# Change the way you upload a file.
def push_file(path=None, obj=None, group=None):
    config = core.read_config()
    api_module = core.extend_load(api)
    api_response = api_module.upload_file(config=config, path=path, obj=obj, group=group)
    if api_response[0]:
        ## print "File uploaded."
        return api_response[1]
    else:
        ## print "File upload failed."
        # # print api_response[1]
        return api_response[1]

# Change the way you upload an environment.
def push_env(name=None, tag=None, path=None):
    config = core.read_config()
    registrations = core.read_reg('default')
    investigations = find_by(regs=registrations, name=name, tag=tag)
    if len(investigations) > 0 and registrations[investigations[0]]['status']['value'] != 'unregistered':
        if registrations[investigations[0]]['status']['value'] == 'watching':
            ## print "Error: Uploading new environment while watching is not possible. Unwatch first."
            return registrations[investigations[0]]
        else:
            api_module = core.extend_load(api)
            api_response = api_module.project_env_next(
                config=config,
                project=registrations[investigations[0]]['project'],
                path=path)
            if api_response[0]:
                ## print "Environment successfully pushed."
                return api_response[1]
            else:
                ## print "Error: Environment push failed."
                # # print api_response[1]
                return api_response[1]