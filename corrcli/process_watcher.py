import psutil

class ProcessWatcher(object):
    schema_dict = {'process_name' : 'name',
                   'executable' : 'exe',
                   'process_created' : 'create_time',
                   'cwd' : 'cwd',
                   'memory' : lambda process_dict, data_dict_old: max(int(process_dict['memory_info'].rss), data_dict_old.get('memory', 0.)),
                   'username' : 'username',
                   'status' : 'status',
                   'cmdline' : 'cmdline'}

    def __init__(self, pid):
        self.pid = pid

    def watch(self, data_dict=dict()):
        data_dict_old = data_dict.copy()
        for key in self.schema_dict.keys():
            data_dict[key] = data_dict.get(key, None)
        try:
            process = psutil.Process(self.pid)
            process_dict = process.as_dict()
        except psutil.NoSuchProcess:
            process = None
        if process is not None:
            for key, value in self.schema_dict.items():
                if type(value) is str:
                    data_dict[key] = process_dict[value]
                else:
                    data_dict[key] = value(process_dict, data_dict_old)
            return data_dict
        else:
            data_dict['status'] = 'finished'
            return data_dict
