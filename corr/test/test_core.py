from corr.main import core
import pkg_resources
import imp

class TestCore:
 
    def test_extend_load(self):
        coreLink_module = core.extend_load('corr.main.coreLink')
        assert coreLink_module.whois() == "CoreLink"
        
        corr_path = imp.find_module('corr')[1]
        extend_coreLink_module = core.extend_load('{0}/data/extend_CoreLink.py'.format(corr_path))
        assert extend_coreLink_module.whois() == "extend_CoreLink"