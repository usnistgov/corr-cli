import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v0.1/admin"
headers = {"Accept": "application/json"}

def user_create(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/user/create"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_profile_create(user_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/user/profile/create/%s"%(base, user_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_profile_show(user_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/user/profile/show/%s"%(base, user_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_show(user_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/user/show/%s"%(base, user_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_login(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/user/login"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_users():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/users"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data
    
if __name__ == '__main__':
    user1 = {
        "email":"u1_corr@gmail.com",
        "password":"U12015",
        "passwordAgain":"U12015",
        "group":"user"
    }
    user2 = {
        "email":"u2_corr@gmail.com",
        "password":"U22015",
        "passwordAgain":"U22015",
        "group":"user"
    }
    dev1 = {
        "email":"d1_corr@gmail.com",
        "password":"D12015",
        "passwordAgain":"D12015",
        "group":"developer"
    }

    # print get_users()

    # resp1 = json.loads(user_create(user1))
    # resp2 = json.loads(user_create(user2))
    # resp3 = json.loads(user_create(dev1))

    # print resp1
    # print resp2
    # print resp3

    profile_user1 = {
        "fname":"User1",
		"lname":"CoRR",
		"about":"I am one of CoRR early stage User1."
    }
    profile_user2 = {
        "fname":"User2",
		"lname":"CoRR",
		"about":"I am one of CoRR early stage User2."
    }
    profile_dev1 = {
        "fname":"Developer1",
		"lname":"CoRR",
		"about":"I am one of CoRR early stage App developer1."
    }

    # if resp1['code'] == 201:
    #     print user_profile_create(resp1['content']['id'], profile_user1)
    #     del user1['group']
    #     resp11 = user_login(user1)
    #     print user_profile_show(resp1['content']['id'])
    # else:
    #     print '%d: %s'%(resp1['code'], resp1['content'])

    # if resp2['code'] == 201:
    #     print user_profile_create(resp2['content']['id'], profile_user2)
    #     del user2['group']
    #     resp21 = user_login(user2)
    #     print user_profile_show(resp2['content']['id'])
    # else:
    #     print '%d: %s'%(resp1['code'], resp1['content'])

    # if resp3['code'] == 201:
    #     print user_profile_create(resp3['content']['id'], profile_user3)
    #     del user3['group']
    #     resp31 = user_login(user3)
    #     print user_profile_show(resp3['content']['id'])
    # else:
    #     print '%d: %s'%(resp1['code'], resp1['content'])


    print user_profile_create('56731c3a9f9d5110105a27f1', profile_user1)
    print user_profile_create('56731c3a9f9d5110105a27f4', profile_user2)
    print user_profile_create('56731c3a9f9d5110105a27f7', profile_dev1)

    del user1['group']
    del user2['group']
    del dev1['group']

    print user_login(user1)
    print user_login(user2)
    print user_login(dev1)

    print user_profile_show('56731c3a9f9d5110105a27f1')
    print user_profile_show('56731c3a9f9d5110105a27f4')
    print user_profile_show('56731c3a9f9d5110105a27f7')

    