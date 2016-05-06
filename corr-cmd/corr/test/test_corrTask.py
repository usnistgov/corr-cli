from corr.main.coRRTask import CoRRTask
from corr.main import coreLink
from corr.main import api
from corr.main import core
import pkg_resources
import imp
import json

class TestCorrTask:
 
    def test_api_status(self):
        elnk_module = core.extend_load('corr.main.coreLink')
        api_module = core.extend_load('corr.main.api')
        tag = None
        reg_resp = coreLink.register(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert reg_resp != None
        tag_resp = coreLink.tag(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert tag_resp != None
        shw_resp = coreLink.show(name='execution', tag=tag_resp, api='corr.main.api', elnk='corr.main.coreLink')
        assert shw_resp != None

        # check what is the latest record now

        corr_path = imp.find_module('corr')[1]
        task_cmd = []
        task_cmd.append('python')
        task_cmd.append('{0}/data/execution.py'.format(corr_path))
        task_cmd.append(tag)
        process = subprocess.Popen(task_cmd)
        tsk = CoRRTask(name='execution', tag=tag_resp, api_module=api_module, elnk_module=elnk_module)
        tsk.run()

        # wait for xxx seconds

        # check that the latest record changed. one more record.
        
