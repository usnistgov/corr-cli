import hashlib
import datetime
from time import sleep

if __name__ == '__main__':
	while True:
		sleep(2)
		print hashlib.sha256(b'HashTime_%s'%(str(datetime.datetime.utcnow()))).hexdigest()