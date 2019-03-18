import os

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext

from subsystem.view_mgr import ViewMgr
from subsystem.pe_mgr import PEMgr


class FileInfoView(ttk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.init()
		
	def init(self):
		self.text = tkinter.scrolledtext.ScrolledText(self)
		self.text.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
	
	def insertText(self, text):
		#self.text.insert(tk.INSERT, text)
		self.text.configure(state=tk.NORMAL)
		self.text.delete("1.0", tk.END)
		self.text.insert("1.0", "{}".format(text))
		self.text.configure(state=tk.DISABLED)
	
	def insertFile(self, fname):
		if os.path.exists(fname):
			lines = None
			with open(fname) as st:
				lines = st.readlines()
			
			self.text.configure(state=tk.NORMAL)
			self.text.delete("1.0", tk.END)
			
			for i in range(len(lines)):
				pos = "{}.0".format(i+1)
				self.text.insert(pos, lines[i])
			
			self.text.configure(state=tk.DISABLED)
			
			return True
			
		else:
			return False
			
