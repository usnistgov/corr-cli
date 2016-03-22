import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v0.1/87b7188171a6f6eed3ce7591ec175fe0e088e43cb282fa21a13a54d07826a073/admin"
headers = {"Accept": "application/json"}

def diff_create(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/diff/create"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def diff_show(diff_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/diff/show/%s"%(base, diff_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def diff_update(diff_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/diff/update/%s"%(base,diff_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def diff_delete(diff_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/diff/delete/%s"%(base, diff_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_diffs():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/diffs"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    diff1 = {
        "session":"5a630011e28d435cdd50e0b638f9c0e6931a2deeee07621d4fa1de9056b83096",
        "from":"56f166ff9f9d51486c4fac3e",
        "to":"56f166ff9f9d51486c4fac40",
        "method":"default",
        "proposition":"reproduced",
        "status":"proposed"
    }

    diff2 = {
        "session":"5a630011e28d435cdd50e0b638f9c0e6931a2deeee07621d4fa1de9056b83096",
        "from":"56f166ff9f9d51486c4fac3b",
        "to":"56f166ff9f9d51486c4fac42",
        "method":"visual",
        "proposition":"reproduced",
        "status":"proposed"
    }

    print get_diffs()

    print diff_create(diff1)
    print diff_create(diff2)

    print get_diffs()

    # print diff_show('56732d699f9d51177e642ee1')
    # print diff_show('56732d699f9d51177e642ee3')

    # diff2['status'] = 'agreed'

    # print diff_update('56732d699f9d51177e642ee3', diff2)

    # print diff_show('56732d699f9d51177e642ee3')

    # print diff_delete('56732d699f9d51177e642ee1')
    # print diff_delete('56732d699f9d51177e642ee3')
