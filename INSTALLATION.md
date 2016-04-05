# Installing CoRR

CoRR is designed as a web app and if possible users should try and use
an existing instance such as
[http://corr-root.org:5000](http://corr-root.org:5000). If you wish to
develop CoRR, then please use the instructions below.

## Native Development Installation

To develop with CoRR it is best to be using an Ubuntu linux
machine. First clone the CoRR repository and then edit
`builds/host_example` and copy it to `builds/host`. Remember that the
`stormpath_id`, `stormpath_secret` and `stormpath_app` values are
required for the cloud service. To install use,

    $ ./config.bash --ask-sudo-pass --tags install --inventory-file builds/hosts

This will run an Ansible script that will install all the necessary
prerequisites to run CoRR. `sudo` privileges are required. Edit
`builds/hosts` to change custom variables such as the version of the
code to install, the repository URL or the conda environment. To start
development servers switch to the `corr` environment with,

    $ source activate corr

and use

    $  sudo service mongodb start

to start the database and then

    $ cd corr-api
    $ python run.py

to start the API and then in another terminal use,

    $ cd ../corr-cloud
    $ python run.py

to start the cloud service. To run the front end, open another
terminal and use

    $ cd ../corr-view/frontend
    $ jekyll serve --watch --port 5000 --host 0.0.0.0

Go to [http://0.0.0.0/](http://0.0.0.0/) to see the front end.

## Test Installation with Docker

There is a Docker file in builds,
[`builds/Dockerfile-test`](builds/Dockerfile-test) for testing the
Ansible installation. To use this, first
[install Docker](https://docs.docker.com/engine/installation/linux/ubuntulinux/)
and then launch Docker with

    $ sudo docker service start

and then copy the Dockerfile into the base corr directory and build
it,

    $ cd corr; pwd
    /path/to/corr
    $ cp builds/Dockerfile-test ./Dockerfile
    $ docker build -t corr-test:latest .
    $ docker run -i -p 5000:5000 --net=host -t corr-test:latest

Go to [http://localhost:5000](http://localhost:4000) and the front end
should be available.

This version of the Dockerfile is just for testing the Ansible
installation script and isn't useful for using or developing CoRR.

## Config Script

The config script install Ansible and runs the CoRR Ansible playbook. To get all the
tags available use,

    $ ./config.bash --list-tags
