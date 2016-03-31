import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v0.1/87b7188171a6f6eed3ce7591ec175fe0e088e43cb282fa21a13a54d07826a073/admin"
headers = {"Accept": "application/json"}

def comment_post(group='unknown', data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/comment/%s"%(base, group), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def comment_show(comment_id=''):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/comment/show/%s"%(base, comment_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def comment_all(group='unknown', item_id=''):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/comment/all/%s/%s"%(base, group, item_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_comments():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/comments"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    comment1 = {
        "sender":"5a630011e28d435cdd50e0b638f9c0e6931a2deeee07621d4fa1de9056b83096",
        "item":"56f166ff9f9d51486c4fac3b",
        "title":"This is a simple comment from user2 on the record",
        "content":"What do you think about my comment user1?"
    }
    comment2 = {
        "sender":"5a630011e28d435cdd50e0b638f9c0e6931a2deeee07621d4fa1de9056b83096",
        "item":"56f166ff9f9d51486c4fac3b",
        "title":"This is a simple comment to user2 on the record",
        "content":"Ask me something interesting user2."
    }
    comment3 = {
        "sender":"5a630011e28d435cdd50e0b638f9c0e6931a2deeee07621d4fa1de9056b83096",
        "item":"56f166ff9f9d51486c4fac3b",
        "title":"This is now a comment on the MKS project",
        "content":"User1, Can we do some phase field simulations with PyMKS?"
    }


    print get_comments()

    print comment_all('record', '56f166ff9f9d51486c4fac3b')

    print comment_post('record', comment1)
    print comment_post('record', comment2)
    print comment_post('record', comment3)

    print get_comments()

    # print comment_all('record', '567322d09f9d5113c3a63dea')

    # print comment_show('5672e33e9f9d517f6c2fcfb7')
    # print comment_show('5672e33e9f9d517f6c2fcfb8')
    # print comment_show('5672e33e9f9d517f6c2fcfb9')
