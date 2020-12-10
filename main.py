from gestor import Gestor
import os
import time
import log

def mkdir (absolutePath, newdirs):#Creation of new dirs
	for i in newdirs.split ('\\'):
		if not os.path.exists (os.path.join (absolutePath, i)):
			os.mkdir (os.path.join (absolutePath, i))

		absolutePath = os.path.join (absolutePath, i)

def relativePath (relative = ""):
	return os.path.join (os.path.dirname (__file__), relative)

#Reads config.txt and asigns its data
lastcommand = None
dirsPath = None
for i in open (relativePath ('config.txt')).readlines ():
	index = i.split ('>')[0]
	if index == "where":
		dirsPath = i.split ('>')[1][:-1]
	elif index == "lastcommand":
		lastcommand = i.split ('>')[1][:-1]
file = open (os.path.join (dirsPath, 'copy.txt'), 'r')

#Prepairments
copyTime = time.time ()
mkdir (dirsPath, "logs")
logfile = log.Log (os.path.join (dirsPath, "logs", f"{str (copyTime)}.txt"), "a")
logfile.write ("starting\n")

#Actual copying
for i in file.readlines ():
	#Get fromPath and toPath from the copy file
	if i.split ('>')[0] == "end":
		continue
	fromPath = i.split ('>')[0]
	toPath = os.path.join (dirsPath, i.split ('>')[1][:-1])

	if not os.path.exists (toPath):
		mkdir (dirsPath, i.split ('>')[1][:-1])

	#Read the data from fromPath
	print (f"Opening {i.split ('>')[1][:-1]}")
	logfile.write (f"\n-{i.split ('>')[1][:-1]}\n")
	with Gestor (fromPath, toPath) as gest: 
		print ("	Comparing...")
		if not gest.compare ():#Compare if new version is needed
			#New version
			print ("\tNew version needed. Copying...")
			logfile.write (f"\tcreating new version\t{time.ctime ()}\n")
			gest.move (newDir = copyTime)
			logfile.write (f"\tend of new version\t{time.ctime ()}\n")
		else:
			#No need
			print ("\tLast version is updated. No need to copy.")
			logfile.write (f"\tno need to copy\n")

	print (f"{i.split ('>')[1][:-1]} ended.")
logfile.write (f"ended {time.ctime ()}\n")
logfile.close ()
os.system (lastcommand)