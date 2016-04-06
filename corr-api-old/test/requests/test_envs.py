import httplib
import json
import requests
import thread
import daemon

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v1/admin"
headers = {"Accept": "application/json"}

def update_env_bundle(bundle="", file_name=""):
    def handle_file_resolution(bundle, file_name):
        url = "http://0.0.0.0:5100%s/file/upload/bundle/%s"%(base, bundle)
        files = {'file': open('%s'%file_name)}
        response = requests.post(url, files=files)
        # print response.content
        with open('bundle-%s-upload.log'%bundle, 'w') as bundle_log:
            bundle_log.write(response.content)

    # handle_file_resolution(bundle, file_name)
    with daemon.DaemonContext():
        handle_file_resolution(bundle, file_name)
    # thread.start_new_thread(handle_file_resolution, (bundle, file_name,))
    # t = threading.Thread(target = handle_file_resolution, args=(bundle, file_name,)).start()    
    return 'Thread sheduled for upload!'

def project_env_next(project_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/project/env/next/%s"%(base, project_id), json.dumps(data), headers)
    response = conn.getresponse()
    print response.status
    data = response.read()
    conn.close()
    return data

def project_env_update(project_id="", env_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/project/env/update/%s/%s"%(base, project_id, env_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def project_envs(project_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/project/envs/%s"%(base, project_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def project_envs_head(project_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/project/envs/head/%s"%(base, project_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def project_env_show(project_id="", env_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/project/env/show/%s/%s"%(base, project_id, env_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    env1 = {
        "group":"computational",
        "system":"container-based",
        "specifics":{'container-system':'docker', 'container-version':'1.0'},
        "version":{
            "system":"git",
            "baseline":"develop",
            "marker":"9c264611cf9af99057ac31d3f863fa300da8e2d7"
        },
        "bundle":{
            "location":"https://s3-us-west-2.amazonaws.com/ddsm-bucket/5595f1b789adcc1556eb41cd-5597914cc922f075f076fa35-unknown.tar"
        }
    }
    env2 = {
        "group":"computational",
        "system":"container-based",
        "specifics":{'container-system':'docker', 'container-version':'1.0'},
        "version":{
            "system":"git",
            "baseline":"master",
            "marker":"35d3d3de724af4dec758be1c02fb56f0600b16b8"
        },
        "bundle":{
            "location":"https://s3-us-west-2.amazonaws.com/ddsm-bucket/5595f1b789adcc1556eb41cd-559aa346c922f009dbc3b872-unknown.tar"
        }
    }

    # print project_envs_head('567321a49f9d511391055d1c')
    # print project_envs_head('56732a619f9d5116675d11b6')

    # print project_envs('567321a49f9d511391055d1c')
    # print project_envs('56732a619f9d5116675d11b6')

    # print project_env_next('567321a49f9d511391055d1c', env1)
    # print project_env_next('56732a619f9d5116675d11b6', env2)

    # print project_envs_head('567321a49f9d511391055d1c')
    # print project_envs_head('56732a619f9d5116675d11b6')

    # print project_envs('567321a49f9d511391055d1c')
    # print project_envs('56732a619f9d5116675d11b6')

    # print project_env_show('567321a49f9d511391055d1c', '56747b939f9d51373dc0a5ea')
    print project_env_show('56732a619f9d5116675d11b6', '56747b939f9d51373dc0a5ed')
    print update_env_bundle('56747b939f9d51373dc0a5ef', '/home/fyc/Documents/Projects/NIST/CoRR/github/demo-sumatra.tar')
    # print update_env_bundle('56747b939f9d51373dc0a5ef', '/home/fyc/Documents/Projects/NIST/CoRR/github/presentation_11-23-2015.pdf')
    # print update_env_bundle('56747b939f9d51373dc0a5ef', '/home/fyc/Documents/Projects/NIST/CoRR/github/Howe_chapter.pdf')
    print project_env_show('56732a619f9d5116675d11b6', '56747b939f9d51373dc0a5ed')
    # env2['bundle']['location'] = "https://s3-us-west-2.amazonaws.com/ddsm-bucket/5595f1b789adcc1556eb41cd-5597914cc922f075f076fa35-unknown.tar"
    # print project_env_update('56732a619f9d5116675d11b6', '56747b939f9d51373dc0a5ed', env2)
    # print project_env_show('56732a619f9d5116675d11b6', '56747b939f9d51373dc0a5ed')

    # print project_show('567321a49f9d511391055d1c')
    # print project_show('567321a49f9d511391055d20')
    # print project_show('56732a619f9d5116675d11b6')

    # print project_delete('567321a49f9d511391055d1c')
    # print project_delete('567321a49f9d511391055d20')
    # print project_delete('56732a619f9d5116675d11b6')
