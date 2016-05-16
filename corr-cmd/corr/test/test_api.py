from corr.main import api
from corr.main import core
import pkg_resources
import imp
import json
from ..test import api_key

class TestApi:
 
    def test_api_status(self):
        config = {'default':{'api':{}}}
        config['default']['api']['host'] = '0.0.0.0'
        config['default']['api']['port'] = 5100
        config['default']['api']['key'] = api_key
        assert api.api_status(host=config['default']['api']['host'], port=config['default']['api']['port']) == True
        assert api.api_status(config=config['default']) == True
    