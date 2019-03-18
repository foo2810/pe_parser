# Function Base Class

FUNCLIST = dict()

def getFuncHandle(fid):
	if fid in FUNCLIST:
		return FUNCLIST[fid]
	else:
		return None

class Function:
	def __init__(self, master, fid):
		self.master = master
		self.fid = fid
		FUNCLIST[fid] = self
		self.frame = None
	
	def __del__(self):
		del FUNCLIST[self.fid]
	
	def __getattr__(self, fid):
		return FUNCLIST[fid]
	
	def __getitem__(self, fid):
		return FUNCLIST[fid]