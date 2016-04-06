import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v1/admin"
headers = {"Accept": "application/json"}

def app_create(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/app/create"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_show(app_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/app/show/%s"%(base, app_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def app_delete(app_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/app/delete/%s"%(base, app_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_apps():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/apps"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':


    app1 = {
        "developer":"56731c3a9f9d5110105a27f7",
        "name":"CoRR-Cmd",
        "about":"This application is the CoRR native client. It is an event based simulation management tool. It uses the system calls and processes table stack and some information extraction to make the record more sustainable and reusable. CoRR-Cmd support parallel and distributed simulation."
    }
    app2 = {
        "developer":"56731c3a9f9d5110105a27f7",
        "name":"Sumatra",
        "about":"Sumatra is a tool for managing and tracking projects based on numerical simulation and/or analysis, with the aim of supporting reproducible research. It can be thought of as an automated electronic lab notebook for computational projects."
    }

    # print get_apps()

    # print app_create(app1)
    # print app_create(app2)

    # print get_apps()

    # print app_delete('56731d849f9d5110105a280b')
    # print app_delete('56731d859f9d5110105a280f')

    # print get_apps()

    print app_show('56731d849f9d5110105a280b')
    print app_show('56731d859f9d5110105a280f')
