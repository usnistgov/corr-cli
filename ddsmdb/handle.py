"""Usage: handle.py [--create | --setup | --run | --clean | --destroy | --migrate] [--debug | --no-debug]

--create        make sure that the database is created.
--setup         will push the zero.json set of projects records as a ground base in the database.
--run   		will cleanup the database to be empty.
--clean   		will cleanup the database to be empty.
--destroy		will destroy the database.
--migrate   	will migrate the database.

"""
from docopt import docopt

if __name__ == "__main__":
	arguments = docopt(__doc__, version='0.1dev')
	debug = not arguments['--no-debug']

	if arguments['--create']:
		print "Creating..."
	if arguments['--setup']:
		print "Setting up..."
	if arguments['--run']:
		print "Running..."
	if arguments['--clean']:
		print "Cleanning up..."
	if arguments['--destroy']:
		print "Destroying..."
	if arguments['--migrate']:
		print "Migrating..."
