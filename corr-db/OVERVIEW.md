# Simulation Management Tools

An important part of the MGI effort is providing infrastructure and
tools to enable reproducible research in computational materials
science. For reproducible research to become a widely used, repeatable
human based process needs to be replaced by automated open-source
logging tools. This is especially the case for simulation management,
which is often poorly documented and recorded during the development
stages of a research project. A good practice is to use a dedicated
simulation management tool (SMT) throughout the development process
rather than creating an ad-hoc simulation management scheme. Listed
below are a number of requirements for an effective SMT.

## Cloud of Reproducible Records Plateform

CoRR is a Plateform designed to store records from SMT initially.
It allows scientists to automatically push their record in the cloud
and be able to display and manipulate them later. Also CoRR is a 
collaboration platform where the interaction between scientists lead to:
- Discussion about records
- Rationels inclusion
- Reproducible tags between each couple of records as: repeated, replicated,
reproduced, non-repeated, non-replicated, non-reproduced.

CoRR has a web front end and an API that can be scripted and 
used in many simulation management tools, Benchmarking tools, Evaluation tools,
Statistical tools or any other computation regarding a set of records.
CoRR Cloud Plateform is divided into four entities: A cloud and api
backend, a database backend and a frontend view. It can be deployed on
web hosting services like AWS, Google Apps or Heroku.

The development repository for CoRR Database backend is on
[GitHub](https://github.com/faical-yannick-congo/corr-db).

## The Sumatra Client

One particular SMT that is currently being integrated is Sumatra. It is
a is a lightweight system for recording the history and provenance
data for numerical simulations. It works particularly well for
scientists that are in the intermediate stage between developing a
code base and using that code base for active research. This is a
common scenario and often results in a mode of development that mixes
branching for both code development and production simulations. Using
Sumatra avoids this unintended use of the versioning system by
providing a lightweight design for recording the provenance data
independently from the versioning system used for the code
development. The lightweight design of Sumatra fits well with existing
ad-hoc patterns of simulation management contrasting with more
pervasive workflow tools, which can require a wholesale alteration of
work patterns. Sumatra uses a straightforward Django-based data model
enabling persistent data storage independently from the Sumatra
installation.

## Requirements for the Client

### Automation

Ideally for a computation, the logging and recording process is entirely
automated with the only researcher contribution being a small 
"commit messages" that logs the researcher's thoughts, reasons and 
outcomes for running the simulation.

### Integrated with Version Control

The SMT should be entirely integrated and aware of the common
distributed version control (DVC) tools such as Git, Bazaar, Svn and
Mercurial. The provenance data and simulation data should not be
recorded by the version control system, only the SMT project data
should be held in version control.

### REST API

The SMT client should communicate using the REST API completely
independent of any backend databases.

### Simple Local Recrods Storage

The SMT should have a simple local store (dump to JSON) for when the
API is unavailable.

### Data

Output data files should be hashed to enable effective replication and
future regression testing with a continuous integration tool.

### Integrate low level tests

Low overhead for integration of low level regression tests with each
provenance record.

### Record Dependencies

All dependencies should be automatically recorded as well as
uninstalled development repositories that the simulation depends
on. This is hard to achieve across multiple language barriers, but one
of the most important requirements.

### Live Inspection

The SMT should be aware of the status of live jobs and send updates
via the API.

### Parallel

The SMT needs to be aware of provenance data associated with parallel
jobs (such as which nodes are being used) as well as awareness of
various queuing systems.

### Other Provenance Data

Every record (simulation) should have a unique ID and an associated time stamp.

### Federation

The entire CoRR platform can be used as a federation platform. Meaning that it
can be linked to more than one CoRR Database instance.
Provided many cloud hostnames and the credentials to access them, the frontend
is able to federate the queries and statistics from all the cloud provided.
