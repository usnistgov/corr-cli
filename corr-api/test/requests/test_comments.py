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
        "sender":"fbff9b2fcd8f56a3ceda3353eee12c1f01ef9cd95ac7386b6f88b3149cfc40f1",
        "item":"567322d09f9d5113c3a63dea",
        "title":"This is a simple comment from user2 on the record",
        "content":"What do you think about my comment user1?"
    }
    comment2 = {
        "sender":"f84375c011876a6f2e8721de682f2781cc4b85f76e9d305cae33564e07b6f275",
        "item":"567322d09f9d5113c3a63dea",
        "title":"This is a simple comment to user2 on the record",
        "content":"Ask me something interesting user2."
    }
    comment3 = {
        "sender":"fbff9b2fcd8f56a3ceda3353eee12c1f01ef9cd95ac7386b6f88b3149cfc40f1",
        "item":"567322d09f9d5113c3a63dea",
        "title":"This is now a comment on the MKS project",
        "content":"User1, Can we do some phase field simulations with PyMKS?"
    }


    # print get_comments()

    # print comment_all('record', '567322d09f9d5113c3a63dea')

    # print comment_post('record', comment1)
    # print comment_post('record', comment2)
    # print comment_post('record', comment3)

    # print get_comments()

    print comment_all('record', '567322d09f9d5113c3a63dea')

    # print comment_show('5672e33e9f9d517f6c2fcfb7')
    # print comment_show('5672e33e9f9d517f6c2fcfb8')
    # print comment_show('5672e33e9f9d517f6c2fcfb9')
