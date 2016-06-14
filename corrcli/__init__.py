"""`corrcli` -- the CoRR comand line tool.

Use

    $ corrcli --help

for usage details or

    $ python setup.py install

to install and

    $ python -c "import corrcli; corrcli.test()"

to test.

"""

import os
from .tools import get_version
from .tools import get_config_dir

def test():
    r"""
    Run all the doctests available.
    """
    import pytest
    path = os.path.split(__file__)[0]
    pytest.main(args=[path, '--doctest-modules', '-r s'])


__version__ = get_version()

default_config_dir = get_config_dir(__name__)
default_config_file = 'config.ini'


from .commands.cli import cli
from .commands.config import config
from .commands.watch import watch


__all__ = ['__version__',
           'test']
