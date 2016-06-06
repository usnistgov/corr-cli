# Using CoRR-cmd

## Configure CoRR-cmd

It is first necessary to create an account on the CoRR app and
donwload an API key (`API_KEY`). To configure CoRR-cmd to use the
front end app, use

    $ corrcmd --config --host=[API_HOST_ADDRESS] --port=[API_PORT_NUMBER] --key=[API_KEY]

To check that the API key is working use,

    $ corr --conx

## Register a software project

To register a software project (`SOFTWARE_NAME`) so that CoRR-cmd can
record simulations, use

    $ corr --register --name=[SOFTWARE_NAME]
    [MARKER]

The `--register` command returns a marker that can be used to record

To remove a software project from being recorded by CoRR-cmd, use

    $ corr --unregister --name software_name --marker software_marker

To view all the software projects currently being watched by Corr, use

    $ corr --list

## Sync the local and remote CoRR records

CoRR-cmd allows offline simulations to be exectued and later
uploaded. It is always a good idea to sync the local store with the
cloud store. To do this, use

    $ corr --align

## Start recording simulations

Once the software project is registerd
