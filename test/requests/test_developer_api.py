import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v1/private"
headers = {"Accept": "application/json"}

def get_apps():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/07366337c49a026cda30d1cb99679a1b86f7dffb9a44cf9765975a5991d6a849/applications"%(base))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_access(app_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/07366337c49a026cda30d1cb99679a1b86f7dffb9a44cf9765975a5991d6a849/application/access/%s"%(base, app_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_connectivity(app_token=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/connectivity"%(base, app_token))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_search(app_name=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/07366337c49a026cda30d1cb99679a1b86f7dffb9a44cf9765975a5991d6a849/application/search/%s"%(base, app_name))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    print get_apps()
    print app_access('56731d859f9d5110105a280f')

    print app_connectivity('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    print app_search('Sumatra')
    #Get logo
    #http://0.0.0.0:5100/api/v1/private/07366337c49a026cda30d1cb99679a1b86f7dffb9a44cf9765975a5991d6a849/application/logo/56731d849f9d5110105a280b

    
