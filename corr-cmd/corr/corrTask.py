import sys, traceback
import datetime
from time import sleep
import daemon
import click
from corr import core
from corr import api
from corr.execLink import ExecLink

class CoRRTask:
    def __init__(self, pid=None, name=None, refresh=10, aid=None, origin=None, marker=None):
        self.pid = pid
        self.origin = origin
        self.aid = aid
        self.name = name
        self.refresh = refresh
        self.root = None
        self.history = []
        self.marker = marker
        self.record = ''
        self.info = None
        self.link = ExecLink(tag=marker)

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
                config = core.read_config()
                registrations = core.read_reg()
                regs = core.find_by(
                    registrations,
                    name=self.name,
                    marker=self.marker)
                print "Record: {0}".format(self.record)
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
                        api_response = api.record_update(
                            config=config,
                            record=self.record,
                            request=request)
                        if not api_response[0]:
                            print "Error: Watcher recording create process failed."
                            print api_response[1]
                    else:
                        request['label'] = self.marker
                        request['tags'] = [self.marker]
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
                        api_response = api.record_create(
                            config=config,
                            project=project,
                            request=request)
                        if api_response[0]:
                            self.record = api_response[1]['head']['id']
                        else:
                            print "Error: Watcher recording create process failed."
                            print api_response[1]

                        if self.info['status'] in ['sleeping', 'killed', 'terminated', 'stoped']:
                            running = False 
                else:
                    print "Error: Unable to find the project."

            if found and not running:
                break
            sleep(self.refresh)
            duration += self.refresh
            if not found and duration >= 60*60:
                break

@click.command()

@click.option('--name', default=None, help="Watched software name.")
@click.option('--marker', default=None, help="Watched process marker.")
@click.option('--delay', default=None, help="Watching delay.")
@click.option('--aid', default=None, help="Backend api host.")
@click.option('--origin', default=None, help="Original process")

def handle(name, marker, delay, aid, origin):
    delay_value = 10
    aid_value = None
    origin_value = None
    print "Name: {0}".format(name)
    print "Marker: {0}".format(marker)

    stamp = str(datetime.datetime.now())

    if delay:
        delay_value = int(delay)

    if name and marker:
        task = CoRRTask(name=name, marker=marker)
        # task.run()
        try:
            print "Loading watcher: {0}".format(task.marker)
            with daemon.DaemonContext():
                task.run()
        except:
            pass


if __name__ == '__main__':
    handle()
