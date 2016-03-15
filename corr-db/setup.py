#!/usr/bin/env python

import subprocess
from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env).communicate()[0]
        return out
    
    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = ""

    return GIT_REVISION

def getVersion(version, release=False):
    if os.path.exists('.git'):
        _git_version = git_version()[:7]
    else:
        _git_version = ''
    if release:
        return version
    else:
        return version + '-dev.' + _git_version

setup(name='corrdb',
      version=getVersion('alpha-0.1', release=False),
      install_requires=required,
      description='Package for CoRR Database Models',
      author='Yannick Congo',
      author_email='yannick.congo@gmail.com',
      url='https://github.com/faical-yannick-congo/corr-db',
      packages=find_packages(),
      package_data={'' : ['test/*.py']},
      )
