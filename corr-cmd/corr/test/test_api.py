from corr.main import api
from corr.main import core
import pkg_resources
import imp
import json

class TestApi:
 
    def test_api_status(self):
        config = {'default':{'api':{}}}
        config['default']['api']['host'] = '0.0.0.0'
        config['default']['api']['port'] = 5100
        config['default']['api']['key'] = '8c27a5c8d508cc10da0ea91412d726479996bdcad05421a6fc815d974ae22ade'
        assert api.api_status(config=config['default']) == True
        assert api.api_status(host=config['default']['api']['host'], port=config['default']['api']['port']) == True

    