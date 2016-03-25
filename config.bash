#!/bin/bash

if ! dpkg -s ansible > /dev/null; then
    sudo apt-get install -y ansible
fi

## be sure to use the system python with ansible at this point
export PATH=/usr/bin:$PATH
ansible-playbook $@ builds/install.yaml
