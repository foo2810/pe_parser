import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog		# なぜかこれじゃないとfiledialogが使えない
from tkinter import messagebox 

from view.dir_tree import *
from view.file_info import *
from subsystem.view_mgr import ViewMgr
from subsystem.pe_mgr import PEMgr

from pe_parser.readpe import *
import logo_messages


# width=App.DEFAULT_WIDTH, height=App.DEFAULT_HEIGHT

# メインウィンドウに表示するtreeviewとfile_infoをPaneWindowで分割表示するようにする
class App(ttk.Frame):
	DEFAULT_WIDTH = 500
	DEFAULT_HEIGHT = 500
	def __init__(self):
		#self.pefile = ""
		self.pefileList = list()		# 複数ファイルの同時表示への対応
		
		super().__init__()
		self.viewInit()
		
		fInfoView = ViewMgr.getView("FileInfo")
		if fInfoView:
			fInfoView.insertFile("help.txt")

	def viewInit(self):
		self.title = "PE Viewer"
		
		self.configure(width=App.DEFAULT_WIDTH, height=App.DEFAULT_HEIGHT)
		
		self.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		self.columnconfigure(0, weight=2)
		self.columnconfigure(1, weight=2)
		self.rowconfigure(0, weight=1)
		
		self.master.columnconfigure(0, weight=1)
		self.master.rowconfigure(0, weight=1)
		
		self.master.title(self.title)
		self.menuInit()
		
		self.treeView = DirTreeView(self)
		self.fileInfoView = FileInfoView(self)
		self.treeView.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		self.fileInfoView.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
		
		ViewMgr.registerView(self.fileInfoView, "FileInfo")
		ViewMgr.registerView(self.treeView, "DirTree")
		
	def menuInit(self):
		self.menu = tk.Menu(self)
		
		self.fileMenu = tk.Menu(self.menu, tearoff=0)
		self.fileMenu.add_command(label="Open", command=self.openFileHandler)
		#self.fileMenu.add_command(label="Close", command=self.closeFileHandler(self.pefile))
		self.closeMenu = tk.Menu(self.fileMenu, tearoff=0)
		self.fileMenu.add_cascade(label="Close", menu=self.closeMenu)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", command=self.master.quit)
		self.menu.add_cascade(label="File", menu=self.fileMenu)
		
		self.editMenu = tk.Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Search", menu=self.editMenu)
		
		self.helpMenu = tk.Menu(self.menu, tearoff=0)
		self.helpMenu.add_command(label="Help", command=self.helpHandler)
		self.helpMenu.add_command(label="About me", command=self.aboutmeHandler)
		self.menu.add_cascade(label="Help", menu=self.helpMenu)
		
		self.master.config(menu=self.menu)
	
	def openFileHandler(self):
		types = [("EXE", "*.exe"), ("DLL", "*.dll"), ("All files", "*")]
		f = filedialog.askopenfilename(filetypes=types)
		
		if f != "":
			def _handler(sof):
				if sof:
					tView = ViewMgr.getView("DirTree")
					if not tView:
						messagebox.showinfo("Error", "Could not get view(DirTree)")
						return
					
					#self.pefile = f
					tView.setTree(f)
					
					# 複数ファイルの同時表示への対応
					self.pefileList.append(f)
					self.closeMenu.add_command(label=f, command=self.closeFileHandler(f))
			
			# pe_mgrサブシステムにファイルの追加が完了した後の処理をハンドラとして渡す
			PEMgr.addFileE(f, _handler)
			"""
			if not PEMgr.addFile(f):
				messagebox.showinfo("Error", "Failed to parse")
				return
			tView = ViewMgr.getView("DirTree")
			if not tView:
				messagebox.showinfo("Error", "Could not get view(DirTree)")
				return
			
			self.pefile = f
			tView.setTree(self.pefile)
			"""
	
	def closeFileHandler(self, fname):
		#self.tmp = fname
		def _handler():
			nonlocal fname
			"""
			if fname == "":
				return
			"""
			
			self.treeView.clearTree(fname)
			PEMgr.removeFile(fname)
			fInfoView = ViewMgr.getView("FileInfo")
			if fInfoView:
				fInfoView.insertFile("help.txt")
			#self.pefile = ""
			self.pefileList.remove(fname)
			self.closeMenu.delete(fname)
			
		return _handler
	
	def helpHandler(self):
		#messagebox.showinfo("Help", "Help")
		fInfoView = ViewMgr.getView("FileInfo")
		if fInfoView:
			fInfoView.insertFile("help.txt")
	
	def aboutmeHandler(self):
		messagebox.showinfo("About me", "PE Viewer\n\nCreated: 2019/3/18\nAuthor: hogedamari")
		"""
		fInfoView = ViewMgr.getView("FileInfo")
		if fInfoView:
			fInfoView.insertText("PE Viewer\n\nAuthor: hogedamari\nCreated: 2019/3/18\n")
		"""
		
	def run(self):
		self.mainloop()

if __name__ == "__main__":
	app = App()
	app.frame.mainloop()
		