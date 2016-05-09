from corr.main.corrTask import CoRRTask
from corr.main import coreLink
from corr.main import api
from corr.main import core
import pkg_resources
import imp
import json
import subprocess

class TestCorrTask:
 
    def test_watch(self):
    	clnk_module = core.extend_load('corr.main.coreLink')
        elnk_module = core.extend_load('corr.main.execLink')
        api_module = core.extend_load('corr.main.api')
        tag = None
        align_resp = coreLink.align(api='corr.main.api', elnk='corr.main.coreLink')
        assert align_resp == True
        reg_resp = coreLink.register(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert reg_resp != None
        tag_resp = coreLink.tag(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert tag_resp != None
        tag = tag_resp[0]
        shw_resp = coreLink.show(name='execution', tag=tag, api='corr.main.api', elnk='corr.main.coreLink')
        assert shw_resp != None

        # check what is the latest record now

        corr_path = imp.find_module('corr')[1]
        task_cmd = []
        task_cmd.append('python')
        task_cmd.append('{0}/data/execution.py'.format(corr_path))
        task_cmd.append(tag)
        process = subprocess.Popen(task_cmd)
        tsk = CoRRTask(name='execution', tag=tag, clnk_module=clnk_module, api_module=api_module, elnk_module=elnk_module, timeout=30)
        records = tsk.run()
        assert len(records) > 0
        
