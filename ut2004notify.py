#!/usr/bin/env python
import pynotify
import subprocess
import threading
import time

UT2004Path="/media/Juegos/UT2004/"

def check(server, port):
	# Use quaqut to query the server for players.
	return subprocess.Popen("./quaqut -p %s %s" % (port, server),shell=True, stdout=subprocess.PIPE)
	
def skip(output,n):
	#Skip lines
	for i in range(n):
		output.stdout.readline()
		
def read(output):
	#Skip the Header
	skip(output, 2)
	
	#If the server is down dont do anything.
	if output.stdout.readline(2) != "**":
		return
	else:
		output.stdout.readline(10)
		Server_Name = output.stdout.readline()
	
	#Game Type
	skip(output,1)
	output.stdout.readline(12)
	Game_Type = output.stdout.readline()
	
	skip(output,7)
	# If the server is empty dont do anything.
	if output.stdout.readline() == "No information to display\n":
		return
	else:
		skip(output, 1)
		A = []
		while True:
			if output.stdout.readline(2) != "":
				N = output.stdout.readline(27).rsplit()
				if N[0] != "Red":
					A.append(N[0])
					skip(output, 1)
				else:
					return (A, Server_Name, Game_Type)
			else:
				return (A, Server_Name, Game_Type)

def analysis (server, port):
	A = read(check(server, port))
	while True:
		time.sleep(10)
		B = read(check(server, port))
		if A[0] != B[0]:
			Old = compare(A[0], B[0])
			New = compare(B[0], A[0])
			notify(New, Old, B[1], B[2], len(B[0]))
			A = B		

def compare(A, B):
	C = []
	if B != None:
		for i in range(len(A)):
			Found = False
			for j in range(len(B)):
				if A[i] == B[j]:
					Found = True
			if not Found:
				C.append(A[i])
		return C
	else:
		return A
		
	
def notify(New, Old, Server_Name, Game_Type, Total_Players):
	pynotify.init("UT2004 Notify")
	Notify = ""
	if len(New) != 0:
		Notify += "New Players: "
		for i in range(len(New)):
			Notify += "%s " % New[i]
		Notify += "\n\n"
	if len(Old) != 0:
		Notify += "Players who left: "
		for i in range(len(Old)):
			Notify += "%s " % Old[i]
		Notify += "\n\n"
	Notify += "Game Type: %s\n\n" % Game_Type 
	Notify += "Total Players: %s" % Total_Players
	n = pynotify.Notification(Server_Name.decode("iso8859-1"), Notify.decode("iso8859-1") , "%s/Help/Unreal.ico" % UT2004Path)
	n.show()
	
if __name__ == "__main__":
	analysis("200.123.156.25","5555")
