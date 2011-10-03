#!/usr/bin/env python
# coding: utf-8
import pynotify
import subprocess
import threading
import time

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
					return A
			else:
				return A

def analysis (server, port):
	A = read(check(server, port))
	while True:
		time.sleep(30)
		B = read(check(server, port))
		if A != B:
			Old = compare(A, B)
			New = compare(B, A)
			if len(Old) != 0:
				print Old				
			if len(New) != 0:
				print New
			A = B		

def compare(A, B):
	C = []
	for i in range(len(A)):
		Found = False
		for j in range(len(B)):
			if A[i] == B[j]:
				Found = True
		if not Found:
			C.append(A[i])
	return C
	
if __name__ == "__main__":
	analysis("200.123.156.25","5555")
