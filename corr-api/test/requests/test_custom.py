import httplib
import json

base = "/api/v1/admin"
headers = {"Accept": "application/json"}

def user_home(comment_id=''):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/comment/show/%s"%(base, comment_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def index_html():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/traffic"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_traffic():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/traffic"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_stats():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/stats"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def clear_traffic():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/traffic/clear"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def clear_stats():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/stats/clear"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    print get_traffic()
    print get_stats()
