import sys
import os
import datetime
import traceback
import getpass
import json
# Externalize api calls here into the coreLink.
# It has to be changeable/extendable.
# Allow the inclusion of the project.json structure.
# The project related cli parts should be moved to
# coreLink.
# It will then handle links from core to the API
# project/registration handling
# It will handle the watch/unwatch mechanism.
# It handles the watcher.
# Core has to implement extension capabilities.
# Load the configuration and load the appropriate
# files.
# We have to add interperate file.
from corr import api


corr_path = "%s/.corr"%os.path.expanduser('~')
config_path = "{0}/config.json".format(corr_path)
reg_path = "{0}/registrations.json".format(corr_path)
repos_path = "{0}/repositories".format(corr_path)
tasks_path = "{0}/tasks".format(corr_path)

def formated_stamp():
    stamp = str(datetime.datetime.now())
    stamp = stamp.replace(" ", "_").replace(":", "-")
    return stamp

def pretty_json(json_data=None):
    if json_data != None:
        return json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        return None
def ensure_root():
    if not os.path.exists(corr_path):
        os.makedirs(corr_path)

    if not os.path.exists(repos_path):
        os.makedirs(repos_path)

    if not os.path.exists(tasks_path):
        os.makedirs(tasks_path)

    if not os.path.isfile(reg_path):
        with open(reg_path, "w") as reg_file:
            reg_file.write(pretty_json([]))

    if not os.path.isfile(config_path):
        with open(config_path, "w") as config_file:
            config_file.write(pretty_json({'api':{}}))

def ensure_repo(name=None):
    ensure_root()
    if name != None:
        repo_path = "{0}/{1}.corr".format(repos_path, name)
        if not os.path.isfile(repo_path):
            with open(repo_path, "w") as repo_json:
                repo_json.write(pretty_json({}))

def read_repo(name=None):
    ensure_repo()
    if name:
        repo_json = {}
        repo_path = "{0}/{1}.corr".format(repos_path, name)
        with open(repo_path, "r") as repo_file:
            repo_json = json.loads(repo_file.read())
        return repo_json
    else:
        return None

def write_repo(name=None, repo_json=None):
    ensure_repo()
    if name and repo_json:
        repo_path = "{0}/{1}.corr".format(repos_path, name)
        with open(repo_path, "w") as repo_file:
            repo_file.write(pretty_json(repo_json))
        return True
    else:
        return False

def read_config():
    try:
        ensure_root()
        config_json = {}
        with open(config_path, "r") as config_file:
            config_json = json.loads(config_file.read())
        return config_json
    except:
        return {}

def write_config(config_json=None):
    try:
        ensure_root()
        with open(config_path, "w") as config_file:
            config_file.write(pretty_json(config_json))
        return True
    except:
        return False

def configure(host=None, port=None, key=None):
    config = read_config()
    if host is None and port is None and key is None:
        print pretty_json(config)
    else:
        if host:
            config['api']['host'] = host
        if port:
            config['api']['port'] = port
        if key:
            config['api']['key'] = key
        write_config(config)

def write_reg(reg=[]):
    ensure_root()
    with open(reg_path, "w") as reg_json:
        reg_json.write(pretty_json(reg))

def read_reg():
    ensure_root()
    registrations = []
    with open(reg_path, "r") as reg_json:
        registrations = json.loads(reg_json.read())
    return registrations

def find_by(regs=[], name=None, marker=None):
    # Todo: Allow research based on records.
    reg_fs = []
    index = 0
    for reg in regs:
        if name != None and name in reg['name']:
            reg_fs.append(index)
        if marker != None and marker in reg['marker']:
            reg_fs.append(index)
        index += 1
    return reg_fs

def list():
    print "# corr registrations"
    print "#"
    registrations = read_reg()
    for reg in registrations:
        print "{0}\t{1}\t{2}\t{3}".format(
            reg['name'], reg['marker'], reg['status']['stamp'],
            reg['status']['value'])

def show(name=None, marker=None):
    registrations = read_reg()
    softwares = find_by(regs=registrations, name=name, marker=marker)
    if len(softwares) > 0:
        for software in softwares:
            print pretty_json(registrations[software])
    else:
        print "Could not found name/marker registered."

# def mark to update a software marker.

def subprocess_cmd(command=[]):
    try:
        import subprocess
        process = subprocess.Popen(command)
        return process
    except:
        return None

def align():
    config = read_config()
    registrations = read_reg()
    api_response = api.project_all(config=config)
    if api_response[0] == True:
        projects_json = api_response[1]
        print "--> Backend has {0} projects".format(
            projects_json['total_projects'])
        projects = projects_json['projects']
        for project in projects:
            name = project['name']
            marker = project['tags'][0]
            softwares = find_by(regs=registrations, name=name)
            if len(softwares) == 0:
                print "--> Aligning with remote project [{0}]...".format(name)
                software = {}
                stamp = formated_stamp()
                software['name'] = name
                software['marker'] = marker
                software['status'] = {'value':'registered', 'stamp':stamp}
                software['consistency'] = True
                software['project'] = project['id']
                software['history'] = []
                software['watcher'] = None
                registrations.append(software)
                ensure_repo(software['name'])
                write_reg(registrations)
                print "--> Done."
    else:
        print "Registrations alignment failed."
        print api_response[1]

def register(name=None):
    print "Registering the software..."
    config = read_config()
    registrations = read_reg()
    softwares = find_by(regs=registrations, name=name)
    if len(softwares) > 0 and registrations[softwares[0]]['status']['value'] != 'unregistered':
        print "A software with this name/marker has already been registered."
        print "Its name and marker are: [{0}|{1}]".format(registrations[softwares[0]]['name'], registrations[softwares[0]]['marker'])
    else:
        if len(softwares) > 0 and registrations[softwares[0]]['status']['value'] == 'unregistered':
            stamp = formated_stamp()
            registrations[softwares[0]]['history'].append(registrations[softwares[0]]['status'])
            registrations[softwares[0]]['status'] = {'value':'registered', 'stamp':stamp}
            registrations[softwares[0]]['consistency'] = False
            ensure_repo(registrations[softwares[0]]['name'])
            write_reg(registrations)
            print "A software with this name/marker was\
             unregistered and is now registered back again."
            if not registrations[softwares[0]]['consistency']:
                api_response = api.project_create(config=config,
                                                  name=registrations[softwares[0]]['name'],
                                                  description='no description provided.',
                                                  goals='no goals set.',
                                                  tags=[registrations[softwares[0]]['marker']])
                if api_response[0] == True:
                    registrations[softwares[0]]['consistency'] = True
                    registrations[softwares[0]]['project'] = api_response[1]['id']
                    ensure_repo(registrations[softwares[0]]['name'])
                    write_reg(registrations)
                    print "The associated project metadata is now consistent."
                else:
                    print "Consistency alignment between registration and project metadat failed. \
                    Please check connectivity and try to sync the software again later."
                    print api_response[1]
        else:
            software = {}
            stamp = formated_stamp()
            software['marker'] = "marker_%s"%stamp
            if name != None:
                software['name'] = name
            else:
                software['name'] = "name_%s"%stamp
            software['status'] = {'value':'registered', 'stamp':stamp}
            software['consistency'] = False
            software['history'] = []
            software['watcher'] = None
            exists = False
            if not software['name'].isalnum():
                print "Registration failed. name has to be alphanumberial."
            else:
                for reg in registrations:
                    if reg['name'] == software['name']:
                        exists = True
                        break
                if not exists:
                    registrations.append(software)
                    ensure_repo(software['name'])
                    write_reg(registrations)
                    print "Registration produced marker: {0}".format(software['marker'])
                    api_response = api.project_create(
                        config=config,
                        name=software['name'],
                        description='no description provided.',
                        goals='no goals set.',
                        tags=[software['marker']])
                    if api_response[0] == True:
                        software['consistency'] = True
                        software['project'] = api_response[1]['id']
                        ensure_repo(software['name'])
                        write_reg(registrations)
                        print "The associated project metadata is now\
                        consistent with the registration."
                    else:
                        print "Consistency alignment between registration\
                        and project metadat failed. Please check connectivity\
                        and try to sync the software later."
                        print api_response[1]
                else:
                    print "Registration failed. A registration already exists\
                    with the name: {0}".format(software['name'])

def sync(name=None, marker=None, force=False):
    config = read_config()
    registrations = read_reg()
    if name is None and marker is None:
        print "Syncing all inconsistent registrations..."
        for idx, reg in enumarate(registrations):
            if not reg['consistency'] or force:
                print "Syncing the registration [{0}]...".format(reg['name'])
                api_response = api.project_create(
                    config=config,
                    name=reg['name'],
                    description='no description provided.',
                    goals='no goals set.',
                    tags=[reg['marker']])
                if api_response[0] == True:
                    reg['consistency'] = True
                    reg['project'] = api_response[1]['id']
                    ensure_repo(reg['name'])
                    registrations[idx] = reg
                    write_reg(registrations)
                    print "--> This associated project metadata is now consistent."
                else:
                    print "--> Consistency alignment between registration\
                    and project metada failed. Please check connectivity\
                    and try to sync the software again later."
                    print api_response[1]
            else:
                print "Registration [{0}] is already consistent.".format(reg['name'])
    else:
        print "Syncing the registration..."
        softwares = find_by(regs=registrations, name=name, marker=marker)
        if len(softwares) > 0 and (not registrations[softwares[0]]['consistency'] or force):
            api_response = api.project_create(
                config=config,
                name=registrations[softwares[0]]['name'],
                description='no description provided.',
                goals='no goals set.',
                tags=[registrations[softwares[0]]['marker']])
            if api_response[0] == True:
                registrations[softwares[0]]['consistency'] = True
                registrations[softwares[0]]['project'] = api_response[1]['id']
                ensure_repo(registrations[softwares[0]]['name'])
                write_reg(registrations)
                print "The associated project metadata is now consistent."
            else:
                print "--> Consistency alignment between registration\
                    and project metada failed. Please check connectivity\
                    and try to sync the software again later."
                print api_response[1]
        else:
            if len(softwares) > 0:
                print "The associated project metadata is already consistent."

            else:
                print "Error: No registration with this name."

def unregister(name=None, marker=None):
    print "Unregistering the software..."
    registrations = read_reg()
    softwares = find_by(regs=registrations, name=name, marker=marker)
    if len(softwares) > 0 and registrations[softwares[0]]['status']['value'] != 'unregistered':
        registrations[softwares[0]]['history'].append(registrations[softwares[0]]['status'])
        stamp = formated_stamp()
        registrations[softwares[0]]['history'].append(registrations[softwares[0]]['status'])
        registrations[softwares[0]]['status'] = {'value':'unregistered', 'stamp':stamp}
        write_reg(registrations)
        # Delete the .source
        # Delete software repo and section from registrations.
        print "Software unregistered."
    else:
        print "Could not found a software with\
        this name/marker to unregister."

def watcher_launch(name=None, marker=None):
    # from subprocess import call
    task_cmd = []
    task_cmd.append("python")
    task_cmd.append("-m")
    task_cmd.append("corr.corrTask")
    if name:
        task_cmd.append("--name")
        task_cmd.append(name)
    if marker:
        task_cmd.append("--marker")
        task_cmd.append(marker)
    # call(task_cmd)
    try:
        import subprocess
        process = subprocess.Popen(task_cmd)
        # print process.stdout
        return process
    except:
        return None

def watcher_stop(reg=None):
    task_cmd = []
    task_cmd.append("sudo")
    task_cmd.append("-S")
    task_cmd.append("kill")
    task_cmd.append("-9")
    task_cmd.append(str(reg['watcher']))
    print "Unwatching on task-[{0}]...".format(str(reg['watcher']))
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

def watch(name=None, marker=None):
    registrations = read_reg()
    softwares = find_by(regs=registrations, name=name, marker=marker)
    # print str(registrations[softwares[0]])
    if len(softwares) > 0 and registrations[softwares[0]]['status']['value'] != 'unregistered':
        if registrations[softwares[0]]['status']['value'] == 'watching':
            print "Already watching this entry."
        else:
            registrations[softwares[0]]['history'].append(registrations[softwares[0]]['status'])
            stamp = formated_stamp()
            registrations[softwares[0]]['history'].append(registrations[softwares[0]]['status'])
            registrations[softwares[0]]['status'] = {'value':'watching', 'stamp':stamp}
            task_process = watcher_launch(
                name=registrations[softwares[0]]['name'],
                marker=registrations[softwares[0]]['marker'])
            if task_process:
                print "Watching on task-[{0}]...".format(int(task_process.pid))
                registrations[softwares[0]]['watcher'] = int(task_process.pid) + 4
                write_reg(registrations)
                print "Watching the software..."
            else:
                print "Error: Could not stop this watcher."
    else:
        print "Could not found this software to watch."

def unwatch(name=None, marker=None):
    registrations = read_reg()
    softwares = find_by(regs=registrations, name=name, marker=marker)
    if len(softwares) > 0 and registrations[softwares[0]]['status']['value'] != 'unregistered':
        if registrations[softwares[0]]['status']['value'] == 'watching':
            registrations[softwares[0]]['history'].append(registrations[softwares[0]]['status'])
            stamp = formated_stamp()
            registrations[softwares[0]]['history'].append(registrations[softwares[0]]['status'])
            registrations[softwares[0]]['status'] = {'value':'unwatched', 'stamp':stamp}
            stop_process = watcher_stop(reg=registrations[softwares[0]])
            if stop_process:
                registrations[softwares[0]]['watcher'] = None
                write_reg(registrations)
                print "Software unwatched"
            else:
                print "Error: Could not stop this watcher."
        elif registrations[softwares[0]]['status']['value'] == 'unwatched':
            print "Already unwatched this entry."
    else:
        print "Could not found this software to unwatch."

def push_file(path=None, obj=None, group=None):
    config = read_config()
    api_response = api.upload_file(config=config, path=path, obj=obj, group=group)
    if api_response[0]:
        print "File uploaded."
    else:
        print "File upload failed."
        print api_response[1]

def push_env(name=None, marker=None, path=None):
    config = read_config()
    registrations = read_reg()
    softwares = find_by(regs=registrations, name=name, marker=marker)
    if len(softwares) > 0 and registrations[softwares[0]]['status']['value'] != 'unregistered':
        if registrations[softwares[0]]['status']['value'] == 'watching':
            print "Error: Uploading new environment while watching is not possible. Unwatch first."
        else:
            api_response = api.project_env_next(
                config=config,
                project=registrations[softwares[0]]['project'],
                path=path)
            if api_response[0]:
                print "Environment successfully pushed."
            else:
                print "Error: Environment push failed."
                print api_response[1]
