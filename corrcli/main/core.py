import sys
import os
import datetime
import traceback
import getpass
import json
# We have to add interoperate file.
import imp

corr_path = "%s/.corr"%os.path.expanduser('~')
config_path = "{0}/config.json".format(corr_path)
reg_path = "{0}/registrations.json".format(corr_path)
extend_path = "{0}/extensions.json".format(corr_path)
repos_path = "{0}/repositories".format(corr_path)
tasks_path = "{0}/tasks".format(corr_path)

def extend_load(module):
    if '.py' in module:
        alias = module.split('/')[-1].split('.')[0]
        return imp.load_source(alias, module)
    else:
        extension = None
        blocks = module.split('.')
        f, filename, description = imp.find_module('corr')
        extension = imp.load_module('corr', f, filename, description)
        try:
            for index in range(len(blocks)):
                if index > 0:
                    f, filename, description = imp.find_module(blocks[index], extension.__path__)
                    extension = imp.load_module('.'.join(blocks[0:index+1]), f, filename, description)
        finally:
            f.close()
        return extension


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
    try:
        if not os.path.exists(corr_path):
            os.makedirs(corr_path)

        if not os.path.exists(repos_path):
            os.makedirs(repos_path)

        if not os.path.exists(tasks_path):
            os.makedirs(tasks_path)

        if not os.path.isfile(reg_path):
            with open(reg_path, "w") as reg_file:
                reg_file.write(pretty_json({'default':[]}))

        if not os.path.isfile(extend_path):
            with open(extend_path, "w") as reg_file:
                reg_file.write(pretty_json({'coreLink':{'default':{}}, 'api':{'default':{}}, 'execLink':{'default':{}},  'corrTask':{'default':{}}}))

        if not os.path.isfile(config_path):
            with open(config_path, "w") as config_file:
                config_file.write(pretty_json({'default':{'api':{}}}))
        return True
    except:
        return False

def ensure_repo(name=None):
    ensure_root()
    if name != None:
        repo_path = "{0}/{1}.corr".format(repos_path, name)
        try:
            if not os.path.isfile(repo_path):
                with open(repo_path, "w") as repo_json:
                    repo_json.write(pretty_json({}))
            return True
        except:
            return False
    else:
        return False

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

def read_config(extend=None):
    try:
        ensure_root()
        config_json = {}
        with open(config_path, "r") as config_file:
            config_json = json.loads(config_file.read())
        if extend:
            try:
                return config_json[extend]
            except:
                return None
        else:
            return config_json
    except:
        return {}

def write_config(extend=None, config_json=None):
    try:
        ensure_root()
        with open(config_path, "w") as config_file:
            if extend:
                try:
                    config = read_config()
                    config[extend] = config_json
                    config_file.write(pretty_json(config))
                    return True
                except:
                    return False
            else:
                try:
                    config = read_config()
                    config['default'] = config_json
                    config_file.write(pretty_json(config))
                    return True
                except:
                    return False
    except:
        return False

def write_reg(extend=None, reg=[]):
    ensure_root()
    regs = read_reg()
    if extend:
        try:
            regs[extend] = reg
            with open(reg_path, "w") as reg_json:
                reg_json.write(pretty_json(regs))
            return True
        except:
            return False
    else:
        try:
            regs['default'] = reg
            with open(reg_path, "w") as reg_json:
                reg_json.write(pretty_json(regs))
            return True
        except:
            return False


def read_reg(extend=None):
    ensure_root()
    registrations = []
    with open(reg_path, "r") as reg_json:
        registrations = json.loads(reg_json.read())
    if extend:
        try:
            return registrations[extend]
        except:
            return registrations['default']
    else:
        return registrations

def write_extend(extends=[]):
    ensure_root()
    try:
        with open(extend_path, "w") as extend_json:
            reg_json.write(pretty_json(extends))
        return True
    except:
        return False

def read_extend():
    ensure_root()
    extends = []
    with open(extend_path, "r") as extend_json:
        extends = json.loads(extend_json.read())
    return extends

def extension_add(extensions=[], group='', impl=''):
    clnks = extensions[group]
    try:
        alias = impl.split('/')[-1].split('.')[0]
        existing = clnks[alias]
    except:
        existing = None
    if existing:
        # # print "A {0} with this alias already exists.".format(group)
        return existing
    else:
        clnks[alias] = {'path':impl}
        core.write_extend(clnks)
        return clnks[alias]

def extension_delete(extensions=[], group='', alias=''):
    clnks = extensions[group]
    try:
        existing = clnks[alias]
    except:
        existing = None
    if existing:
        del clnks[alias]
    else:
        # # print "No {0} with this alias found.".format(group)
        pass
    core.write_extend(clnks)

def extension_all(extensions=[]):
    # # print pretty_json(extensions)
    return pretty_json(extensions)

