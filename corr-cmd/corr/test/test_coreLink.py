from corr.main import coreLink
from corr.main import core
import pkg_resources
import subprocess
import imp
import json

class TestCoreLink:
    def __init__(self):
        self.tag = None
 
    def test_configure(self):
        config = {'default':{'api':{}}}
        config['default']['api']['host'] = '0.0.0.0'
        config['default']['api']['port'] = 5100
        config['default']['api']['key'] = '8c27a5c8d508cc10da0ea91412d726479996bdcad05421a6fc815d974ae22ade'
        coreLink.configure(host=config['default']['api']['host'], port=config['default']['api']['port'], key=config['default']['api']['key'])
        assert core.pretty_json(config) == coreLink.configure()

    def test_align(self):
        self.tag = None
        align_resp = coreLink.align(api='corr.main.api', elnk='corr.main.coreLink')
        assert align_resp == True

    def test_register(self):
        reg_resp = coreLink.register(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert reg_resp != None

    def test_tag(self):
        tag_resp = coreLink.tag(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert tag_resp != None

    def test_list(self):
        list_resp = coreLink.list(api='corr.main.api', elnk='corr.main.coreLink')
        assert len(list_resp) > 0

    def test_show(self):
        show_resp = coreLink.show(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert show_resp != None

    def test_sync(self):
        sync_resp = coreLink.sync(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert sync_resp != None
        sync_resp = coreLink.sync(api='corr.main.api', elnk='corr.main.coreLink')
        assert sync_resp != None

    def test_unregister(self):
        unreg_resp = coreLink.unregister(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert unreg_resp == True

    def test_watch_unwatch(self):
    	reg_resp = coreLink.register(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert reg_resp != None
        tag_resp = coreLink.tag(name='execution', api='corr.main.api', elnk='corr.main.coreLink')
        assert tag_resp != None
        self.tag = tag_resp[0]
        corr_path = imp.find_module('corr')[1]
        task_cmd = []
        task_cmd.append('python')
        task_cmd.append('{0}/data/execution.py'.format(corr_path))
        task_cmd.append(self.tag)
        watch_resp = coreLink.watch(name='execution', tag=self.tag, api='corr.main.api', elnk='corr.main.coreLink', ctsk='corr.main.corrTask')
        # print watch_resp[1]
        assert watch_resp[0] == True
        unwatch_resp = coreLink.unwatch(name='execution', tag=self.tag, api='corr.main.api', elnk='corr.main.coreLink', ctsk='corr.main.corrTask')
        # print unwatch_resp[1]
        assert unwatch_resp[0] == True
