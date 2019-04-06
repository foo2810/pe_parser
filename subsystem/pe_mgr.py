
import os
from threading import Thread
from pe_parser.readpe import PEReader

class PEMgr:
	readerList = dict()
	
	@classmethod
	def init(cls):
		print("PE Manager initialized")
	
	@classmethod
	def fin(cls):
		rl = cls.readerList
		for f in rl.keys():
			if rl[f] is None:
				return
			cls.removeFile(f)
	
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
	# pe_mgrサブシステムにファイルの追加が完了した後の処理をハンドラとして渡す
	# ハンドラには依頼した処理の成否が引数で渡される
		def _process():
			sof = cls.addFile(fname)
			handler(sof)
		
		thread = Thread(target=_process)
		thread.start()
		
	@classmethod
	def removeFile(cls, fname):
		if fname in cls.readerList:
			#del cls.readerList[fname]
			cls.readerList[fname] = None
	
	@classmethod
	def getReader(cls, fname):
		fname = os.path.abspath(fname)
		if fname in cls.readerList:
			return cls.readerList[fname]
		else:
			return None

