import os
import tkinter as tk
import tkinter.ttk as ttk
import view.function as _F

class DirTree(_F.Function):
	def __init__(self, master, fid):
		super().__init__(master, fid)
		self.frame = ttk.Frame(self.master.frame)
		self.rooNode = None
		self.init()
	
	def init(self):
		path = "C:\\Users\\kondo\\Desktop"
		
		self.tree = ttk.Treeview(self.frame)
		self.tree.column("#0", stretch=True, minwidth=1080)	# minwidthはPCの画面サイズを設定すべき？
		
		xsb = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.tree.xview)
		ysb = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
		self.tree.configure(xscroll=xsb.set, yscroll=ysb.set)
		self.tree.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		xsb.grid(column=0, row=1, sticky=(tk.E, tk.W))
		ysb.grid(column=1, row=0, sticky=(tk.N, tk.S))
		self.frame.columnconfigure(0, weight=1)
		self.frame.rowconfigure(0, weight=1)
		
		#self.tree.heading("#0", text="", anchor="w")
		
		#self.tree.bind("<<TreeviewOpen>>",  self.dirOpenHandler)
		self.tree.bind("<<TreeviewSelect>>", self.fileSelectHandler)
		
		self.rootNode = self.tree.insert("", "end", text="PE Info", values="ROOT", open=True)
		
		#self._processDirectory(self.rootNode)
		
		
	def _processDirectory(self, parent):
		peInfoHandler = _F.getFuncHandle("PEInfo")
		
		if not peInfoHandler:
			return
		
		if not peInfoHandler.peReader:
			return

		self.msdosNode = self.tree.insert(parent, "end", text="MSDOS Header", values="MSDOS_HEADER", open=False)
		self.fNode = self.tree.insert(parent, "end", text="File Header", values="FILE_HEADER", open=False)
		self. ntNode = self.tree.insert(parent, "end", text="NT Header", values="NT_HEADER", open=False)
		self.optNode = self.tree.insert(parent, "end", text="Optional Header", values="OPTIONAL_HEADER", open=False)
		
		exportFuncList = peInfoHandler.peReader.getExportFuncNameList()
		self.eTableNode = self.tree.insert(parent, "end", text="Export Table", values="EXPORT_TABLE", open=False)
		for e in exportFuncList:
			self.tree.insert(self.eTableNode, "end", text=e, values="EXPORT_TABLE_ENTRY", open=False)
		
		importDllList = peInfoHandler.peReader.getImportDllList()
		self.iTableNode = self.tree.insert(parent, "end", text="Import Table", values="IMPORT_TABLE", open=False)
		for i in importDllList:
			node = self.tree.insert(self.iTableNode, "end", text=i, values="IMPORT_TABLE_ENTRY", open=False)
			for f in peInfoHandler.peReader.getImportFunctionList(i):
				self.tree.insert(node, "end", text=f, values="IMPORT_TABLE_ENTRY2", open=False)
				
		
		self.rTableNode = self.tree.insert(parent, "end", text="Relocation Table", values="RELOCATION_TABLE", open=False)
		self.tree.insert(self.rTableNode, "end", text="entry...", values="RELOCATION_TABLE_ENTRY", open=False)		
	
	def setTree(self):
		self._processDirectory(self.rootNode)
	
	def resetTree(self):
		self.clearTree()
		self.setTree()
	
	def clearTree(self):
		self.tree.delete(self.msdosNode)
		self.tree.delete(self.fNode)
		self.tree.delete(self.ntNode)
		self.tree.delete(self.optNode)
		self.tree.delete(self.eTableNode)
		self.tree.delete(self.iTableNode)
		self.tree.delete(self.rTableNode)
		
		self.msdosNode = self.fNode = self.ntNode = self.optNode = self.eTableNode = self.iTableNode = self.rTableNode = None
	
	def dirOpenHandler(self, evt):
		pass
	
	def fileSelectHandler(self, evt):			
		node = self.tree.selection()
		type = self.tree.item(node)["values"][0]
		text = "".join(self.tree.item(node)["text"])
		
		if type == "EXPORT_TABLE" or type == "IMPORT_TABLE" or type == "RELOCATION_TABLE":
			return
		
		text = self._getEntryText(type, text)
		
		fileInfoHandler = _F.getFuncHandle("FileInfo")
		if fileInfoHandler:
			fileInfoHandler.insertText(text)
	
	def _getEntryText(self, type, value=""):
		peInfoHandler = _F.getFuncHandle("PEInfo")
		
		if not peInfoHandler:
			return ""
			
		peReader = peInfoHandler.peReader
		
		text = None
		
		if type == "EXPORT_TABLE":
			text = type
		elif type == "EXPORT_TABLE_ENTRY":
			text = "VRVA: {:#018x}".format(peReader.getExportFuncAddr(value))
		elif type == "IMPORT_TABLE":
			text = type
		elif type == "IMPORT_TABLE_ENTRY":
			dllInfo = peReader.getImportDllInfo(value)
			strs = list()
			for k in dllInfo.keys():
				strs.append("{}: {}\n".format(k, dllInfo[k]))
			text = "".join(strs)
		elif type == "IMPORT_TABLE_ENTRY2":
			funcInfo = peReader.getImportFunctionInfo(value)
			strs = list()
			for k in funcInfo.keys():
				strs.append("{}: {}\n".format(k, funcInfo[k]))
			text = "".join(strs)
		elif type == "RELOCATION_TABLE":
			text = type
		elif type == "RELOCATION_TABLE_ENTRY":
			text = type
		elif type == "MSDOS_HEADER":
			header = peReader.getMSDosHeader()
			strs = list()
			for k in header.keys():
				strs.append("{}: {}\n".format(k, header[k]))
			text = "".join(strs)
			
		elif type == "FILE_HEADER":
			header = peReader.getFileHeader()
			strs = list()
			for k in header.keys():
				strs.append("{}: {}\n".format(k, header[k]))
			text = "".join(strs)
		elif type == "NT_HEADER":
			header = peReader.getNTHeader()
			strs = list()
			for k in header.keys():
				strs.append("{}: {}\n".format(k, header[k]))
			text = "".join(strs)
		elif type == "OPTIONAL_HEADER":
			header = peReader.getOptionalHeader()
			strs = list()
			for k in header.keys():
				strs.append("{}: {}\n".format(k, header[k]))
			text = "".join(strs)
		
		return text
