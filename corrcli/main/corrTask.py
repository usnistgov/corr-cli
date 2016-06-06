import sys, traceback
import datetime
from time import sleep
import daemon
import click
from corr.main import core

class CoRRTask:
    def __init__(self, pid=None, name=None, refresh=10, aid=None, origin=None, tag=None, clnk_module=None, api_module=None, elnk_module=None, timeout=60*60):
        self.pid = pid
        self.origin = origin
        self.aid = aid
        self.name = name
        self.refresh = refresh
        self.root = None
        self.history = []
        self.tag = tag
        self.record = ''
        self.info = None
        self.timeout = timeout

        self.clnk_module = clnk_module
        self.link = elnk_module.ExecLink(tag=tag, watcher='corrTask')
        extensions = core.read_extend()

        self.api_module = api_module
        self.records = []
        self.request = {}
        self.ios = {'inputs':[], 'outputs':[]}

    def sync_io(self, config):
        for _input in self.ios['inputs']:
            api_response = self.api_module.upload_file(
                config=config,
                path=_input,
                group='input',
                obj=self.record)
        for _output in self.ios['outputs']:
            api_response = self.api_module.upload_file(
                config=config,
                path=_output,
                group='output',
                obj=self.record)

    def run(self):
        found = False
        duration = 0
        project = None
        config  = None
        while True:
            running = False
            self.info = self.link.record()
            if self.info:
                found = True
                running = True
                core.write_repo(self.name, self.info)
                config = core.read_config('default')
                registrations = core.read_reg('default')
                # # print self.name
                # # print self.tag
                regs = self.clnk_module.find_by(
                    regs=registrations,
                    name=self.name,
                    tag=self.tag)
                # # print "Record: {0}".format(self.record)
                # # print registrations
                # # print regs
                if len(regs) > 0:
                    project = registrations[regs[0]]['project']
                if project:
                    if self.link.updated:
                        # print self.tag
                        for data in self.info['io_files']:
                            if data[3] in ['r', 'r+', 'a+'] and data[0] not in self.ios['inputs']:
                                self.ios['inputs'].append(data[0])
                            if data[3] in ['w', 'w+', 'a', 'a+'] and data[0] not in self.ios['outputs']:
                                self.ios['outputs'].append(data[0])
                        try:
                            self.request['inputs'] = [
                                {
                                    'input':data
                                } for data in self.info['io_files'] if data[3] in ['r', 'r+', 'a+']]
                        except:
                            self.request['inputs'] = []
                        try:
                            self.request['outputs'] = [
                                {
                                    'output':data
                                } for data in self.info['io_files'] if data[3] in ['w', 'w+', 'a', 'a+']]
                        except:
                            self.request['outputs'] = []
                        try:
                            self.request['dependencies'] = [
                                {
                                    'dependency':data
                                } for data in self.info['libraries']]
                        except:
                            self.request['dependencies'] = []
                        self.request['status'] = self.info['status']
                        self.request['extend'] = {}
                        self.request['extend']['children'] = self.info['children']
                        self.request['extend']['network'] = self.info['network']
                        self.request['extend']['cp_purcentage'] = self.info['cp_purcentage']
                        self.request['extend']['mem_purcentage'] = self.info['mem_purcentage']
                        self.request['extend']['threads'] = self.info['threads']

                        api_response = self.api_module.record_update(
                            config=config,
                            record=self.record,
                            request=self.request)
                        self.records.append(self.request)
                        # print "Record updated"
                        if not api_response[0]:
                            # # print "Error: Watcher recording create process failed."
                            # # print api_response[1]
                            pass
                    else:
                        self.request['label'] = self.tag
                        self.request['tags'] = [self.tag]
                        # print self.tag
                        self.request['system'] = self.info['computer']
                        for data in self.info['io_files']:
                            if data[3] in ['r', 'r+', 'a+'] and data[0] not in self.ios['inputs']:
                                self.ios['inputs'].append(data[0])
                            if data[3] in ['w', 'w+', 'a', 'a+'] and data[0] not in self.ios['outputs']:
                                self.ios['outputs'].append(data[0])
                        try:
                            self.request['inputs'] = [
                                {
                                    'input':data
                                } for data in self.info['io_files'] if data[3] in ['r', 'r+', 'a+']]
                        except:
                            self.request['inputs'] = []
                        try:
                            self.request['outputs'] = [
                                {
                                    'output':data
                                } for data in self.info['io_files'] if data[3] in ['w', 'w+', 'a', 'a+']]
                        except:
                            self.request['outputs'] = []
                        try:
                            self.request['dependencies'] = [
                                {
                                    'dependency':data
                                } for data in self.info['libraries']]
                        except:
                            self.request['dependencies'] = []
                        self.request['status'] = self.info['status']
                        self.request['access'] = 'private'
                        self.request['execution'] = {
                            'cmdline':self.info['cmdline'],
                            'executable':self.info['executable'],
                            'path':self.info['path'],
                            'name':self.info['name']}
                        self.request['extend'] = {}
                        self.request['extend']['children'] = self.info['children']
                        self.request['extend']['network'] = self.info['network']
                        self.request['extend']['cp_purcentage'] = self.info['cp_purcentage']
                        self.request['extend']['mem_purcentage'] = self.info['mem_purcentage']
                        self.request['extend']['threads'] = self.info['threads']
                        api_response = self.api_module.record_create(
                            config=config,
                            project=project,
                            request=self.request)
                        # print "Record created"
                        self.records.append(self.request)
                        if api_response[0]:
                            self.record = api_response[1]['head']['id']
                        else:
                            # # print "Error: Watcher recording create process failed."
                            # print api_response[1]
                            # pass
                            pass

                        if self.info['status'] in ['killed', 'terminated', 'stoped']: #'sleeping', 
                            running = False 
                else:
                    # print "Error: Unable to find the project."
                    pass
            else:
                # print "No info!!!"
                pass
            if found and not running:
                break
            sleep(self.refresh)
            duration += self.refresh
            if duration >= self.timeout:
                break
        self.sync_io(config)
        return self.records

@click.command()

@click.option('--name', default=None, help="Watched software name.")
@click.option('--tag', default=None, help="Watched process tag.")
@click.option('--delay', default=None, help="Watching delay.")
@click.option('--aid', default=None, help="Backend api host.")
@click.option('--origin', default=None, help="Original process")
@click.option('--clnk', default=None, help="core linker")
@click.option('--api', default=None, help="api client")
@click.option('--elnk', default=None, help="execution linker")

def handle(name, tag, delay, aid, origin, elnk):
    delay_value = 10
    aid_value = None
    origin_value = None
    # # print "Name: {0}".format(name)
    # # print "tag: {0}".format(tag)

    stamp = str(datetime.datetime.now())

    if delay:
        delay_value = int(delay)

    if name and tag and api and elnk and clnk:
        clnk_module = core.extend_load(clnk)
        elnk_module = core.extend_load(elnk)
        api_module = core.extend_load(api)
        task = CoRRTask(name=name, tag=tag, clnk_module=clnk_module, api_module=api_module, elnk_module=elnk_module)
        # task.run()
        try:
            # # print "Loading watcher: {0}".format(task.tag)
            with daemon.DaemonContext():
                task.run()
        except:
            pass


if __name__ == '__corr.main__':
    handle()
