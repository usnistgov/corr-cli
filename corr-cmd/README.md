### What is it?
CoRR (Cloud of Reproducible Records) is a cloud platform that allows scientists to record their investigations (computational or experimental) in the cloud to allow a better share and collaboration around the reproducible nature of their work. CoRR also expose an API for 3rd Party applications like Benchmarking, Scoring, Reproducibility Assessment, Learning to hook up to all the publicly shared records and their meta-data for the better good in Science.
CoRR-Cmd is the client that allow researchers to interact with their cloud space. It was created to propose another solution to recording investigations. As an example, most computational investigation recorders struggle in providing critical information regarding the parallel nature of the code being run. Yet we know today that 'Out of Order Execution' is implemented in most architectures and if the simulation depends on it then this crucial information is lost and there is no way to explain why results are different or why we cannot have the same results right away on the same computer.
CoRR-Cmd will allow the scientist to register/unregister execution to record and push them to the cloud. But also be able to rerun the record. The scientist will be able to query the backend through the API too.

### Requirements
* Python
* Python modules: click, docopt, progress, psutil, getpass, httplib2, daemon.

### Bugs
* If you find a bug, please [email me](mailto:faical.congo@nitst.gov)

### TODO
* Assess the path clearly from a CoRR record (json) to a CoRR record with a Container based system, a Virtual Machine system, a Packaging system, etc...
* Parallel meta-data information in extended. But multiple execution dependencies.
* Upload input/output files more robust for big size.
* Psutil difference in io between inputs and outputs files.
* Auto sync deamon with pid in the config file. for automatic sync of inconsistent projects.
* Auto sync of records is already taken care of by the watcher. Yet previous records are lost while live inspecting.

### Quickstart
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