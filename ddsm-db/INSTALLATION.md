## Manual installation
    
    $ apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    $ echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
    $ apt-get update -y
    $ apt-get install -y mongodb-org
    $ mkdir -p /data/db

## Building docker containers

After configuring docker based on your platform, do:

    $ git clone https://github.com/data-driven-science/ddsm-db.git
    $ cd ddsm-db
    $ cd ddsmdb
    $ docker build -t ddsm-db .

Befor you can run the containers, figureout the docker vm or interface
ip address.

### On Ubuntu run:

    $ ifconfig.
    Notice a docker0 interface and copy the ip_address.

### On Osx: run: 

    $ boot2docker ip.
    Copy the ip_address of the boot2docker vm.
    In the ddsm-db code, inside config.py, replace 
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

    $ docker run -d -p 27017:27017 -p 28017:28017 ddsm-db

## Pull from docker registry

After configuring docker based on your platform, do:

    $ docker pull palingwende/ddsm-db

Before you can run the containers we have to bridge the docker0 
interface to the settings in the ddsm-db parameters of the database.

###On Ubuntu:

    $ ip link add br0 type bridge
    $ sudo ip link add br0 type bridge
    $ sudo ip addr add 192.168.59.103/20 dev br0
    $ sudo ip link set br0 up
    $ docker run -d -p 27017:27017 -p 28017:28017 palingwende/ddsm-db

Finally to make that persistant run the following commands that will 
add the bridging to your network interfaces file.

    $ sudo vim /etc/network/interfaces

Add the follwing at the end of the file:

    auto br0
    iface br0 inet static
            address 192.168.59.103
            netmask 255.255.255.0
            bridge_ports dummy0
            bridge_stp off
            bridge fd 0

###On Osx:

Run: $ boot2docker ip.
Make sure that the ip is equivalent to 192.168.59.103. If it is
you can just do the following:

    $ docker run -d -p 27017:27017 -p 28017:28017 palingwende/ddsm-db

NOTE: 192.168.59.103 is the default boot2docker ip, unless your have
some colisions with another vm using the same ip, you are good to go.

###On other plateforms:

We assume that the Ubuntu case will be most likely the case for Linux
based plateforms. 

For non unix based plateforms that will probably
require a vm to run the docker containers, it will be most likely the 
same as Osx.

###Runnin the containers:

When you solve that based on your plateform, run:

    $ docker run -d -p 27017:27017 -p 28017:28017 ddsm-db

## Going to the cloud service frontend

Figure out your docker ip.

    If you are on linux: the ip is localhost (127.0.0.1)
    If you are on osx: $ boot2docker ip

Open the browser got to: http://ip_address:5000/

You are on the ddsm-db mongodb instance at this point.

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