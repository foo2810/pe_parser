import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext
import view.function as _F

class FileInfo(_F.Function):
	def __init__(self, master, fid):
		super().__init__(master, fid)
		self.frame = ttk.Frame(self.master.frame)
		self.init()
		self.cnt = 0
		
	def init(self):
		self.text = tkinter.scrolledtext.ScrolledText(self.frame)
		self.text.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
		self.frame.columnconfigure(0, weight=1)
		self.frame.rowconfigure(0, weight=1)
	
	def insertText(self, text):
		#self.text.insert(tk.INSERT, text)
		self.text.delete("1.0", tk.END)
		self.text.insert("1.0", "{}".format(text))
		self.cnt += 1
