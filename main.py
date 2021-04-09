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

def output (message, display = False, logger = None, addLog = "\n"):
	if display:
		print (message)
	if logger != None:
		logger.write (message + addLog)

def backupPath (fromPath, toPath, logger = None, display = True):#Everythong related to the creation of the backup
	if not os.path.exists (toPath):
		mkdir (toPath)
	name = toPath.split ('\\')[-1]

	#Read the data from fromPath
	output (f"\tOpening {name}", display = display, logger = logger)
	try:
		with gestor.Gestor (fromPath, toPath) as gest: 
			output ("\t\tComparing...", display = display)
			if not gest.compare ():#Compare if new version is needed
				#New version
				output ("\t\tNew version needed. Copying...", display = display, logger = logger)
				gest.move (newDir = copyTime)
				output (f"\t\tend of new version\t{time.ctime ()}\n", logger = logger)
			else:
				#No need
				output ("\t\tLast version is updated. No need to copy.", display = display, logger = logger)
	except Exception as error:
		output ("\t\tAn error acurred during the process", display = display, logger = logger)
		output (f'\t\tGo to log to get more information "{logger.path}"', display = display)
		output (f"\t\t{str (error)}", logger = logger)

	output (f"\t{name} ended.\n", display = display, logger = logger)

def clearBackup (path, gulagPath = None, logger = None, display = True):
	name = path.split ('\\')[-1]
	output (f"\tOpening {name}", display = display, logger = logger)
	output (f"\t\tAnalising...", display = display, logger = logger)
	gest = gestor.versionGestor (path)
	tokeep = gest.clean ()
	output (f"\t\tDeleting {tokeep.count (False)} versions...", display = display, logger = logger)
	output (f"{str (gest.getunwanted ())}\n", logger = logger)
	mkdir (gulagPath)
	gest.delversions (gulagPath)

	output ("\tCleaning ended\n", display = display)

def main ():
	#Reads config.txt and asigns its data
	lastcommand = None
	dirsPath = None
	settings = reader.Config (relativePath ('config.txt'))

	dirsPath = settings.get ("where")
	lastcommand = settings.get ("lastcommand")


	#Prepairments
	mkdir (os.path.join (dirsPath, "- logs"))
	logfile = log.Log (os.path.join (dirsPath, "- logs", f"{str (copyTime)}.txt"), "a")
	logfile.write ("starting\n")

	copies = reader.Config (os.path.join (dirsPath, 'copy.txt'))
	copiesInfo = copies.contents

	#Actual copying
	output ("Starting backup creation", display = True, logger = logfile)
	for i in copiesInfo:
		#Get fromPath and toPath from the copy file
		origin = i
		backup = os.path.join (dirsPath, copiesInfo [i])
		backupPath (origin, backup, logfile)
	output (f"Ending backup creation {time.ctime ()}", logger = logfile)

	#Deletion of unnecesary versions
	output ("\nStarting version cleaner", display = True, logger = logfile)
	for i in copiesInfo:
		path = copiesInfo [i]
		clearBackup (path = os.path.join (dirsPath, path), gulagPath = os.path.join (dirsPath, "- gulag", path), logger = logfile)
#Delete old versions in gulag
#add error to reading

	#End
	logfile.close ()
	os.system (lastcommand)

if __name__ == "__main__":
	copyTime = time.time ()
	main ()