import daemon
from corrTask import CoRRTask
import traceback
import sys

#corr will not use a server anymore.
#it will be a single client command run along side the command: as --cmd "command to run"
# run also with --corr-root id_1abc3x

# tasks = {}
# daemon.start()
# def register(name):
#     try:
#         task = CoRRTask(pid='/home/fyc/tasks/%s.pid'%name, name=name)
#         task.start()
#         tasks.setdefault()
#     except:
#         traceback.print_exc(file=sys.stdout)
#     # task = CoRRTask(name=name)
#     # try:
#     #     with daemon.DaemonContext() as context:
#     #         task.run(context)
#     #     tasks['%s'%name]=task
#     # except:
#     #     traceback.print_exc(file=sys.stdout)

# def unregister(name):
#     try:
#     	task = tasks.get('%s'%name)
#         task.stop()
#         del tasks['%s'%name]
#     except KeyError:
#     	traceback.print_exc(file=sys.stdout)
#         print 'No current task watching this execution.'

