"""Inspector that uses psutil to gather proces data.

"""
import psutil
from .inspector import Inspector

class ProcessInspector(Inspector):
    """Inspector that uses psutil to gather data.

    A process is returned with 'status' finished if it can't be found.

    >>> large_int = 100000000000000
    >>> inspector = ProcessInspector(large_int)
    >>> print(inspector.inspect()['status'])
    finished

    Attributes:
      pid: the process ID to inspect
      schema_dict: the mapping from psutil to the CoRR schema

    """
    memory_parse = lambda process_dict, data_dict: \
                   max(int(process_dict['memory_info'].rss), data_dict['memory'] or 0)

    schema_dict = {'process_name' : 'name',
                   'executable' : 'exe',
                   'process_created' : 'create_time',
                   'cwd' : 'cwd',
                   'memory' : memory_parse,
                   'username' : 'username',
                   'status' : 'status',
                   'cmdline' : 'cmdline'}


    def inspect(self, data_dict=None):
        observed_dict = self.get_observed_dict()
        data_dict = self.ini_data_dict(data_dict)
        if observed_dict is not None:
            return self.update_data_dict(observed_dict, data_dict)
        else:
            data_dict['status'] = 'finished'
            return data_dict

    def get_observed_dict(self):
        try:
            process = psutil.Process(self.pid)
            observed_dict = process.as_dict()
        except psutil.NoSuchProcess:
            observed_dict = None
        return observed_dict
