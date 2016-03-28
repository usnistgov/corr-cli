import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v0.1/87b7188171a6f6eed3ce7591ec175fe0e088e43cb282fa21a13a54d07826a073/admin"
headers = {"Accept": "application/json"}

def record_create(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/record/create"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def record_show(record_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/record/show/%s"%(base, record_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def record_update(record_id="", data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/record/update/%s"%(base,record_id), json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def record_delete(record_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/record/delete/%s"%(base, record_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_records():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/records"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':

    record1 = {
        "project":"56f161539f9d51478c0a7c45",
        "app_token":"dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a",
        "system":{
            "architecture_bits": "64bit",
            "architecture_linkage": "ELF",
            "ip_addr": "127.0.0.1",
            "machine": "x86_64",
            "network_name": "606d8d28528d",
            "processor": "Intel Core i7-4470HQ CPU @ 2.20Ghz x 8",
            "gpu":"Intel Iris Pro Graphics 5200 (GT3 + 128 MB eDRAM)",
            "release": "3.19.0-18-generic",
            "system_name": "Linux",
            "distribution": "Ubuntu 15.04",
            "version": "#18-Ubuntu SMP Tue May 19 18:31:35 UTC 2015"
        },
        "inputs":[
            {
                "parameters": {

                    "content": "modulus = 100, 120 # Elastic modulus\nratio = 0.3, 0.3 # Poissons ratio\nstrain = 0.02 # Macro strain\nsize = 21, 21 # Microstructure size",
                    "type": "SimpleParameterSet"
                }
            },
            {
                "script_arguments": "<parameters>"
            }
        ],
        "outputs":[
            {
                "creation": "2015-07-01 04:53:59",
                "digest": "43a47cb379df2a7008fdeb38c6172278d000fdc4",
                "metadata": {
                    "encoding": '',
                    "mimetype": '',
                    "size": 2500
                },
                "path": "example2.dat"
            }
        ],
        "dependencies":[
            {
                "diff": "",
                "module": "python",
                "name": "_markerlib",
                "path": "/usr/lib/python2.7/dist-packages/_markerlib",
                "source": '',
                "version": "unknown"
            },
            {
                "diff": "",
                "module": "python",
                "name": "numpy",
                "path": "/usr/lib/python2.7/dist-packages/numpy",
                "source": "attribute",
                "version": "1.8.2"
            },
            {
                "diff": "",
                "module": "python",
                "name": "pymks",
                "path": "/usr/lib/python2.7/dist-packages/pymks",
                "source": "attribute",
                "version": "0.2.3"
            },
            {
                "diff": "",
                "module": "python",
                "name": "setuptools",
                "path": "/usr/lib/python2.7/dist-packages/setuptools",
                "source": "attribute",
                "version": "3.3"
            }
        ],
        "status":"running",
        "rationels":[
            "Compute the linear strain field for a two phase composite material",
            "Linear Elasticity in 2D"
        ]
    }

    record2 = {
        "project":"56f161539f9d51478c0a7c47",
        "app_token":"a07e6c383a5ce8ba4497c6ebce2c6ed065b1cf20a4a57d263932187d7b85b655",
        "system":{
            "machine": "TGA",
            "characteristics": "20C_45Bar",
            "model": ""
        },
        "inputs":[
            {
                "absorbate": "CO2",
                "sample": {
                    "lot": "20 degC (Repeat with HT outgas)",
                    "name": "RM8852 with UHPCO2 up to 45 bar"
                }
            }
        ],
        "outputs":[
            {
                "digest": "43a47cb379df2a7008fdeb38c6172278d000fdc4",
                "metadata": {
                    "encoding": '',
                    "mimetype": '',
                    "size": 2500
                },
                "path": "/Experiments/8852_Aliq2_CO2_20C_45Bar_TGA.xlsx"
            }
        ],
        "status":"starting",
        "rationels":[
            "Aliq #2 with Kalrez (Jarod)",
            "JH"
        ]
    }

    record3 = {
        "project":"56f161539f9d51478c0a7c47",
        "app_token":"a07e6c383a5ce8ba4497c6ebce2c6ed065b1cf20a4a57d263932187d7b85b655",
        "system":{
            "machine": "IGA",
            "characteristics": "20C_20BAR",
            "model": ""
        },
        "inputs":[
            {
                "absorbate": "CO2",
                "sample": {
                    "lot": "Sample73 with 20C",
                    "name": "CO2 Aliq2 Sample73"
                }
            }
        ],
        "outputs":[
            {
                "digest": "43a47cb379df2a7008fdeb38c6172278d000fdc4",
                "metadata": {
                    "encoding": '',
                    "mimetype": '',
                    "size": 2500
                },
                "path": "/Experiments/CO2_20C_20BAR_Aliq2_Sample73_IGA.xlsx"
            }
        ],
        "status":"starting",
        "rationels":[
            "Unknown pressure up to 20BAR"
        ]
    }

    record4 = {
        "project":"56f161539f9d51478c0a7c49",
        "system":{
            "architecture_bits": "64bit",
            "architecture_linkage": "ELF",
            "ip_addr": "127.0.0.1",
            "machine": "x86_64",
            "network_name": "606d8d28528d",
            "processor": "Intel Core i7-4470HQ CPU @ 2.20Ghz x 8",
            "gpu":"Intel Iris Pro Graphics 5200 (GT3 + 128 MB eDRAM)",
            "release": "3.19.0-18-generic",
            "system_name": "Linux",
            "distribution": "Ubuntu 15.04",
            "version": "#18-Ubuntu SMP Tue May 19 18:31:35 UTC 2015"
        },
        "inputs":[
            {
                "script_arguments": "<parameters>"
            }
        ],
        "outputs":[
            {
                    "stdout_stderr": "Not launched."
            },
            {
                "stdout_stderr": "No output."
            }
        ],
        "dependencies":[
            {
                "diff": "",
                "module": "python",
                "name": "_markerlib",
                "path": "/usr/lib/python2.7/dist-packages/_markerlib",
                "source": '',
                "version": "unknown"
            },
            {
                "diff": "",
                "module": "python",
                "name": "numpy",
                "path": "/usr/lib/python2.7/dist-packages/numpy",
                "source": "attribute",
                "version": "1.8.2"
            },
            {
                "diff": "",
                "module": "python",
                "name": "fipy",
                "path": "/usr/lib/python2.7/dist-packages/fipy",
                "source": "attribute",
                "version": "3.1"
            },
            {
                "diff": "",
                "module": "python",
                "name": "setuptools",
                "path": "/usr/lib/python2.7/dist-packages/setuptools",
                "source": "attribute",
                "version": "3.3"
            }
        ],
        "status":"starting",
        "rationels":[
            "First record",
            "Simple example for integration",
            "Crank-Nicholson transient diffusion"
        ]
    }

    # print get_records()

    # print record_create(record1)
    # print record_create(record2)
    # print record_create(record3)
    # print record_create(record4)

    # print get_records()

    print record_update('56f166ff9f9d51486c4fac3b', {'access':'public'})
    print record_update('56f166ff9f9d51486c4fac3e', {'access':'public'})
    print record_update('56f166ff9f9d51486c4fac40', {'access':'public'})
    print record_update('56f166ff9f9d51486c4fac42', {'access':'public'})

    print record_show('56f166ff9f9d51486c4fac3b')
    print record_show('56f166ff9f9d51486c4fac3e')
    print record_show('56f166ff9f9d51486c4fac40')
    print record_show('56f166ff9f9d51486c4fac42')

    # print record_delete('56f166ff9f9d51486c4fac3b')
    # print record_delete('56f166ff9f9d51486c4fac3e')
    # print record_delete('56f166ff9f9d51486c4fac40')
    # print record_delete('56f166ff9f9d51486c4fac42')