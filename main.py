import gestor
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
		print (f"\tOpening {name}")
	if logger != None:
		logger.write (f"\n\t-{name}\n")
	with gestor.Gestor (fromPath, toPath) as gest: 
		if display:
			print ("\t\tComparing...")
		if not gest.compare ():#Compare if new version is needed
			#New version
			if display:
				print ("\t\tNew version needed. Copying...")
			if logger != None:
				logger.write (f"\t\tcreating new version\t{time.ctime ()}\n")
			gest.move (newDir = copyTime)
			if logger != None:
				logger.write (f"\t\tend of new version\t{time.ctime ()}\n")
		else:
			#No need
			if display:
				print ("\t\tLast version is updated. No need to copy.")
			if logger != None:
				logger.write (f"\t\tno need to copy\n")

	print (f"\t{name} ended.\n")

def clearBackup (path, logger = None, display = True):
	name = path.split ('\\')[-1]
	if display:
		print (f"\tOpening {name}")
		print (f"\t\tAnalising...")
	if logger != None:
		logger.write (f"\t-{name}\n")
		logger.write (f"\t\tAnalising...\n")
	gest = gestor.versionGestor (path)
	tokeep = gest.clean ()
	if display:
		print (f"\t\tDeleting {len (tokeep)} versions...")
	if logger != None:
		logger.write (f"\t\tDeleting {len (gest.versions) - len (tokeep)} versions...:")
		logger.write (f"{str (gest.invertList(tokeep))}\n")
	gest.delnotinlist (tokeep)

	print ("\tCleaning ended\n")

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
	copiesInfo = copies.contents

	#Actual copying
	logfile.write ("\nStarting backup creation")
	print ("Starting backup creation")
	for i in copiesInfo:
		#Get fromPath and toPath from the copy file
		origin = i
		backup = os.path.join (dirsPath, copiesInfo [i])
		backupPath (origin, backup, logfile)
	logfile.write (f"Ending backupcreation {time.ctime ()}")

	#Deletion of unnecesary versions
	print ("\n\nStarting version cleaner")
	logfile.write ("\nStarting version cleaner\n")
	for i in copiesInfo:
		path = copiesInfo [i]
		clearBackup (os.path.join (dirsPath, path), logfile)
	

	#End
	logfile.close ()
	os.system (lastcommand)

if __name__ == "__main__":
	copyTime = time.time ()
	main ()