import httplib
import json

base = "/api/v0.1/87b7188171a6f6eed3ce7591ec175fe0e088e43cb282fa21a13a54d07826a073/admin"
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
