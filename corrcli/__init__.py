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
        version = get_distribution(__name__).version
    except DistributionNotFound:
        version = "unknown, try running `python setup.py egg_info`"

    return version

__version__ = get_version()

@click.group(invoke_without_command=True)
@click.version_option(__version__)
# @click.option('--version', '-v', is_flag=True, help="Print the version number.")
def cli():
    """Base command for simple meta query options.

    $ corrcli --version

    """
    click.echo("Use --help to show usage.")

__all__ = ['__version__',
           'test']
