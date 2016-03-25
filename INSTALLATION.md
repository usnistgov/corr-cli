# Installing CoRR

CoRR is designed as a web app and if possible users should try and use
an exising instance such as
[http://corr-root.org:5000](http://corr-root.org:5000). If you wish to
develop CoRR, then please use the instructions below.

## Native Development Installation

To develop with CoRR it is best to be using an Ubuntu linux
machine. First clone the CoRR repository and then run

    $ ./config.bash -K --tags "install_develop,serve_develop"

This will install and run an Ansible script that will install and run
mongodb, create a "corr" conda environment and run the various
webapps.  Other varialbes that can be passed at the command line
include `corr_env`, `corr_version`, `corr_repo` and
`anaconda_path`. For example, to install from a different repository use

## Docker Development Installation

To come


## Deployment
