import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog		# なぜかこれじゃないとfiledialogが使えない
from tkinter import messagebox 

import view.function as _F
from view.dir_tree import *
from view.file_info import *

from pe_parser.readpe import *

class PEInfo(_F.Function):
	def __init__(self):
		super().__init__("independet", "PEInfo")
		self.peReader = None
		self.peFile = None
		self.isClear = True
	
	def setFile(self, pefile):		
		self.peFile = pefile
		self.peReader = PEReader(self.peFile)
	
	def closeFile(self):
		if self.peReader is None:
			return
		
		self.peFile = None
		self.peReader = None
		
		dirTreehandle = _F.getFuncHandle("DirTree")
		if not dirTreehandle:
			print(" >>> Handle not found")
			return
		
		dirTreehandle.clearTree()
		self.isClear = True
	
	def applyInfo(self):
		dirTreehandle = _F.getFuncHandle("DirTree")
		if not dirTreehandle:
			return
		
		if self.isClear:
			dirTreehandle.setTree()
		else:
			dirTreehandle.resetTree()
		
		self.isClear = False

class App(_F.Function):
	DEFAULT_WIDTH = 500
	DEFAULT_HEIGHT = 500
	def __init__(self):
		super().__init__("root", "root")
		self.sysInit()
		self.viewInit()
		self.peInfo.applyInfo()
	
	def sysInit(self):
		pefile = "C:\\Windows\\System32\\kernel32.dll"
		#pefile = "C:\\Windows\\SysWow64\\kernel32.dll"
		self.peInfo = PEInfo()
		self.peInfo.setFile(pefile)

	def viewInit(self):
		self.frame = ttk.Frame(width=App.DEFAULT_WIDTH, height=App.DEFAULT_HEIGHT)
		
		self.frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		self.frame.columnconfigure(0, weight=2)
		self.frame.columnconfigure(1, weight=2)
		self.frame.rowconfigure(0, weight=1)
		
		self.frame.master.columnconfigure(0, weight=1)
		self.frame.master.rowconfigure(0, weight=1)
		
		self.frame.master.title("Title")
		self.menuInit()
		
		self.treeView = DirTree(self, "DirTree")
		self.fileInfoView = FileInfo(self, "FileInfo")
		self.treeView.frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		self.fileInfoView.frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
		
	def menuInit(self):
		self.menu = tk.Menu(self.frame)
		
		self.fileMenu = tk.Menu(self.menu, tearoff=0)
		self.fileMenu.add_command(label="Open", command=self.selectFileHandler)
		self.fileMenu.add_command(label="Close", command=self.closeFileHandler)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=self.frame.master.quit)
		self.menu.add_cascade(label="File", menu=self.fileMenu)
		
		self.editMenu = tk.Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Search", menu=self.editMenu)
		
		self.helpMenu = tk.Menu(self.menu, tearoff=0)
		self.helpMenu.add_command(label="Help", command=self.helpHandler)
		self.helpMenu.add_command(label="About me", command=self.aboutmeHandler)
		self.menu.add_cascade(label="Help", menu=self.helpMenu)
		
		self.frame.master.config(menu=self.menu)
	
	def selectFileHandler(self):
		types = [("EXE", "*.exe"), ("DLL", "*.dll"), ("All files", "*")]
		f = filedialog.askopenfilename(filetypes=types)
		
		if f != "":
			self.peInfo.setFile(f)
			self.peInfo.applyInfo()
	
	def closeFileHandler(self):
		self.peInfo.closeFile()
	
	def helpHandler(self):
		messagebox.showinfo("Help", "Help")
	
	def aboutmeHandler(self):
		messagebox.showinfo("About me", "PE Viewer\n\nCreated: 2019/3/18\nAuthor: hogedamari")
		
	def run(self):
		self.frame.mainloop()

if __name__ == "__main__":
	app = App()
	app.frame.mainloop()
		