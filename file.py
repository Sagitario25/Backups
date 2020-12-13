import os
import shutil

class newFile:
	def __init__ (self, path, bookFile = True):
		self.path = path
		if bookFile:
			self.file = open (self.path, 'r')
		self.name = self.path.split ('\\')[-1]
		self.moddate = os.path.getmtime (self.path)

	def copy (self, path):
		#Copies the file to the desired path
		shutil.copyfile (self.path, os.path.join (path, self.name))