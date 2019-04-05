
from subsystem.view_mgr import ViewMgr
from subsystem.pe_mgr import PEMgr

from view.app import App

class System:
	def __init__(self):
		pass
	
	def init(self):
		self._subSystemInit()
		self.mainView = App()
		print("System initialized")
	
	def fin(self):
		PEMgr.fin()
		ViewMgr.fin()
		print("System destructed")
	
	def _subSystemInit(self):
		PEMgr.init()
		ViewMgr.init()
	
	def run(self):
		self.mainView.run()
