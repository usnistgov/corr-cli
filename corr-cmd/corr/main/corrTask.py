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

    def run(self):
        found = False
        duration = 0
        project = None
        while True:
            running = False
            self.info = self.link.record()
            if self.info:
                found = True
                running = True
                core.write_repo(self.name, self.info)
                request = {}
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
                        request['inputs'] = [
                            {
                                'library':data[0]
                            } for data in self.info['io_files']]
                        request['outputs'] = [
                            {
                                'library':data[0]
                            } for data in self.info['io_files']]
                        request['dependencies'] = [
                            {
                                'library':data[0]
                            } for data in self.info['libraries']]
                        request['status'] = self.info['status']
                        request['extend'] = {}
                        request['extend']['children'] = self.info['children']
                        request['extend']['network'] = self.info['network']
                        request['extend']['cp_purcentage'] = self.info['cp_purcentage']
                        request['extend']['mem_purcentage'] = self.info['mem_purcentage']
                        request['extend']['threads'] = self.info['threads']

                        api_response = self.api_module.record_update(
                            config=config,
                            record=self.record,
                            request=request)
                        self.records.append(request)
                        # print "Record updated"
                        if not api_response[0]:
                            # # print "Error: Watcher recording create process failed."
                            # # print api_response[1]
                            pass
                    else:
                        request['label'] = self.tag
                        request['tag'] = [self.tag]
                        request['system'] = self.info['computer']
                        request['inputs'] = [
                            {
                                'library':data[0]
                            } for data in self.info['io_files']]
                        request['outputs'] = [
                            {
                                'library':data[0]
                            } for data in self.info['io_files']]
                        request['dependencies'] = [
                            {
                                'library':data[0]
                            } for data in self.info['libraries']]
                        request['status'] = self.info['status']
                        request['access'] = 'private'
                        request['execution'] = {
                            'cmdline':self.info['cmdline'],
                            'executable':self.info['executable'],
                            'path':self.info['path'],
                            'name':self.info['name']}
                        request['extend'] = {}
                        request['extend']['children'] = self.info['children']
                        request['extend']['network'] = self.info['network']
                        request['extend']['cp_purcentage'] = self.info['cp_purcentage']
                        request['extend']['mem_purcentage'] = self.info['mem_purcentage']
                        request['extend']['threads'] = self.info['threads']
                        api_response = self.api_module.record_create(
                            config=config,
                            project=project,
                            request=request)
                        # print "Record created"
                        self.records.append(request)
                        if api_response[0]:
                            self.record = api_response[1]['head']['id']
                        else:
                            # # print "Error: Watcher recording create process failed."
                            # # print api_response[1]
                            pass

                        if self.info['status'] in ['sleeping', 'killed', 'terminated', 'stoped']:
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
            if not found and duration >= self.timeout:
                break
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
