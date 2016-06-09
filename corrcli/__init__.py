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
import click


def test():
    r"""
    Run all the doctests available.
    """
    import pytest
    path = os.path.split(__file__)[0]
    pytest.main(args=[path, '--doctest-modules', '-r s'])


def get_version():
    """Get the version of the code from egg_info.

    Returns:
      the package version number
    """
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__).version # pylint: disable=no-member
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version


__version__ = get_version()

@click.group()
@click.version_option(__version__)
def cli():
    """The CoRR command line tool.
    """

## These modules must be imported after defining cli

from . import commands # pylint: disable=wrong-import-position

__all__ = ['__version__',
           'test']
