from corr.main.execLink import ExecLink
from corr.main import core
import pkg_resources
import imp
import json
import subprocess
from time import sleep
import sys, traceback
import os
import signal

class TestExecLink:
 
    def test_record(self):
        tag = 'execution-tag-{0}'.format(core.formated_stamp())
        corr_path = imp.find_module('corr')[1]
        task_cmd = []
        task_cmd.append('python')
        task_cmd.append('{0}/data/execution.py'.format(corr_path))
        task_cmd.append(tag)
        process = subprocess.Popen(task_cmd)
        elnk = ExecLink(tag=tag, watcher='CoRRTask')
        record = None
        for trial in range(10):
            try:
                record = elnk.record()
                sleep(2)
                if record != None:
                    break
            except:
                pass
        assert record != None


