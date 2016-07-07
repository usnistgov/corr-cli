"""Abstract base class for all watchers
"""
import abc


class Watcher(object):
    """Abstract base class for all watchers.

    A watcher queries a process for metadata about that process.

    Attributes:
      pid: the process ID to watch
      schema_dict: mapping from the observed data to the output data

    """
    __metaclass__ = abc.ABCMeta
    schema_dict = {}
    def __init__(self, pid):
        """Instantiate a Watcher.

        Args:
          pid: the process ID to watch

        """
        self.pid = pid

    @abc.abstractmethod
    def watch(self, data_dict=None):
        """Gather data about a process.

        Data is aggregated from the observed process data and the
        data_dict passed.

        Args:
          data_dict: the dictionary to update

        Returns:
          an updated data_dict

        """

    @abc.abstractmethod
    def get_observed_dict(self):
        """Query for the observed process data.

        Returns:
          the observed data as a dictionary

        """

    def ini_data_dict(self, data_dict):
        """Initialize the passed in data dictionary.

        Update the data to have the keys associated with the watcher
        object even if nothing is observed about the process.

        Args:
          data_dict: the dictionary to update

        Returns:
          the initialized data dictionary

        """
        if data_dict is None:
            data_dict = dict()
        for key in self.schema_dict.keys():
            data_dict[key] = data_dict.get(key, None)
        return data_dict

    def update_data_dict(self, observed_dict, data_dict):
        """Update the data dictionary with the observed data.

        Args:
          observed_dict: the observed process dictionary
          data_dict: dictionary to update

        Returns:
          the data dictionary updated with the observed data

        >>> class TestWatcher(Watcher):
        ...     schema_dict = {'key1' : 'value1',
        ...                    'key2' : lambda x, y: x['value2'] + '_test'}
        >>> watcher = TestWatcher(1)
        >>> observed_dict = {'value1' : 'observation1',
        ...                  'value2' : 'observation2'}
        >>> data_dict = {}
        >>> print(watcher.update_data_dict(observed_dict, data_dict))
        {'key2': 'observation2_test', 'key1': 'observation1'}
        """
        for key, value in self.schema_dict.items():
            if isinstance(value, str):
                data_dict[key] = observed_dict[value]
            else:
                func = value
                data_dict[key] = func(observed_dict, data_dict)
        return data_dict
