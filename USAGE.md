# Using CoRR-cli

## Configure CoRR-cli

It is first necessary to create an account on the CoRR app and
donwload an API key (`API_KEY`). To configure CoRR-cmd to use the
front end app, use

    $ corrcli --config --host=[API_HOST_ADDRESS] --port=[API_PORT_NUMBER] --key=[API_KEY]

To check that the API key is working use,

    $ corrcli --conx

## Register a software project

To register a software project (`SOFTWARE_NAME`) so that CoRR-cmd can
record simulations, use

    $ corrcli --register --name=[SOFTWARE_NAME]
    [MARKER]

The `--register` command returns a marker that can be used to record
simulations.

To remove a software project from being recorded by CoRR-cmd, use

    $ corrcli --unregister --name=[SOFTWARE_NAME] --marker=[MARKER]

To view all the software projects currently being watched by Corr, use

    $ corrcli --list

## Sync the local and remote CoRR records

CoRR-cmd allows offline simulations to be exectued and later
uploaded. It is always a good idea to sync the local store with the
cloud store. To do this, use

    $ corrcli --align

## Start recording simulations

Once the software project is registeed and a marker (`MARKER`) has
been obtained, a deamon is started that watches for when the software
(`SOFTWARE_NAME`) is run,

    $ corrcli --watch --name=[SOFTWARE_NAME] --marker=[MARKER]

Now to stop watching the simulations use

    $ corrcli --unwatch --name=[SOFTWARE_NAME] --maker=[MARKER]
