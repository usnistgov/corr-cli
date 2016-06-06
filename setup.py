#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='corrcli',
    version="0.1",
    packages=["corrcli"],
    include_package_data=True,
    maintainer='Faical Yannick P. Congo',
    description=('The command line client to the CoRR platform.'),
    url='https://github.com/wd15/corr-cli',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'corrcli = corrcli.main.cli:handle',
        ],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
)
