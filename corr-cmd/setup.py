#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='corr',
    version="0.1",
    packages=["corr"],
    include_package_data=True,
    maintainer='Faical Yannick P. Congo',
    description=('The command line client to the CoRR platform.'),
    url='https://github.com/usnistgov/corr',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'corr = corr.cli:handle',
        ],
    },
    # package_data = {
    #     'data': ['*.json'],
    # },
    test_suite='nose.collector',
    tests_require=['nose'],
)
