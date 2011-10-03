#!/usr/bin/env python
# coding: utf-8
import pynotify
import subprocess

def check(server, port):
	return subprocess.Popen("./quaqut -y -p %s %s" % (port, server),shell=True, stdout=subprocess.PIPE)
	
def read(output):
	# Skip the header
	output.stdout.readline()
	output.stdout.readline()
	
	print output.stdout.read()
	
if __name__ == "__main__":
	read(check("200.123.156.25","5555"))
