## Manual installation

    $ gem install jekyll

## Building docker containers

After configuring docker based on your platform, do:

    $ git clone https://github.com/faical-yannick-congo/corr-view.git
    $ cd sumatra-view
    $ docker build -t corr-view .

Befor you can run the containers, figureout the docker vm or interface
ip address.

### On Ubuntu run:

    $ ifconfig.
    Notice a docker0 interface and copy the ip_address.

### On Osx: run: 

    $ boot2docker ip.
    Copy the ip_address of the boot2docker vm.
    In the corr-view code, inside config.py, replace 
    'host': '192.168.59.103' in MONGODB_SETTINGS {} by
    'host': 'ip_address'.
    Then you are good to go.

### On other plateforms:

We assume that the Ubuntu case will be most likely the case for Linux
based plateforms. 

For non unix based plateforms that will probably
require a vm to run the docker containers, it will be most likely the 
same as Osx.

When you solve that based on your plateform, run:

    $ docker run -i -t -p 4000:4000 corr-view serve -H localhost

## Pull from docker registry

After configuring docker based on your platform, do:

    $ docker pull palingwende/corr-view

Before you can run the full corr plateform make sure corr-db and
corr-cloud are running.

NOTE: 192.168.59.103 is the default boot2docker ip, unless your have
some colisions with another vm using the same ip, you are good to go.

Figure out your docker ip.

    If you are on linux: the ip is localhost
    If you are on osx: $ boot2docker ip

Open the browser got to: http://ip_address:4000/

You are on the corr-view frontend at this point.

## Installation
[Install docker][official]

On Osx/Non Linux: [Boot2docker][boot2docker].
        
    $ boot2docker init
    $ boot2docker start
    EXPORT the values being displayed.
    
On Linux:
        
    $ sudo apt-get update
    $ sudo apt-get install docker.io

[official]: https://docs.docker.com/installation/
[boot2docker]: https://github.com/boot2docker/osx-installer/releases/tag/v1.5.0