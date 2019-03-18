
class ViewMgr:
	viewList = dict()
	
	@classmethod
	def init(cls):
		print ("View Manager initialized")
	
	@classmethod
	def registerView(cls, view, vid):
		cls.viewList[vid] = view
	
	@classmethod
	def unregisterView(cls, vid):
		del cls.viewList[vid]
	
	@classmethod
	def getView(cls, vid):
		if vid in cls.viewList:
			return cls.viewList[vid]
		else:
			return None
