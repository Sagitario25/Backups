import os
import file

class Tree:
	def __init__ (self, path, openFiles = True):
		self.path = path
		self.files = {}
		self.filesNames = []
		self.dirs = {}
		self.dirsNames = []

		if not os.path.exists (self.path):
			os.mkdir (self.path)

		for i in os.listdir (self.path):
			if os.path.isfile (os.path.join (self.path, i)):
				self.files [i] = file.newFile (os.path.join (self.path, i), bookFile = openFiles)
				self.filesNames.append (i)
			else:
				self.dirs [i] = Tree (os.path.join (self.path, i), openFiles)
				self.dirsNames.append (i)

	def copy (self, path):
		for i in self.filesNames:
			self.files [i].copy (path)

		for i in self.dirsNames:
			os.mkdir (os.path.join (path, i))
			self.dirs [i].copy (os.path.join (path, i))

	def getTreeList (self):
		self.tree = []
		self.tree.append (self.dirsNames)
		for i in self.dirsNames:
			self.tree.append (self.dirs [i].getTreeList ())

		self.tree.append (self.filesNames)
		return self.tree