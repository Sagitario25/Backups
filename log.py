class Log:
	def __init__ (self, path, mode):
		self.path = path
		self.mode = mode
		open (self.path, "w")

	def write (self, message):
		open (self.path, self.mode).write (message)
	
	def close (self):
		self.write ("Log closed")
		self.__exit__ ()
	
	def __exit__(self, exc_type = None, exc_value = None, traceback = None):
		pass