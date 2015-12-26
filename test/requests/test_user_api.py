import httplib
import json
import re
import requests

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v1/private/2af0482f74dc27040b81bcbd0d69bfe85381c9026b0edaa194a0c2a69e1f0c9f"
headers = {"Accept": "application/json"}

def user_status(app_token=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/user/status"%(base, app_token))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_home(app_token=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/user/home"%(base, app_token))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_search(app_token="", user_name=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/user/search/%s"%(base, app_token, user_name))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_app_connectivity(app_token=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/connectivity"%(base, app_token))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

# Messages
def user_message_create(app_token="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/%s/message/create"%(base, app_token), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_message_show(app_token="", message_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/message/show/%s"%(base, app_token, message_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_message_update(app_token="", message_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/%s/message/update/%s"%(base, app_token,message_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_message_delete(app_token="", message_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/message/delete/%s"%(base, app_token, message_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_get_messages(app_token=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/messages"%(base, app_token))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

# Files
def user_file_create(app_token="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/%s/file/create"%(base, app_token), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_file_show(app_token="", file_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/file/show/%s"%(base, app_token, file_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_file_update(app_token="", file_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/%s/file/update/%s"%(base, app_token,file_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_file_delete(app_token="", file_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/file/delete/%s"%(base, app_token, file_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def user_file_upload(app_token="", group='unknown', item_id="", file_name=""):
    url = "http://0.0.0.0:5100%s/%s/file/upload/%s/%s"%(base, app_token,group,item_id)
    files = {'file': open('%s'%file_name)}
    response = requests.post(url, files=files)
    return response.content

def user_file_download(app_token="", file_id=""):
    url = "http://0.0.0.0:5100%s/%s/file/download/%s"%(base, app_token, file_id)
    # conn = httplib.HTTPConnection("0.0.0.0", 5100)
    # conn.request("GET","%s/%s/file/download/%s"%(base, app_token, file_id))
    # response = conn.getresponse()
    response = requests.get(url)
    return "Headers: %s"%response.headers
    # content = response.content
    # d = response.headers['Content-Disposition']
    # fname = re.findall("filename=(.+)", d)
    # with open(fname, 'w') as downloaded_f:
    #     downloaded_f.write(content)
    # return '%s Downloaded'%fname

def user_get_files(app_token=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/%s/files"%(base, app_token))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    # print user_status('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    print user_home('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    # print user_search('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', 'User2-CoRR')
    # print user_search('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', 'CoRR')

    print user_app_connectivity('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    
    message1 = {
        "receiver":"56731c3a9f9d5110105a27f4",
        "title":"Test New Message 1",
        "content":"This is a test from user api."
    }

    message2 = {
        "receiver":"56731c3a9f9d5110105a27f4",
        "title":"Test New Message 2",
        "content":"This is another test from user api."
    }

    message3 = {
        "receiver":"56731c3a9f9d5110105a27f4",
        "title":"Test New Message 3",
        "content":"This is yet another test from user api."
    }

    # print user_get_messages('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    # print user_message_create('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', message1)
    # print user_message_create('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', message2)
    # print user_message_create('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', message3)
    # print user_get_messages('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    # print user_message_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8')
    # message3['content'] = 'This is yet another updated message done from the user api.'
    # print user_message_update('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8', message3)
    # print user_message_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8')
    # print user_message_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f7')
    # print user_message_delete('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f7')
    # print user_message_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f7')


    file1 = {
        "name":"Another reference to pymks-paper-2015.pdf",
        "storage":"566b18159f9d516b595d7e19_pymks-paper-2015.pdf",
        "group": "resource",
        "description":"This a resource pdf file of a PyMKS paper."
    }

    file2 = {
        "name":"An Introduction to Quantum Computing",
        "storage":"http://sergeev.fiz.univ.szczecin.pl/Dydaktyka/Wyklady/Kaye.pdf",
        "group": "file",
        "access": "private",
        "description":"We have offered a course at the University of Waterloo in quantum comput-\
                       ing since 1999. We have had students from a variety of backgrounds take the\
                       course, including students in mathematics, computer science, physics, and engi-\
                       neering. While there is an abundance of very good introductory papers, surveys\
                       and books, many of these are geared towards students already having a strong\
                       background in a particular area of physics or mathematics."
    }

    print user_get_files('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    print user_file_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '56743c0d9f9d5123f6d3effe')
    print user_file_download('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '56743c0d9f9d5123f6d3effe')
    # print user_file_create('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', file1)
    # print user_file_create('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', file2)
    # print user_get_files('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')

    print user_file_upload('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', 'attach', '567b106b9f9d517f31ec24f8', '0602096.pdf')
    print user_get_files('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a')
    # # Show the uploaded file and download it.
    # print user_file_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8')
    # print user_file_download('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8')

    #File 2 download
    # print user_file_download('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8')

    # file1['description'] = 'This is an updated description of the PyMKS paper.'
    # print user_file_update('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8', file1)
    # print user_file_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f8')

    # # File 1 delete
    # print user_file_delete('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f7')
    # print user_file_show('dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a', '567b106b9f9d517f31ec24f7')

    

