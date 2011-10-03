#!/usr/bin/env python
# coding: utf-8
import pynotify
import subprocess
import threading

def check(server, port):
	# Use quaqut to query the server for players.
	return subprocess.Popen("./quaqut -y -p %s %s" % (port, server),shell=True, stdout=subprocess.PIPE)
	
def skip(output,n):
	#Skip lines
	for i in range(n):
		output.stdout.readline()
		
def read(output):
	#Skip the Header
	skip(output, 2)
	
	# If the server is empty dont do anything.
	if output.stdout.readline() == "No information to display\n":
		return
	else:
		skip(output, 1)
		A = []
		while True:
			if output.stdout.readline(2) != "":
				N = output.stdout.readline(27).rsplit()
				if N != "Red Team Score            " and N != "Blue Team Score           ":
					A.append(N[0])
					skip(output, 1)
				else:
					break
			else:
				break

	
if __name__ == "__main__":
	read(check("200.123.156.25","5555"))
