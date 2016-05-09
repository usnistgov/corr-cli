import sys, traceback
import datetime
import platform
import psutil

class ExecLink:
    def __init__(self, tag=None, pid=None, origin=None, aid=None, watcher='NoTask'):
        self.tag = tag
        self.pid = pid
        self.origin = origin
        self.aid = aid
        self.info = {}
        self.updated = False
        self.watcher = watcher
        # # print tag

    def record(self):
        pids = psutil.pids()
        stamp = str(datetime.datetime.now())
        process = None
        
        if len(self.info) > 0:
            self.updated = True
        if self.pid:
            process = psutil.Process(self.pid)
        else:
            for i in xrange(len(pids)):
                p = psutil.Process(pids[i])
                if self.tag in ' '.join(
                        p.cmdline()) and self.watcher not in ' '.join(p.cmdline()):
                    # # print p.cmdline()
                    process = p
                    break
        if process is None:
            # # print "Process is None"
            return None
        else:
            try:
                if not self.updated:
                    name = process.name().replace('/', '-')
                    self.info['stamp'] = stamp
                    self.info['aid'] = self.aid
                    self.info['origin'] = self.origin
                    # self.info['marker'] = self.marker
                    try:
                        self.info['computer'] = {
                            'machine':platform.machine(),
                            'node':platform.node(),
                            'platform':platform.platform(aliased=True),
                            'processor':platform.processor(),
                            'release':platform.release(),
                            'system':platform.system(),
                            'version':platform.version()}
                    except:
                        self.info['computer'] = 'unknown'
                    try:
                        self.info['name'] = process.name()
                    except:
                        self.info['name'] = 'unknown'
                    try:
                        self.info['pid'] = i
                    except:
                        self.info['pid'] = 'unknown'
                    try:
                        self.info['executable'] = process.exe()
                    except:
                        self.info['executable'] = 'unknown'
                    try:
                        self.info['path'] = process.cwd()
                    except:
                        self.info['path'] = 'unknown'
                    try:
                        self.info['cmdline'] = process.cmdline()
                    except:
                        self.info['cmdline'] = 'unknown'
                    try:
                        self.info['owner'] = process.username()
                    except:
                        self.info['owner'] = 'unknown'
                    try:
                        self.info['created'] = datetime.datetime.fromtimestamp(
                            process.create_time()).strftime("%Y-%m-%d %H:%M:%S.%f")
                    except:
                        self.info['created'] = 'unknown'
                    try:
                        self.info['terminal'] = process.terminal()
                    except:
                        self.info['terminal'] = 'unknown'
                    try:
                        self.info['status'] = process.status()
                    except:
                        self.info['status'] = 'unknown'
                    # Following subjected to changes.
                    try:
                        threads = process.threads()
                        self.info['threads'] = {'number':len(threads), 'list':threads}
                    except:
                        self.info['threads'] = 'unknown'
                    try:
                        children = process.children()
                        self.info['children'] = {'number':len(children), 'list':[]}
                        for c in children:
                            self.info['children']['list'].append(self.wrap_child(int(c.pid)))
                    except:
                        self.info['children'] = 'unknown'
                    
                    try:
                        self.info['cp_purcentage'] = [process.cpu_percent(interval=1.0)]
                    except:
                        self.info['cp_purcentage'] = 'unknown'
                    try:
                        self.info['mem_purcentage'] = [process.memory_percent()]
                    except:
                        self.info['mem_purcentage'] = 'unknown'
                    try:
                        self.info['libraries'] = process.memory_maps()
                    except:
                        self.info['libraries'] = 'unknown'
                    try:
                        self.info['network'] = process.get_connections()
                    except:
                        # # print traceback.# print_exc(file=sys.stdout)
                        self.info['network'] = 'unknown'
                    try:
                        self.info['io_files'] = process.open_files()
                    except:
                        self.info['io_files'] = 'unknown'
                else:
                    try:
                        threads = process.threads()
                        self.info['threads'].append({'number':len(threads), 'list':threads})
                        self.info['threads'] = map(dict, set(tuple(sorted(d.items())) for d in self.info['threads']))
                    except:
                        pass
                    try:
                        children = process.children()
                        for c in children:
                            self.info['children']['list'].append(self.wrap_child(int(c.pid)))

                        self.info['children']['list'] = map(dict, set(tuple(sorted(d.items())) for d in self.info['children']['list']))
                        self.info['children']['number'] = len(self.info['children']['list'])
                    except:
                        pass
                    
                    try:
                        self.info['cp_purcentage'].append(process.cpu_percent(interval=1.0))
                    except:
                        self.info['cp_purcentage'].append('unknown')
                    try:
                        self.info['mem_purcentage'].append(process.memory_percent())
                    except:
                        self.info['mem_purcentage'].append('unknown')
                    try:
                        self.info['libraries'].append(process.memory_maps())
                        self.info['libraries'] = map(dict, set(tuple(sorted(d.items())) for d in self.info['libraries']))
                    except:
                        pass
                    try:
                        self.info['network'].append(process.get_connections())
                        self.info['network'] = map(dict, set(tuple(sorted(d.items())) for d in self.info['network']))
                    except:
                        pass
                    try:
                        self.info['io_files'].append(process.open_files())
                        self.info['io_files'] = map(dict, set(tuple(sorted(d.items())) for d in self.info['io_files']))
                    except:
                        pass
                return self.info
            except:
                # # print traceback.# print_exc(file=sys.stdout)
                return None

    def wrap_child(self, pid):
        process = psutil.Process(pid)
        info = {}
        try:
            info['name'] = process.name()
        except:
            info['name'] = 'unknown'
        try:
            info['pid'] = pid
        except:
            info['pid'] = 'unknown'
        try:
            info['executable'] = process.exe()
        except:
            info['executable'] = 'unknown'
        try:
            info['path'] = process.cwd()
        except:
            info['path'] = 'unknown'
        try:
            info['cmdline'] = process.cmdline()
        except:
            info['cmdline'] = 'unknown'
        try:
            info['owner'] = process.username()
        except:
            info['owner'] = 'unknown'
        try:
            info['created'] = datetime.datetime.fromtimestamp(
                process.create_time()).strftime("%Y-%m-%d %H:%M:%S.%f")
        except:
            info['created'] = 'unknown'
        try:
            info['terminal'] = process.terminal()
        except:
            info['terminal'] = 'unknown'
        try:
            threads = process.threads()
            info['threads'] = {'number':len(threads), 'list':threads}
        except:
            info['threads'] = 'unknown'
        try:
            info['status'] = process.status()
        except:
            info['status'] = 'unknown'
        try:
            info['mem_purcentage'] = process.memory_percent()
        except:
            info['mem_purcentage'] = 'unknown'
        try:
            info['libraries'] = process.memory_maps()
        except:
            info['libraries'] = 'unknown'
        try:
            info['network'] = process.get_connections()
        except:
            info['network'] = 'unknown'
        try:
            info['io_files'] = process.open_files()
        except:
            info['io_files'] = 'unknown'
        return info
