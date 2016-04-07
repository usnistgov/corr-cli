"""Usage: controller.py [--process=<process>]

--process=<process>   set the process to watch.

"""
from docopt import docopt
arguments = docopt(__doc__, version='0.1dev')

process = arguments['--process']

import os
import sys, traceback
import psutil
import json
from progress.bar import Bar
import datetime
from time import sleep
import platform

while True:

	pids = psutil.pids()

	stamp = str(datetime.datetime.now())
	bar = Bar('Gathering %s'%stamp, max=len(pids))

	# base = "repository/%s---EventControl"%stamp
	# if not os.path.exists(base): os.makedirs(base)

	for i in xrange(len(pids)):
		try:
			p = psutil.Process(pids[i])
			name = p.name().replace('/', '-')

			if os.path.isfile('repository/%s.json'%name):
				try:
					with open('repository/%s.json'%name, 'r') as info_json:
						info = json.loads(info_json.read())
				except:
					info = {}
					try:
						info['computer'] = {'machine':platform.machine(), 'node':platform.node(), 'platform':platform.platform(aliased=True), 'processor':platform.processor(), 'release':platform.release(), 'system':platform.system(), 'version':platform.version()}
					except:
						info['computer'] = 'unknown'
					try:
						info['name'] = p.name()
					except:
						info['name'] = 'unknown'
					try:
						info['pid'] = i
					except:
						info['pid'] = 'unknown'
					try:
						info['executable'] = p.exe()
					except:
						info['executable'] = 'unknown'
					try:
						info['path'] = p.cwd()
					except:
						info['path'] = 'unknown'
					try:
						info['cmdline'] = p.cmdline()
					except:
						info['cmdline'] = 'unknown'
					try:
						info['owner'] = p.username()
					except:
						info['owner'] = 'unknown'
					try:
						info['created'] = datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
					except:
						info['created'] = 'unknown'
					try:
						info['terminal'] = p.terminal()
					except:
						info['terminal'] = 'unknown'
					info['stamps'] = []
			else:
				info = {}
				try:
					info['computer'] = {'machine':platform.machine(), 'node':platform.node(), 'platform':platform.platform(aliased=True), 'processor':platform.processor(), 'release':platform.release(), 'system':platform.system(), 'version':platform.version()}
				except:
					info['computer'] = 'unknown'
				try:
					info['name'] = p.name()
				except:
					info['name'] = 'unknown'
				try:
					info['pid'] = i
				except:
					info['pid'] = 'unknown'
				try:
					info['executable'] = p.exe()
				except:
					info['executable'] = 'unknown'
				try:
					info['path'] = p.cwd()
				except:
					info['path'] = 'unknown'
				try:
					info['cmdline'] = p.cmdline()
				except:
					info['cmdline'] = 'unknown'
				try:
					info['owner'] = p.username()
				except:
					info['owner'] = 'unknown'
				try:
					info['created'] = datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S")
				except:
					info['created'] = 'unknown'
				try:
					info['terminal'] = p.terminal()
				except:
					info['terminal'] = 'unknown'
				info['stamps'] = []

			details = {'stamp':stamp}
			try:
				threads = p.threads()
				# print threads
				details['threads'] = {'number':len(threads), 'list':threads}
				# for t in threads:
				# 	details['threads']['list'].append({'id':t.id(), 'number':t.numer()})
				# print details['threads']
			except:
				# traceback.print_exc(file=sys.stdout)
				details['threads'] = 'unknown'
			try:
				children = p.children()
				# print children
				details['children'] = {'number':len(children), 'list':[]}
				for c in children:
					details['children']['list'].append({'child':c.pid, 'name':c.name()})
				# print details['children']
			except:
				details['children'] = 'unknown'
			try:
				details['status'] = p.status()
			except:
				details['status'] = 'unknown'
			
			try:
				details['cp_purcentage'] = p.cpu_percent(interval=1.0)
			except:
				details['cp_purcentage'] = 'unknown'
			try:
				details['mem_purcentage'] = p.memory_percent()
			except:
				details['mem_purcentage'] = 'unknown'
			try:
				details['libraries'] = p.memory_maps()
			except:
				details['libraries'] = 'unknown'
			try:
				details['network'] = p.get_connections()
			except:
				traceback.print_exc(file=sys.stdout)
				details['network'] = 'unknown'

			try:
				details['io_files'] = p.open_files()
			except:
				details['io_files'] = 'unknown'

			info['stamps'].append(details)

			if info['name'] != 'unknown':
				with open('repository/%s.json'%name, 'w') as info_json:
					info_json.write(json.dumps(info, sort_keys=True, indent=4, separators=(',', ': ')))

			bar.next()
		except:
			pass
	bar.finish()

#strace system calls.


# MILA
# Theano
# ZeroMW
# dill vs pickle
