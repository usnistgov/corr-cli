<p align="center">
    <img src="https://rawgit.com/usnistgov/corr/master/corr-view/frontend/images/logo.svg"
         height="240"
         alt="CoRR logo"
         class="inline">
</p>

<p align="center"><sup><strong>
See the live instance at <a href="http://corr-root.org/">corr-root.org:5000</a>.
</strong></sup></p>

CoRR-cmd is a simulation management tool to record computational
investigations in scientific computing. It is designed to work with
the Cloud of Reproducible Records (CoRR), an app for storing and
viewing data gathered by CoRR-cmd

[![Gitter Chat](https://img.shields.io/gitter/room/gitterHQ/gitter.svg)](https://gitter.im/usnistgov/corr)

* **[INSTALL](INSTALLATION.md)** – installation instructions.
* **[LICENSE](LICENSE)** – the license.
* **[USAGE](USAGE)** - usage examples.

## What is it?

The CoRR (Cloud of Reproducible Records) app is a cloud platform that
allows scientists to record their computational investigations in the
cloud to improve sharing and collaboration.  CoRR-cmd is the client
that runs locally to capture meta-data about simulations. CoRR-cmd can
run independetly from the CoRR app and use the local file system for
storage.

## Quickstart

* `git clone git@github.com:usnistgov/corr.git`
* `cd corr/corr-cmd`
* `python setup.py install`

# Setup
* Configure the cloud backend api access parameters.
* `corr --config --host api_host_default=0.0.0.0 --port api_port_default=5100 --key user_api_key_from_frontent`
* Check the connectivity to the backend
* `corr --conx` says if we can reach the backend or not.
* Align the local repository with the remote user space one. All projects are synched (without the records.)
* `corr --align`
* Register/Unregister a software/project
* `corr --register --name software_name` Returns a marker that should be used when executing an instance.
* `corr --unregister --name software_name --marker software_marker`
* Manage softwares
* `corr --list` List of all the registered softwares (summary).
* `corr --show --name software_name --marker software_marker` Detailed description of a software.
* Manage watchers
* `corr --watch --name software_name --marker software_marker` Will initiate a watcher deamon that will listen for an instance and
* `corr --unwatch --name software_name --marker software_marker` Will list the users.

# Test coverage
* nosetests -sv --with-coverage --cover-erase --cover-html --cover-package=corr
