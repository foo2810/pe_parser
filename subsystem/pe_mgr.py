
import os
from threading import Thread
from pe_parser.readpe import PEReader

class PEMgr:
	readerList = dict()
	currentFile = None
	
	@classmethod
	def init(cls):
		print("PE Manager initialized")
	
	@classmethod
	def addFile(cls, fname):
		absPath = os.path.abspath(fname)
		if os.path.exists(absPath):
			reader = PEReader(absPath)
			cls.readerList[absPath] = reader
			if not reader.parse():
				return False
			
			return True
			
		else:
			return False
	
	@classmethod
	def addFileE(cls, fname, handler):
		def _process():
			sof = cls.addFile(fname)
			handler(sof)
		
		thread = Thread(target=_process)
		thread.start()
		
	@classmethod
	def removeFile(cls, fname):
		if fname in cls.readerList:
			cls.readerList[fname] = None
	
	@classmethod
	def getReader(cls, fname):
		fname = os.path.abspath(fname)
		if fname in cls.readerList:
			return cls.readerList[fname]
		else:
			return None
	
	"""
	@classmethod
	def focusFile(cls, fname):
		fname = os.path.abspath(fname)
		if fname in cls.reader:
			cls.currentFile = fname
			return True
		else:
			return False
	"""
