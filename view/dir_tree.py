import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from subsystem.view_mgr import ViewMgr
from subsystem.pe_mgr import PEMgr

import logo_messages

class DirTreeView(ttk.Frame):
	def __init__(self, master):
		super().__init__(master)
		#self.rootNode = None
		#self.isClear = True
		#self.pefile = None
		self.fNodeList = dict()	# 複数ファイルの同時表示に対応
		self.init()
	
	def init(self):
		self.tree = ttk.Treeview(self)
		self.tree.column("#0", stretch=True, minwidth=500)	# minwidthはPCの画面サイズを設定すべき？
		self.tree.configure(columns=["reserved", "kind", "belongs"])
		self.tree.configure(displaycolumns=[])
		
		xsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
		ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
		self.tree.configure(xscroll=xsb.set, yscroll=ysb.set)
		self.tree.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		xsb.grid(column=0, row=1, sticky=(tk.E, tk.W))
		ysb.grid(column=1, row=0, sticky=(tk.N, tk.S))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		
		self.tree.heading("#0", text="PE Info", anchor="w")
		
		#self.tree.bind("<<TreeviewOpen>>",  self.dirOpenHandler)
		self.tree.bind("<<TreeviewSelect>>", self.fileSelectHandler)
		
		#self.rootNode = self.tree.insert("", "end", text="PE Info", values=[None, "root", None], open=True)
		
	def _processDirectory(self, parent, pefile):
		self._reader = PEMgr.getReader(pefile)
		if not self._reader:
			messagebox.showinfo("Error", "Failed to get reader")
			return False
		
		self.tree.item(parent, text=os.path.basename(pefile))

		msdosNode = self.tree.insert(parent, "end", text="MSDOS Header", values=[None, "MSDOS_HEADER", pefile], open=False)
		fNode = self.tree.insert(parent, "end", text="File Header", values=[None, "FILE_HEADER", pefile], open=False)
		ntNode = self.tree.insert(parent, "end", text="NT Header", values=[None, "NT_HEADER", pefile], open=False)
		optNode = self.tree.insert(parent, "end", text="Optional Header", values=[None, "OPTIONAL_HEADER", pefile], open=False)
		
		sectionList = self._reader.getSectionList()
		sTableNode = self.tree.insert(parent, "end", text="Section Headers", values=[None, "SECTION_TABLE", pefile], open=False)
		for s in sectionList:
			self.tree.insert(sTableNode, "end", text=s, values=[None, "SECTION_TABLE_ENTRY", pefile])
		
		exportFuncList = self._reader.getExportFuncNameList()
		eTableNode = self.tree.insert(parent, "end", text="Export Table", values=[None, "EXPORT_TABLE", pefile], open=False)
		for e in exportFuncList:
			self.tree.insert(eTableNode, "end", text=e, values=[None, "EXPORT_TABLE_ENTRY", pefile])
		
		importDllList = self._reader.getImportDllList()
		iTableNode = self.tree.insert(parent, "end", text="Import Table", values=[None, "IMPORT_TABLE", pefile], open=False)
		for i in importDllList:
			node = self.tree.insert(iTableNode, "end", text=i, values=[None, "IMPORT_TABLE_ENTRY", pefile], open=False)
			for f in self._reader.getImportFunctionList(i):
				self.tree.insert(node, "end", text=f, values=[None, "IMPORT_TABLE_ENTRY2", pefile])
		
		relocBaseList = self._reader.getBaseRelocationList()
		rTableNode = self.tree.insert(parent, "end", text="Relocation Table", values=[None, "RELOCATION_TABLE", pefile], open=False)
		for baseReloc in relocBaseList:
			baseAddr = baseReloc["VirtualAddress"]
			baseRelocNode = self.tree.insert(rTableNode, "end", text="{:#x}".format(baseAddr), values=[None, "RELOCATION_TABLE_ENTRY", pefile], open=False)
			for e in self._reader.getRelocationEntryList(baseAddr):
				self.tree.insert(baseRelocNode, "end", text="{:#x}".format(e), values=[None, "RELOCATION_TABLE_ENTRY2", pefile], open=False)
		#self.tree.insert(rTableNode, "end", text="entry...", values=[None, "RELOCATION_TABLE_ENTRY", pefile], open=False)		
	
		return True
	
	def setTree(self, pefile):
		rootNode = self.tree.insert("", "end", text=os.path.basename(pefile), values=[None, "root", pefile], open=True)
		if self._processDirectory(rootNode, pefile):
			self.fNodeList[pefile] = rootNode
			print("{} set".format(pefile))
		
		return
		
		"""
		if self._processDirectory(self.rootNode, pefile):
			self.pefile = pefile
		"""
	
	def clearTree(self, pefile):
		if pefile in self.fNodeList:
			rootNode = self.fNodeList[pefile]
			self.fNodeList[pefile] = None
			self.tree.delete(rootNode)
			print("{} deleted".format(pefile))
		return
		
		"""
		if not self.isClear:
			self.tree.delete(self.msdosNode)
			self.tree.delete(self.fNode)
			self.tree.delete(self.ntNode)
			self.tree.delete(self.optNode)
			self.tree.delete(self.sTableNode)
			self.tree.delete(self.eTableNode)
			self.tree.delete(self.iTableNode)
			self.tree.delete(self.rTableNode)
			
			self.msdosNode = self.fNode = self.ntNode = self.optNode = self.eTableNode = self.iTableNode = self.rTableNode = None
			self.tree.item(self.rootNode, text="PE Info", values="root")

		self.isClear = True
		self.pefile = None
		"""
	
	def dirOpenHandler(self, evt):
		pass
	
	def fileSelectHandler(self, evt):
		node = self.tree.selection()
		values = self.tree.item(node)["values"]
		ntype = values[1]
		belongs = values[2]
		text = "".join(self.tree.item(node)["text"])
		
		#if ntype == "EXPORT_TABLE" or ntype == "IMPORT_TABLE" or ntype == "RELOCATION_TABLE":
		insertText = None
		if ntype == "root":
			finfo = os.stat(belongs)
			# View file info
			insertText = "Target file: {}\n".format(belongs)
			insertText = insertText + "\tsize: {}\n".format(finfo.st_size)
		else:
			insertText = self._getEntryText(node, ntype, belongs, text)
		
		fileInfoView = ViewMgr.getView("FileInfo")
		if fileInfoView:
			fileInfoView.insertText(insertText)
	
	def _getEntryText(self, node, ntype, belongs, value=""):
		peReader = PEMgr.getReader(belongs)
		
		if not peReader:
			return ""
		
		text = None
		
		if ntype == "EXPORT_TABLE":
			text = ntype
			
		elif ntype == "EXPORT_TABLE_ENTRY":
			addr = peReader.getExportFuncAddr(value)
			text = "{}\n\n+ VRVA: {:#018x}".format(value, addr)
			if peReader.isExported(value):
				n = peReader.getExportName(addr)
				text = "{} (Export to {})".format(text, n)
				
		elif ntype == "IMPORT_TABLE":
			text = ntype
			
		elif ntype == "IMPORT_TABLE_ENTRY":
			dllInfo = peReader.getImportDllInfo(value)
			strs = list()
			for k in dllInfo.keys():
				if type(dllInfo[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, dllInfo[k]))
				else:
					strs.append("{}: {}\n".format(k, dllInfo[k]))
			text = "".join(strs)
			
		elif ntype == "IMPORT_TABLE_ENTRY2":
			parent = self.tree.parent(node)
			dllVal = "".join(self.tree.item(parent)["text"])
			dllInfo = peReader.getImportDllInfo(dllVal)
			funcInfo = peReader.getImportFunctionInfo(value)
			strs = list()
			strs.append("+ Dll Info\n\n")
			for k in dllInfo.keys():
				if type(dllInfo[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, dllInfo[k]))
				else:
					strs.append("{}: {}\n".format(k, dllInfo[k]))
			
			strs.append("\n+ Function Info\n\n")
			for k in funcInfo.keys():
				if type(funcInfo[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, funcInfo[k]))
				else:
					strs.append("{}: {}\n".format(k, funcInfo[k]))
			text = "".join(strs)
			
		elif ntype == "RELOCATION_TABLE":
			text = ntype
			
		elif ntype == "RELOCATION_TABLE_ENTRY":
			text = ntype
		
		elif ntype == "RELOCATION_TABLE_ENTRY2":
			parent = self.tree.parent(node)
			baseRelocAddr = int(self.tree.item(parent)["text"], 16)
			offset = int(self.tree.item(node)["text"], 16)
			relocInfo = peReader.getRelocationInfo(baseRelocAddr, offset)
			text = "Base Address: {:#x}\nType: {}\nOffset: {:#x}".format(baseRelocAddr, relocInfo["TypeText"], offset)
			
		elif ntype == "SECTION_TABLE":
			text = ntype
			
		elif ntype == "SECTION_TABLE_ENTRY":
			header = peReader.getSectionHeader(value)
			strs = list()
			for k in header.keys():
				if type(header[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, header[k]))
				else:
					strs.append("{}: {}\n".format(k, header[k]))
			text = "\n".join(strs)
			
		elif ntype == "MSDOS_HEADER":
			header = peReader.getMSDosHeader()
			strs = list()
			for k in header.keys():
				if type(header[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, header[k]))
				else:
					strs.append("{}: {}\n".format(k, header[k]))
			text = "\n".join(strs)
			
		elif ntype == "FILE_HEADER":
			header = peReader.getFileHeader()
			strs = list()
			for k in header.keys():
				if type(header[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, header[k]))
				else:
					strs.append("{}: {}\n".format(k, header[k]))
			text = "\n".join(strs)
			
		elif ntype == "NT_HEADER":
			header = peReader.getNTHeader()
			strs = list()
			for k in header.keys():
				if type(header[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, header[k]))
				else:
					strs.append("{}: {}\n".format(k, header[k]))
			text = "\n".join(strs)
			
		elif ntype == "OPTIONAL_HEADER":
			header = peReader.getOptionalHeader()
			strs = list()
			for k in header.keys():
				if type(header[k]) == int:
					strs.append("{}: {:#018x}\n".format(k, header[k]))
				else:
					strs.append("{}: {}\n".format(k, header[k]))
			text = "\n".join(strs)
			
		else:
			text = "Protable Executable"
		
		return text
