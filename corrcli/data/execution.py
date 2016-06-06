from time import sleep
import random

if __name__ == '__main__':
	with open("execution.dump.txt", "w") as exec_dump:
	    for num in range(30):
	        pitch = random.random()
	        exec_dump.write("{0}".format(pitch))
	        sleep(2)

	# There is an issue with psutils geting the io files when 
	# We make atomic open and write instead of a longer open
	# and write
	# with open("execution.dump.txt", "w") as exec_dump:
 #            pitch = random.random()
 #            exec_dump.write("{0}".format(pitch))
 #        sleep(2)