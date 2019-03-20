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
		self.rooNode = None
		self.isClear = True
		self.pefile = None
		self.init()
	
	def init(self):
		self.tree = ttk.Treeview(self)
		self.tree.column("#0", stretch=True, minwidth=1080)	# minwidthはPCの画面サイズを設定すべき？
		
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
		
		self.rootNode = self.tree.insert("", "end", text="PE Info", values="root", open=True)
		
		#self._processDirectory(self.rootNode)
		
		
	def _processDirectory(self, parent, pefile):
		reader = PEMgr.getReader(pefile)
		if not reader:
			messagebox.showinfo("Error", "Failed to get reader")
			return False
		
		self.tree.item(self.rootNode, text=os.path.basename(pefile))

		self.msdosNode = self.tree.insert(parent, "end", text="MSDOS Header", values="MSDOS_HEADER", open=False)
		self.fNode = self.tree.insert(parent, "end", text="File Header", values="FILE_HEADER", open=False)
		self. ntNode = self.tree.insert(parent, "end", text="NT Header", values="NT_HEADER", open=False)
		self.optNode = self.tree.insert(parent, "end", text="Optional Header", values="OPTIONAL_HEADER", open=False)
		
		sectionList = reader.getSectionList()
		self.sTableNode = self.tree.insert(parent, "end", text="Section Headers", values="SECTION_TABLE", open=False)
		for s in sectionList:
			self.tree.insert(self.sTableNode, "end", text=s, values="SECTION_TABLE_ENTRY")
		
		exportFuncList = reader.getExportFuncNameList()
		self.eTableNode = self.tree.insert(parent, "end", text="Export Table", values="EXPORT_TABLE", open=False)
		for e in exportFuncList:
			self.tree.insert(self.eTableNode, "end", text=e, values="EXPORT_TABLE_ENTRY")
		
		importDllList = reader.getImportDllList()
		self.iTableNode = self.tree.insert(parent, "end", text="Import Table", values="IMPORT_TABLE", open=False)
		for i in importDllList:
			node = self.tree.insert(self.iTableNode, "end", text=i, values="IMPORT_TABLE_ENTRY", open=False)
			for f in reader.getImportFunctionList(i):
				self.tree.insert(node, "end", text=f, values="IMPORT_TABLE_ENTRY2")
				
		
		self.rTableNode = self.tree.insert(parent, "end", text="Relocation Table", values="RELOCATION_TABLE", open=False)
		self.tree.insert(self.rTableNode, "end", text="entry...", values="RELOCATION_TABLE_ENTRY", open=False)		
	
		return True
	
	def setTree(self, pefile):
		self.clearTree()
		if self._processDirectory(self.rootNode, pefile):
			self.pefile = pefile
			self.isClear = False
	
	def clearTree(self):
		if not self.isClear:
			self.tree.delete(self.msdosNode)
			self.tree.delete(self.fNode)
			self.tree.delete(self.ntNode)
			self.tree.delete(self.optNode)
			self.tree.delete(self.eTableNode)
			self.tree.delete(self.iTableNode)
			self.tree.delete(self.rTableNode)
			
			self.msdosNode = self.fNode = self.ntNode = self.optNode = self.eTableNode = self.iTableNode = self.rTableNode = None
			self.tree.item(self.rootNode, text="PE Info", values="root")

		self.isClear = True
		self.pefile = None
	
	def dirOpenHandler(self, evt):
		pass
	
	def fileSelectHandler(self, evt):			
		node = self.tree.selection()
		ntype = self.tree.item(node)["values"][0]
		text = "".join(self.tree.item(node)["text"])
		
		#if ntype == "EXPORT_TABLE" or ntype == "IMPORT_TABLE" or ntype == "RELOCATION_TABLE":
		insertText = None
		if ntype == "root":
			# View file info
			insertText = "Target file: {}".format(self.pefile)
		else:
			insertText = self._getEntryText(ntype, text)
		
		fileInfoView = ViewMgr.getView("FileInfo")
		if fileInfoView:
			fileInfoView.insertText(insertText)
	
	def _getEntryText(self, ntype, value=""):
		if self.pefile is None:
			return ""
		
		peReader = PEMgr.getReader(self.pefile)
		
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
				strs.append("{}: {}\n".format(k, dllInfo[k]))
			text = "".join(strs)
		elif ntype == "IMPORT_TABLE_ENTRY2":
			funcInfo = peReader.getImportFunctionInfo(value)
			strs = list()
			for k in funcInfo.keys():
				strs.append("{}: {}\n".format(k, funcInfo[k]))
			text = "".join(strs)
		elif ntype == "RELOCATION_TABLE":
			text = ntype
		elif ntype == "RELOCATION_TABLE_ENTRY":
			text = ntype
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
