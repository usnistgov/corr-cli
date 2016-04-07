import os
import sys, traceback
import psutil
import json
import datetime
from time import sleep
import platform
import daemon
import core
import api
import click

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
        # self.context = None
    
    def run(self):#, context=None):
        # self.context = context
        found = False
        duration = 0
        while True:

            pids = psutil.pids()
            # print pids
            print "running...."
            stamp = str(datetime.datetime.now())
            running = False
            for i in xrange(len(pids)):
                try:
                    p = psutil.Process(pids[i])
                    # print "Name: %s"%p.name()
                    # print "CmdLine: %s"%p.cmdline()
                    #TODO: Fix in case of many occurences found.
                    #For now we pick only one. How about concurent instance of the same code?
                    #I will have to think about a list. Yet i think they should be seen as threads.
                    # print "MARKER: %s"%self.marker
                    # print "CMD: %s"%p.cmdline()
                    if self.marker in ' '.join(p.cmdline()) and 'CoRRTask' not in ' '.join(p.cmdline()):
                    #if self.name in ' '.join(p.cmdline()) and ((self.marker != None and self.marker in ' '.join(p.cmdline())) or self.marker == None):
                        found = True
                        running = True
                        name = p.name().replace('/', '-')
                        
                        info = {'stamp':stamp}
                        info['aid'] = self.aid
                        info['origin'] = self.origin
                        info['marker'] = self.marker
                        try:
                            info['computer'] = {'machine':platform.machine(), 'node':platform.node(), 'platform':platform.platform(aliased=True), 'processor':platform.processor(), 'release':platform.release(), 'system':platform.system(), 'version':platform.version()}
                        except:
                            info['computer'] = 'unknown'
                        try:
                            info['name'] = p.name()
                        except:
                            info['name'] = 'unknown'
                        try:
                            info['pid'] = i
                        except:
                            info['pid'] = 'unknown'
                        try:
                            info['executable'] = p.exe()
                        except:
                            info['executable'] = 'unknown'
                        try:
                            info['path'] = p.cwd()
                        except:
                            info['path'] = 'unknown'
                        try:
                            info['cmdline'] = p.cmdline()
                        except:
                            info['cmdline'] = 'unknown'
                        try:
                            info['owner'] = p.username()
                        except:
                            info['owner'] = 'unknown'
                        try:
                            info['created'] = datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S.%f")
                        except:
                            info['created'] = 'unknown'
                        try:
                            info['terminal'] = p.terminal()
                        except:
                            info['terminal'] = 'unknown'
                        try:
                            threads = p.threads()
                            info['threads'] = {'number':len(threads), 'list':threads}
                        except:
                            info['threads'] = 'unknown'
                        try:
                            children = p.children()
                            info['children'] = {'number':len(children), 'list':[]}
                            for c in children:
                                info['children']['list'].append(self.wrap_child(int(c.pid)))
                                # info['children']['list'].append({'child':c.pid, 'name':c.name()})
                        except:
                            info['children'] = 'unknown'
                        try:
                            info['status'] = p.status()
                        except:
                            info['status'] = 'unknown'
                        try:
                            info['cp_purcentage'] = p.cpu_percent(interval=1.0)
                        except:
                            info['cp_purcentage'] = 'unknown'
                        try:
                            info['mem_purcentage'] = p.memory_percent()
                        except:
                            info['mem_purcentage'] = 'unknown'
                        try:
                            info['libraries'] = p.memory_maps()
                        except:
                            info['libraries'] = 'unknown'
                        try:
                            info['network'] = p.get_connections()
                        except:
                            traceback.print_exc(file=sys.stdout)
                            info['network'] = 'unknown'
                        try:
                            info['io_files'] = p.open_files()
                        except:
                            info['io_files'] = 'unknown'

                        # if self.root != None:
                        #     print json.dumps(self.root, sort_keys=True, indent=4, separators=(',', ': '))

                        if self.root != None:
                            if info != self.root['info']:
                                info['stamp'] = stamp
                                diff_res = self.diff(self.root['info'], info)
                                if len(diff_res) != 0:
                                   self.history.append(diff_res)
                                # print json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '))
                                # os.path.expanduser('~')
                                core.write_repo(self.name, {'info':self.root['info'], 'history':self.history})
                                # filename = "{0}/{1}.corr".format(core.repos_path, self.name)
                                # with open(filename, 'w') as info_json:
                                #     info_json.write(json.dumps({'info':self.root['info'], 'history':self.history}, sort_keys=True, indent=4, separators=(',', ': ')))
                            else:
                                # Nothing to do. No changes.
                                pass       
                        else:
                            self.root = {'info':info, 'history':[]}
                            # print json.dumps(info, sort_keys=True, indent=4, separators=(',', ': '))
                            # filename = '%s/.corr/repository/%s-%s.json'%(os.path.expanduser('~'), self.name, self.marker.split("marker_")[1])
                            # filename = filename.replace(' ','_').replace(':','-')
                            # with open(filename, 'w') as info_json:
                            #     info_json.write(json.dumps(self.root, sort_keys=True, indent=4, separators=(',', ': ')))
                            core.write_repo(self.name, self.root)
                            request = {}
                            # print core.pretty_json(request)
                            config = core.read_config()
                            registrations = core.read_reg()
                            regs = core.find_by(registrations, name=self.name, marker=self.marker)
                            print "Record: {0}".format(self.record)
                            if len(regs) > 0:
                                project = registrations[regs[0]]['project']
                                if self.record == '':
                                    request['label'] = self.marker
                                    request['tags'] = [self.marker]
                                    request['system'] = info['computer']
                                    request['inputs'] = [{'library':data[0]} for data in info['io_files']]
                                    request['outputs'] = [{'library':data[0]} for data in info['io_files']]
                                    request['dependencies'] = [{'library':data[0]} for data in info['libraries']]
                                    request['status'] = info['status']
                                    request['access'] = 'private'
                                    request['execution'] = {'cmdline':info['cmdline'], 'executable':info['executable'], 'path':info['path'], 'name':info['name']}
                                    request['extend'] = {}
                                    request['extend']['children'] = info['children']
                                    request['extend']['network'] = info['network']
                                    request['extend']['cp_purcentage'] = info['cp_purcentage']
                                    request['extend']['mem_purcentage'] = info['mem_purcentage']
                                    request['extend']['threads'] = info['threads']
                                    # print core.pretty_json(request)
                                    api_response = api.record_create(config=config, project=project, request=request)
                                    if api_response[0]:
                                        self.record = api_response[1]['head']['id']
                                    else:
                                        print "Error: Watcher recording create process failed."
                                        print api_response[1]
                                else:
                                    request['inputs'] = [{'library':data[0]} for data in info['io_files']]
                                    request['outputs'] = [{'library':data[0]} for data in info['io_files']]
                                    request['dependencies'] = [{'library':data[0]} for data in info['libraries']]
                                    request['status'] = info['status']
                                    request['extend'] = {}
                                    request['extend']['children'] = info['children']
                                    request['extend']['network'] = info['network']
                                    request['extend']['cp_purcentage'] = info['cp_purcentage']
                                    request['extend']['mem_purcentage'] = info['mem_purcentage']
                                    request['extend']['threads'] = info['threads']
                                    api_response = api.record_update(config=config, record=self.record, request=request)
                                    if not api_response[0]:
                                        print "Error: Watcher recording create process failed."
                                        print api_response[1]
                                    # update
                            # This allows us to always be recording and not updating.
                            # Figure out a process to upate.
                            self.root = None

                        break
                except:
                    print traceback.print_exc(file=sys.stdout)
                    # pass
            if found and not running:
                # Stop the deamon because the execution finished.
                break
            sleep(self.refresh)
            duration += self.refresh
            if not found and duration >= 60*60: # 1h of wait. terminate the deamon.
                break

    def wrap_child(self, pid):
        p = psutil.Process(pid)
        info = {}
        try:
            info['name'] = p.name()
        except:
            info['name'] = 'unknown'
        try:
            info['pid'] = pid
        except:
            info['pid'] = 'unknown'
        try:
            info['executable'] = p.exe()
        except:
            info['executable'] = 'unknown'
        try:
            info['path'] = p.cwd()
        except:
            info['path'] = 'unknown'
        try:
            info['cmdline'] = p.cmdline()
        except:
            info['cmdline'] = 'unknown'
        try:
            info['owner'] = p.username()
        except:
            info['owner'] = 'unknown'
        try:
            info['created'] = datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S.%f")
        except:
            info['created'] = 'unknown'
        try:
            info['terminal'] = p.terminal()
        except:
            info['terminal'] = 'unknown'
        try:
            threads = p.threads()
            info['threads'] = {'number':len(threads), 'list':threads}
        except:
            info['threads'] = 'unknown'
        try:
            info['status'] = p.status()
        except:
            info['status'] = 'unknown'
        try:
            info['mem_purcentage'] = p.memory_percent()
        except:
            info['mem_purcentage'] = 'unknown'
        try:
            info['libraries'] = p.memory_maps()
        except:
            info['libraries'] = 'unknown'
        try:
            info['network'] = p.get_connections()
        except:
            # traceback.print_exc(file=sys.stdout)
            info['network'] = 'unknown'
        try:
            info['io_files'] = p.open_files()
        except:
            info['io_files'] = 'unknown'
        return info

    def diff(self, info1={}, info2={}):
        result = {}
        if info1['computer'] != info2['computer']:
            result['computer'] = info2['computer']

        if info1['threads'] != info2['threads']:
            result['threads'] = info2['threads']

        if info1['children'] != info2['children']:
            result['children'] = info2['children']

        if info1['status'] != info2['status']:
            result['status'] = info2['status']

        #Not necessary tracks.
        # if info1['cp_purcentage'] != info2['cp_purcentage']:
        #     result['cp_purcentage'] = info2['cp_purcentage']
        
     #    if info1['mem_purcentage'] != info2['mem_purcentage']:
        #     result['mem_purcentage'] = info2['mem_purcentage']

        if info1['libraries'] != info2['libraries']:
            result['libraries'] = info2['libraries']
        
        if info1['network'] != info2['network']:
            result['network'] = info2['network']

        if info1['io_files'] != info2['io_files']:
            result['io_files'] = info2['io_files']

        return result

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
        # task = CoRRTask(pid='{0}/{1}-single-{2}.pid'.format(core.tasks_path, name, stamp), name=name, marker=marker)
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