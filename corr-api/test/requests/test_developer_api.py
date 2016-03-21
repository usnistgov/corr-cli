import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v0.1"
headers = {"Accept": "application/json"}

def get_apps():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/c81422a6752a34539a78bcdf90153944611bd0a4088efc800c1cc6a57bb02682/developer/apps"%(base))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_access(app_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/c81422a6752a34539a78bcdf90153944611bd0a4088efc800c1cc6a57bb02682/developer/app/access/%s"%(base, app_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_connectivity(app_token=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/app/connectivity"%(base, app_token))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_search(app_name=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/c81422a6752a34539a78bcdf90153944611bd0a4088efc800c1cc6a57bb02682/developer/app/search/%s"%(base, app_name))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    print get_apps()
    print app_access('56f0065f9f9d5179bb5569c6')

    print app_connectivity('9646216f8e0001cc4bd26dd6fcd213b50f4e44ddeee74c78436677bebc67aee9')
    print app_search('CoRR-Cmd')
    #Get logo
    #http://0.0.0.0:5100/api/v0.1/c81422a6752a34539a78bcdf90153944611bd0a4088efc800c1cc6a57bb02682/developer/app/logo/56f0065f9f9d5179bb5569c6

    
