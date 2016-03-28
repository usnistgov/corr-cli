# Installing CoRR

CoRR is designed as a web app and if possible users should try and use
an existing instance such as
[http://corr-root.org:5000](http://corr-root.org:5000). If you wish to
develop CoRR, then please use the instructions below.

## Native Development Installation

To develop with CoRR it is best to be using an Ubuntu linux
machine. First clone the CoRR repository and then run

    $ ./config.bash -K --tags install_develop

This will run an Ansible script that will install all the necessary
prerequisites to run CoRR. `sudo` privileges are required. Edit
[`builds/install.yaml`](builds/install.yaml) to change custom
variables such as the version of the code to install and the
repository URL. To launch the front end web app and the API use,

    $ ./config.bash -K --tags serve_develop

This runs the mongodb, the flask development servers for corr-cloud
and corr-api as well as jekyll for the frontend.

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
    $ docker run -i -p 4000:4000 --net=host -t corr-test:latest

Go to http://localhost:4000 and the front end should be available.

This version of the Dockerfile is just for testing the Ansible
installation script and isn't useful for using or developing CoRR.
