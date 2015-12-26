import httplib
import json
import requests

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v1/private/admin"
headers = {"Accept": "application/json"}

def file_create(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/file/create"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def file_show(file_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/file/show/%s"%(base, file_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def file_download(file_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/file/download/%s"%(base, file_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def file_update(file_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/file/update/%s"%(base,file_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def file_upload(group='unknown', item_id="", file_name=""):
    url = "http://0.0.0.0:5100%s/file/upload/%s/%s"%(base,group,item_id)
    files = {'file': open('%s'%file_name)}
    response = requests.post(url, files=files)
    return response.content

def file_delete(item_id="", file_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/file/delete/%s/%s"%(base, item_id, file_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_files():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/files"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    file1 = {
        "name":"566b18159f9d516b595d7e19_pymks-paper-2015.pdf",
        "storage":"566b18159f9d516b595d7e19_pymks-paper-2015.pdf",
        "location":"local",
        "group": "resource",
        "description":"This a resource pdf file of a PyMKS paper."
    }

    file2 = {
        "name":"logo.jpg",
        "storage":"logo.jpg",
        "location":"local",
        "group": "file",
        "description":"This the CoRR logo."
    }

    # print get_files()

    # print file_create(file1)
    # print file_create(file2)

    # print get_files()

    print file_show('56743c0d9f9d5123f6d3effe')
    # print file_show('56743c459f9d51240e66212f')

    # file2['description'] = 'This the CoRR jpg logo image file.'

    # print file_update('56743c459f9d51240e66212f', file2)

    # print file_show('56743c459f9d51240e66212f')

    # print file_upload('resource-app', '56731d849f9d5110105a280b', 'reproducibility.pptx')

    # print file_delete('56743c0d9f9d5123f6d3effe')
    # When a file is created with a reference to any item in the plaform. Its name does not have
    # A reference to an existing item so deleting it requires this trick.
    # A script to purge orphan files will follow this logic to clean the database and the storage.
    # print file_delete('logo.jpg', '56743c459f9d51240e66212f')
