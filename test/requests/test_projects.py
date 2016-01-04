import httplib
import json

# conn = httplib.HTTPSConnection("http://0.0.0.0:5100")
base = "/api/v1/admin"
headers = {"Accept": "application/json"}

def project_create(data={}):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("POST","%s/project/create"%base, json.dumps(data), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def project_show(project_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/project/show/%s"%(base, project_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def project_delete(project_id=""):
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/project/delete/%s"%(base, project_id))
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def get_projects():
    conn = httplib.HTTPConnection("0.0.0.0", 5100)
    conn.request("GET","%s/projects"%base)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == '__main__':


    project1 = {
        "api_token":"2af0482f74dc27040b81bcbd0d69bfe85381c9026b0edaa194a0c2a69e1f0c9f",
        "app_token":"dad86479d3f0e4b1c6ed17b8ab02a9df4fa65e61761d5952f45770c19fb5194a",
        "name":"Materials Knowledge Systems in Python",
        "description":"The Materials Knowledge Systems (MKS) is a novel data science approach for solving multiscale materials science problems. It uses techniques from physics, machine learning, regression analysis, signal processing, and spatial statistics to create structure-property-processing relationships. The MKS carries the potential to bridge multiple length scales using localization and homogenization linkages, and provides a data driven framework for solving inverse material design problems.",
        "goals":"The Materials Knowledge Materials in Python (PyMKS) framework is an object oriented set of tools and examples written in Python that provide high level access to the MKS framework for rapid creation and analysis of structure-property-processing relationships. A short intoduction of how to use PyMKS is outlined below and example cases can be found in the examples section. Both code and example contributions are welcome.",
        "tags":["multiscale","materials science","physics","machine learning","regression analysis","signal processing","spatial statistics","MGI","NIST","Georgia Tech"],
        "group":"computational"
    }
    project2 = {
        "api_token":"ce967787f485d8cb0baeceeec0fecab5df37a297b373178684c4d2cf13345d7f",
        "app_token":"a07e6c383a5ce8ba4497c6ebce2c6ed065b1cf20a4a57d263932187d7b85b655",
        "name":"Facility for Adsorbent Characterization and Testing",
        "description":"The NIST Facility for Adsorbent Characterization and Testing (FACT) is a state-of-the-art laboratory recently commissioned with support from the U.S. Department of Energy's Advanced Research Projects Agency-Energy (ARPA-E) to address the challenges inherent to measuring gas and vapor sorption properties.",
        "goals":"FACT supports programs developing adsorbents and serves the sorbent materials research community by providing impartial testing and characterization of material sorption properties, establishing testing procedures, and disseminating reliable sorbent material property data and measurement best practices.",
        "tags":["adsorbent","DoE","ARPA-E","gas","vapor","sorption","materials research","measurement","NIST"],
        "group":"experimental"
    }

    project3 = {
        "api_token":"ce967787f485d8cb0baeceeec0fecab5df37a297b373178684c4d2cf13345d7f",
        "name":"FiPy: A Finite Volume PDE Solver Using Python",
        "description":"FiPy is an object oriented, partial differential equation (PDE) solver, written in Python, based on a standard finite volume (FV) approach. The framework has been developed in the Materials Science and Engineering Division (MSED) and Center for Theoretical and Computational Materials Science (CTCMS), in the Material Measurement Laboratory (MML) at the National Institute of Standards and Technology (NIST).",
        "goals":"The solution of coupled sets of PDEs is ubiquitous to the numerical simulation of science problems. Numerous PDE solvers exist, using a variety of languages and numerical approaches. Many are proprietary, expensive and difficult to customize. As a result, scientists spend considerable resources repeatedly developing limited tools for specific problems. Our approach, combining the FV method and Python, provides a tool that is extensible, powerful and freely available. A significant advantage to Python is the existing suite of tools for array calculations, sparse matrices and data rendering.",
        "tags":["python","materials science","PDE","MML","MSED","CTCMS","transent diffusion","convection","NIST","standard resources","coupled elliptic","hyperbolic","parabolic"],
        "group":"computational"
    }

    # print get_projects()

    # print project_create(project1)
    # print project_create(project2)
    # print project_create(project3)

    # print get_projects()

    print project_show('567321a49f9d511391055d1c')
    print project_show('567321a49f9d511391055d20')
    print project_show('56732a619f9d5116675d11b6')

    # print project_delete('567321a49f9d511391055d1c')
    # print project_delete('567321a49f9d511391055d20')
    # print project_delete('56732a619f9d5116675d11b6')
