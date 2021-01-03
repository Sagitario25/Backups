from gestor import Gestor
import os
import time
import log
import reader

def mkdir (newdirs):#Creation of new dirs
	absolutePath, newdirs = os.path.splitdrive (newdirs)
	for i in newdirs.split ('\\'):
		if not os.path.exists (os.path.join (absolutePath, i)):
			os.mkdir (os.path.join (absolutePath, i))

		absolutePath = os.path.join (absolutePath, i)

def relativePath (relative = ""):#Relative path
	return os.path.join (os.path.dirname (__file__), relative)

def backupPath (fromPath, toPath, logger = None, display = True):#Everythong related to the creation of the backup
	if not os.path.exists (toPath):
		mkdir (toPath)
	name = toPath.split ('\\')[-1]

	#Read the data from fromPath
	if display:
		print (f"Opening {name}")
	if logger != None:
		logger.write (f"\n-{name}\n")
	with Gestor (fromPath, toPath) as gest: 
		if display:
			print ("	Comparing...")
		if not gest.compare ():#Compare if new version is needed
			#New version
			if display:
				print ("\tNew version needed. Copying...")
			if logger != None:
				logger.write (f"\tcreating new version\t{time.ctime ()}\n")
			gest.move (newDir = copyTime)
			if logger != None:
				logger.write (f"\tend of new version\t{time.ctime ()}\n")
		else:
			#No need
			if display:
				print ("\tLast version is updated. No need to copy.")
			if logger != None:
				logger.write (f"\tno need to copy\n")

	print (f"{name} ended.")


def main ():
	#Reads config.txt and asigns its data
	lastcommand = None
	dirsPath = None
	settings = reader.Config (relativePath ('config.txt'))

	dirsPath = settings.get ("where")
	lastcommand = settings.get ("lastcommand")


	#Prepairments
	mkdir (os.path.join (dirsPath, "logs"))
	logfile = log.Log (os.path.join (dirsPath, "logs", f"{str (copyTime)}.txt"), "a")
	logfile.write ("starting\n")

	copies = reader.Config (os.path.join (dirsPath, 'copy.txt'))
	copiesPath = copies.labels
	copiesInfo = copies.contents


	#Actual copying
	for i in copiesPath:
		#Get fromPath and toPath from the copy file
		origin = i
		backup = os.path.join (dirsPath, copiesInfo [i])
		backupPath (origin, backup, logfile)

	logfile.write (f"ended {time.ctime ()}\n")
	logfile.close ()
	os.system (lastcommand)

if __name__ == "__main__":
	copyTime = time.time ()
	main ()