from dir import Tree
import cleaner
import reader

import os
import time
import shutil

def compareStrings (list1, list2):
	#Compares two strings efficently
	if len (list1) != len (list2):
		return False

	for i in range (0, len (list1)):
		if type (list1 [i]) != type (list2 [i]):
			return False

		if type (list1 [i]) == type ([]):
			if compareStrings (list1 [i], list2 [i]):
				continue
			else:
				return False

		if list1 [i] != list2 [i]:
			return False

	return True

def compareDate (tree1, tree2):
	for i in tree1.filesNames:
		if tree1.files [i].moddate > tree2.files [i].moddate:
			return False

	for i in tree1.dirsNames:
		if not compareDate (tree1.dirs [i], tree2.dirs [i]):
			return False

	return True

def getVersions (path):
    versions = []
    for i in os.listdir (path):
        if os.path.isdir (os.path.join (path, i)):
            try:
                versions.append (float (i))
            except:
                pass
    return versions

class Gestor:
	def __init__ (self, fromPath, toPath, openFiles = False):
		self.fromPath = fromPath
		self.toPath = toPath

		self.toTree = Tree (self.toPath, openFiles = openFiles)
		self.fromTree = Tree (self.fromPath, openFiles = openFiles)

		self.versions = []
		if not os.path.exists (self.toPath):
			os.mkdir (self.toPath)
		for i in os.listdir (self.toPath):
			if os.path.isdir (os.path.join (self.toPath, i)):
				try:
					self.versions.append (float (i))
				except:
					pass

		try:
			self.max = max (self.versions)
		except:
			self.max = 0

		if self.max == 0:
			self.time = time.time ()
			os.mkdir (os.path.join (self.toPath, str (self.time)))
			self.max = self.time

		self.newest = os.path.join (self.toPath, str (self.max))
		self.newestTree = Tree (self.newest, openFiles = openFiles)

	def compare (self):
		if compareStrings (self.fromTree.getTreeList (), self.newestTree.getTreeList ()):
			return compareDate (self.fromTree, self.newestTree)
		else:
			return False

	def move (self, newDir = None):
		self.time = time
		self.where = self.toPath
		newDir = str (newDir)
		if newDir != None:
			os.mkdir (os.path.join (self.toPath, newDir))
			self.where = os.path.join (self.where, newDir)
		self.fromTree.copy (os.path.join (self.toPath, self.where))

	def __enter__ (self):
		return self

	def __exit__(self, exc_type = None, exc_value = None, traceback = None):
		pass

class versionGestor:
	def __init__ (self, path):
		self.versions = getVersions (path)
		self.path = path
	
	def clean (self):
		from main import relativePath
		self.gestor = cleaner.VersionCleaner (versions = self.versions, settings = reader.Config (relativePath ("cleanerconfig.txt")))
		self.gestor.byage ()
		self.gestor.bydist ()
		self.gestor.bycant ()
		self.gestor.proccess ()

		return self.gestor.save

	def delversions (self, gulag):
		for i in range (len (self.gestor.save)):
			if (not self.gestor.save [i]) and (not os.path.exists (os.path.join (gulag, str (self.versions [i])))):
				shutil.move (os.path.join (self.path, str (self.versions [i])), gulag)

	def getunwanted (self):
		self.result = []
		for i in range (len (self.versions)):
			if self.gestor.save [i] == False:
				self.result.append (self.versions [i])
		return self.result


if __name__ == "__main__":
	versionGestor (r"E:\Copia de seguridad\Informatica").clean ()