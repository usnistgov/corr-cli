### What is it?
CoRR (Cloud of Reproducible Records) is a cloud platform that allows scientists to record their investigations (computational or experimental) in the cloud to allow a better share and collaboration around the reproducible nature of their work. CoRR also expose an API for 3rd Party application like Benchmarking, Scoring, Reproducibility Assessment, Learning to hook up to all the publicly shared records and their meta-data for the better good in Science.
CoRR-Cmd is the client that allow research to interact with his/her cloud space. It was created to propose another solution to recording investigations. As an example most computational investigation recorders struggle in providing critical information regarding the parallel nature of the code being run. Yet we know today that 'Out of Order Execution' is implemented in most architectures and if the simulation depends on it then this crucial information is lost and there is no way to explain why my result is different that another one or why i cannot have the same result right away on my own computer.
CoRR-Cmd will allow the scientist to register/unregister execution to record and push them to the cloud. But also be able to rerun the record. CoRR-Cmd will live in a Container/System/Cluster that has visibility to all the runing codes to record from. The scientist will be able to query the backend through the API too.

### Requirements
* Python
* Python modules: Pillow, click, docopt, progress, psutil, 

### Bugs
* If you find a bug, please [email me](mailto:yannick.congo@gmail.com)

### TODO
* Assess the path clearly from a CoRR record (json) to a CoRR record with a Container based system, a Virtual Machine system, a Packaging system, etc...

### Quickstart
* `git clone https://github.com/faical-yannick-congo/CoRR-Cmd.git`
* `cd CoRR-Cmd`
* `python setup.py install`
# Admin section
* `corr --serve` Ask for an admin password.
* `corr --user --add fyc` Will add user fyc
* `corr --user --remove fyc` Will remove user fyc
* `corr --user --list` Will list the users.
* `corr --hook corr_server_host`
* `corr --register "pymks-demo"`
