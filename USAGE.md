# Using CoRR-cli

CoRR-cli is a very simple tool for recording jobs executed at the
command line. It makes recording executions extremely straightforward
requiring only the most minimal change to the workflow. It uses a
"watcher" daemon process that observes other designated processes and
records information about those processes and stores that information
as a permanent record.

## Quickstart

### Configuration

Firstly [install](INSTALLATION.md) CoRR-cli and then configure using,

    $ corrcli config set --email=my.email@test.com --author="My Name"
    Write 'email = my.email@test.com' to config.ini.
    Write 'author = My Name' to config.ini.

To check the configuration use,

    $ corrcli config list
    [default]
    email = my.email@test.com
    author = My Name

The configuration is not strictly required, however, it is nice to
have the author name and email saved with the task records.

### Watchers

In CoRR-cli, the watched processes are known as "tasks" while the
watching deamon is a "watcher". To start a watcher use,

    $ corrcli watch start
    Launch daemon with ID: e58d5000c5f4

A watcher daemon is now running. To check for running watcher use

    $ corrcli watch list
       daemon_id  process_id
    e58d5000c5f4        1230

Note that multiple watchers can run at once and watchers can watch an
unlimited number of processes. To stop a watcher use,

    $ corrcli watch stop e58d5000c5f4
    Stopping watchers.
    Stopped e58d5000c5f4 with pid 1230

Use `--all` to stop all running watchers. Start up another watcher,

    $ corrcli watch start
    Launch daemon with ID: 3fb28b6527e6

### Tasks

To record processes, jobs or tasks, the daemon ID is required to be
present on the command line of the job being executed. So, to record a
very trivial task use,

    $ python -c "import time; time.sleep(3)" 3fb28b6527e6

Remember to copy the tag from the watcher which will be different from
`3fb28b6527e6`. To check that the task was recorded use,

    $ corrcli task list
          label    status           time stamp   pid
    0  a056b686  finished  2016-06-28 12:37:42  7559

This is the most basic information about the job being executed such
as the pid and the status of the task. Each task is also given a
unique label. A longer view of the task's data can be view by passing
the task label.

    $ corrcli task list a056b686
    {
      "author": "Daniel Wheeler",
      "cmdline": [
        "python",
        "-c",
        "import time; time.sleep(60)",
        "149965edff3e"
      ],
      "created_time": "2016-06-28 12:37:42.311173",
      "cwd": "/home/wd15/git/corr-cli",
      "email": "daniel.wheeler2@gmail.com",
      "executable": "/home/wd15/anaconda/envs/py3/bin/python3.5",
      "label": "a056b6866ceb4cf9bb3ac225a74e1377",
      "memory": 8753152,
      "node_name": "barrow",
      "platform": "Linux-4.4.0-24-generic-x86_64-with-debian-stretch-sid",
      "process_created": 1467131860.49,
      "process_id": 7559,
      "process_name": "python",
      "status": "finished",
      "update_time": "2016-06-28 12:38:42.306564",
      "username": "wd15"
    }

Run another task

    $ python -c "import time; time.sleep(3)" 3fb28b6527e

and

    $ corrcli task list
          label    status           time stamp   pid
    0  da053784  finished  2016-06-28 18:37:39  1908
    1  a056b686  finished  2016-06-28 12:37:42  7559

There are now two tasks in the list. To delete tasks use,

    $ corrcli task remove a056b686
    Remove task a056b686 from the file data store? [y/N]: y
    Task a056b686 removed.
    $ corrcli task list
          label    status           time stamp   pid
    0  da053784  finished  2016-06-28 18:37:39  1908

## More to come ...
