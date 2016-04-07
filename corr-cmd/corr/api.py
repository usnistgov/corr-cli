import httplib
import json
import traceback
import requests

def api_status(config=None, host=None, port=None):
    if host is None or port is None:
        try:
            conn = httplib.HTTPConnection(config['api']['host'], int(config['api']['port']))
        except:
            return False
    else:
        conn = httplib.HTTPConnection(host, int(port))

    conn.request("GET", "/api/v0.1/public/api/status")
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 200:
            return True
        else:
            return False
    except:
        return False

def project_create(config=None, name=None, description='', goals='',
                   tags=[], access='private', group='computational'):
    if api_status(config=config):
        conn = httplib.HTTPConnection(config['api']['host'], int(config['api']['port']))
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    request = {}
    request['name'] = name
    request['description'] = description
    request['goals'] = goals
    request['tags'] = tags
    request['access'] = access
    request['group'] = group
    conn.request(
        "POST", 
    	   "/api/v0.1/private/{0}/no-app/project/create".format(config['api']['key']), 
    	   json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def project_all(config=None):
    if api_status(config=config):
        conn = httplib.HTTPConnection(config['api']['host'], int(config['api']['port']))
    else:
        return [False, 'No configured api.']

    conn.request("GET", "/api/v0.1/private/{0}/no-app/projects".format(config['api']['key']))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 200:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def record_create(config=None, project=None, request={}):
    if api_status(config=config):
        conn = httplib.HTTPConnection(config['api']['host'], int(config['api']['port']))
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    conn.request(
        "POST",
        "/api/v0.1/private/{0}/no-app/project/record/create/{1}".format(
            config['api']['key'], project), json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def record_update(config=None, record=None, request={}):
    if api_status(config=config):
        conn = httplib.HTTPConnection(config['api']['host'], int(config['api']['port']))
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    conn.request(
        "POST",
        "/api/v0.1/private/{0}/no-app/record/update/{1}".format(
            config['api']['key'], record), json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]

def upload_file(config=None, path=None, obj=None, group=None):
    if api_status(config=config):
        if path and group and obj:
            url = "http://{0}:{1}/api/v0.1/private/{2}/no-app/file/upload/{3}/{4}".format(
                config['api']['host'], int(config['api']['port']),
                config['api']['key'], group, obj)
        else:
            return [False, 'Required path, obj and group.']
    else:
        return [False, 'No configured api.']

    files = {'file': open('{0}'.format(path))}
    response = requests.post(url, files=files)
    data = response.content

    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            return [True, data_json['content']]
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]


def project_env_next(config=None, project=None, path=None):
    if api_status(config=config):
        conn = httplib.HTTPConnection(config['api']['host'], int(config['api']['port']))
    else:
        return [False, 'No configured api.']

    headers = {"Accept": "application/json"}
    request = {
        "group":"computational",
        "system":"tool-based",
        "specifics":{'tool':'corr-cmd', 'version':'0.1'},
        "version":{},
        "bundle":{}
    }
    conn.request(
        "POST",
        "/api/v0.1/private/{0}/no-app/project/env/next/{1}".format(
            config['api']['key'], project), json.dumps(request), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    try:
        data_json = json.loads(data)
        if data_json['code'] == 201:
            upload_response = upload_file(
                config=config, path=path, 
                obj=data_json['content']['bundle'], group='bundle')
            if upload_response[0]:
                return [True, data_json['content']]
            else:
                return upload_response
        else:
            return [False, data_json['content']]
    except:
        return [False, str(traceback.print_exc())]



