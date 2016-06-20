import psutil

class PIDWatcher(object):
    schema_dict = {'name' : 'name',
                   'executable' : 'exe',
                   'created' : 'create_time',
                   'cwd' : 'cwd',
                   'memory' : lambda process_dict: process_dict['memory'].rss,
                   'username' : 'username',
                   'status' : 'status',
                   'cmdline' : 'cmdline'}

    def __init__(self, pid):
        self.pid = pid

    def watch(self):
        process = psutil.Process(self.pid)
        if process:
            process_dict = process.as_dict()
            data_dict = dict()
            for key, value in self.schema_dict.iteritems():
                if type(value) is str:
                    data_dict[key] = process_dict[value]
                else:
                    data_dict[key] = value(process_dict)
            return data_dict
        else:
            return None

    @staticmethod
    def get_pids_for_identifier(identifier):
        pid_list = []
        for pid in psutil.pids():
            if any(identifier in item for item in psutil.Process(pid)['cmdline']):
                pid_list.append(pid)
        return pid_list
