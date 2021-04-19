import os
import file

import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom

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


class Tree:
	def __init__ (self, path):
		"""Starts the tree class. Path is the path to the dir to the root directory of the tree."""
		#Path management
		self.path = path
		if os.path.exists (self.path):#Just making sure the path exists
			if os.path.isfile (self.path):#In case you decided to input the path of a file
				raise Exception (f"The provided path is a file {self.path}")
		else:
			raise Exception (f"There is not such directory {self.path}")

		#XML setup
		self.xml = ET#This will make this eassier
		self.root = self.xml.Element ("root")#This wont be used, but an Element is needed to start adding subelements
		self.dir = self.xml.SubElement (self.root, "dir")#Subelement with all the information
		self.dir.text = self.path.split ("\\")[-1]#Adds the name of the directory to the dir subelement
		
		self.data = self.xml.SubElement  (self.dir, "data")#This will store any information needed from the directory 
		self.xml.SubElement (self.data, "path").text = self.path#Adds the path to the directory

		self.contents = self.xml.SubElement (self.dir, "contents")#Creates the content subelement
		self.files = self.xml.SubElement (self.contents, "files")#Start file subelement
		self.files.set ("amount", "0")#Add file counter
		self.dirs = self.xml.SubElement (self.contents, "dirs")#Start directory subelement
		self.dirs.set ("amount", "0")#Start directory counter

	def getContent (self):
		"""Loads content of the tree to the XML"""
		for i in os.listdir (self.path):
			self.temppath = os.path.join (self.path, i)
			if os.path.isfile (self.temppath):
				if "ï" in self.temppath:
					raise Exception (f"Path cant contain ï {self.temppath}")
				self.addFile (self.path, i)
			else:
				self.addDir (self.temppath)
				
	def addFile (self, path, filename):
		"""Adds file to the XML. Internal use."""
		self.files.set ("amount", str (int (self.files.get ("amount")) + 1))
		self.file = self.xml.SubElement (self.files, "file")
		self.file.set ("moddate", str (os.path.getmtime (path)))
		self.file.text = filename

	def addDir (self, path):
		"""Adds dir to the XML. Internal use."""
		self.newDir = Tree (path)
		self.newDir.getContent ()
		self.newXML = self.newDir.dir
		self.dirs.set ("amount", str (int (self.dirs.get ("amount")) + 1))
		self.dirs.append (self.newXML)

	def save (self, path, encoding = "UTF-8"):
		"""Saves the XML to the specified files"""
		self.xml.ElementTree (self.dir).write (path, encoding = encoding)
	
	def XMLObject (self):
		"""Returns XML as object"""
		return self.dirs

	def returnXML (self):
		"""Returns XML as string"""
		return self.xml.tostring (self.dir, encoding = "UTF-8", method = "xml").decode ()

	def prettify (self):
		"""Return XML as a prettified string"""
		return minidom.parseString (self.returnXML ()).toprettyxml ()
