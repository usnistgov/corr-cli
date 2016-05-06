from corr.main import coreLink
from corr.main import core
import pkg_resources
import imp
import json

class TestCore:
 
    def test_configure(self):
        config = {'default':{'api':{}}}
        assert core.pretty_json(config) == coreLink.configure()

        config['default']['api']['host'] = '0.0.0.0'
        config['default']['api']['port'] = 5100
        config['default']['api']['key'] = '8c27a5c8d508cc10da0ea91412d726479996bdcad05421a6fc815d974ae22ade'
        coreLink.configure(host=config['default']['api']['host'], port=config['default']['api']['port'], key=config['default']['api']['key'])
        assert core.pretty_json(config) == coreLink.configure()
