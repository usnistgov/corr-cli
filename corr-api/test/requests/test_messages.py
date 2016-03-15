import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v1/admin"
headers = {"Accept": "application/json"}

def message_create(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/message/create"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def message_show(message_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/message/show/%s"%(base, message_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def message_update(message_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/message/update/%s"%(base,message_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def message_delete(message_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/message/delete/%s"%(base, message_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_messages():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/messages"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    message1 = {
        "sender":"f84375c011876a6f2e8721de682f2781cc4b85f76e9d305cae33564e07b6f275",
        "receiver":"56731c3a9f9d5110105a27f4",
        "title":"Duplicated - Hello User2",
        "content":"It is user 1 and i was wondering if you had any record on some DFT simulations.Thanks, User1"
    }

    message2 = {
        "sender":"fbff9b2fcd8f56a3ceda3353eee12c1f01ef9cd95ac7386b6f88b3149cfc40f1",
        "receiver":"56731c3a9f9d5110105a27f1",
        "title":"Duplicated - Re - Hello User2",
        "content":"Hi user1, I am sorry but i currently do not have any exemple with some DFT simulations. Are you interested into collaborating in one? Thank you, User2"
    }

    message3 = {
        "sender":"f84375c011876a6f2e8721de682f2781cc4b85f76e9d305cae33564e07b6f275",
        "receiver":"56731c3a9f9d5110105a27f4",
        "title":"Duplicated - Test message",
        "content":"This is just a test message from user2."
    }

    # print get_messages()

    # print message_create(message1)
    # print message_create(message2)
    # print message_create(message3)

    # print get_messages()

    print message_show('567326ca9f9d5114f35257e1')
    print message_show('567326ca9f9d5114f35257e4')
    print message_show('567326ca9f9d5114f35257e7')

    message3['title'] = 'Your impressions about this platform.'
    message3['content'] = 'What do you think about CoRR?'

    print message_update('567326ca9f9d5114f35257e7', message3)

    print message_show('567326ca9f9d5114f35257e7')

    # print message_delete('567326ca9f9d5114f35257e1')
    # print message_delete('567326ca9f9d5114f35257e4')
