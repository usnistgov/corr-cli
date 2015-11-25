# Simulation Management Tools AJAX frontend

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
To run this, you have to run the database first:

    $ jekyll serve -H localhost

By default it will run on your localhost on port 4000.

## [Sumatra]()

Sumatra is a command line tool that captures a lot of meta-data
pertaining to a Python execution. Sumatra is primarily aimed at
scientists using Python to run simulations, but the ideas could extend
to many other uses. The captured meta-data is not scientific specific,
but scientist often run the same script multiple times with only
slight modifications to parameter values. Version control alone is not
good at capturing this aspect of the scientific process.

## More reasons for CoRR

CoRR has a web front end and an API that can be scripted and 
used in many simulation management tools (Sumatra), Benchmarking tools,
Evaluation tools, Statistical tools or any other computation regarding
a set of records. CoRR Cloud Plateform is divided into four entities: A
cloud and api backend, a database backend and a frontend view. It can 
be deployed on web hosting services like AWS, Google Apps or Heroku.

## License

[The MIT license.][LICENSE]

## Instances

There are no current instances of the App, but we're working on making
an instance available.

## Prerequisites and Installation

See the [installation guide](INSTALLATION.md).