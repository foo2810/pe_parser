# PE Parser

##########################################################################
# c.f.                                                                   #
# https://en.wikibooks.org/wiki/X86_Disassembly/Windows_Executable_Files #
# http://hp.vector.co.jp/authors/VA050396/tech_06.html                   #
#                                                                        #
##########################################################################

# -*- coding: utf-8 -*-

import os
import sys
from array import array
from mmap import *

from pe_parser._peHeader import *
from pe_parser._importTable import *
from pe_parser._exportTable import *
from pe_parser._relocationTable import *
from pe_parser._binary import *


class PEParser:
	def __init__(self, pefile):
		self.mapData = None
		self.bData = None
		self.peHeader = None
		with open(pefile, "rb") as st:
			self.bData = st.read()
		
		self.importTable = None
		self.exportTable = None
		self.relocationTable = None
		
		self.filename = os.path.abspath(pefile)
	
	def __del__(self):
		if self.mapData is not None:
			self.mapData.close()
	
	def parse(self):
		try:
			self.peHeader = PEHeader(self.bData)
			self.__loadToMemory(False)
		except (ROMImage, UnknownMagic) as e:
			sys.stderr.write("{}\n".format(e))
			return False
		except (BaseException, Exception) as e:
			sys.stderr.write("{}\n".format(e))
			return False
			
		return True
	
	def getMSDosHeader(self):
		return self.peHeader.msDosHeader
		
	def getNTHeader(self):
		return self.peHeader.ntHeader
		
	def getFileHeader(self):
		return self.peHeader.fileHeader
	
	def getOptionalHeader(self):
		return self.peHeader.optionalHeader
	
	def getDataDirectory(self):
		return self.peHeader.dataDirectory
	
	def getSectionTable(self):
		return self.peHeader.sectionTable
		
	def getImportTable(self):
		if self.importTable is not None:
			return self.importTable
	
		importTableVRva = self.peHeader.optionalHeader.DataDirectory[1].VirtualAddress
		importTableSize = self.peHeader.optionalHeader.DataDirectory[1].Size
		if self.peHeader.optionalHeader.Magic == b"\x0b\x01":
			magic = 32
		elif self.peHeader.optionalHeader.Magic == b"\x0b\x02":
			magic = 64
		else:
			raise ROMImage("in dumpImportTable")
			
		self.importTable = ImportTable(self.mapData, importTableVRva, importTableSize, magic)
		return self.importTable
	
	def getExportTable(self):
		if self.exportTable is not None:
			return self.exportTable
		
		exportTableVRva = self.peHeader.optionalHeader.DataDirectory[0].VirtualAddress
		exportTableSize = self.peHeader.optionalHeader.DataDirectory[0].Size
		self.exportTable = ExportTable(self.mapData, exportTableVRva, exportTableSize)
		
		return self.exportTable
	
	def getRelocationTable(self):
		if self.relocationTable is not None:
			return self.relocationTable
		
		relocationTableVRva = self.peHeader.optionalHeader.DataDirectory[5].VirtualAddress
		relocationTableSize = self.peHeader.optionalHeader.DataDirectory[5].Size
		self.relocationTable = RelocationTable(self.mapData, relocationTableVRva, relocationTableSize)
		
		return self.relocationTable
		
	def dumpImportTable(self, flg=1):
		self.importTable = self.getImportTable()
		self.importTable.printAll(flg)
	
	def dumpExportTable(self):
		self.exportTable = self.getExportTable()
		self.exportTable.printAll()
	
	def dumpRelocationTable(self):
		self.relocationTable = self.getRelocationTable()
		self.relocationTable.printAll()
	
	def __loadToMemory(self, printOn=False):
		alignment = self.peHeader.ntHeader.OptionalHeader.SectionAlignment
		baseAddr = self.peHeader.ntHeader.OptionalHeader.ImageBase
		mapSize = self.peHeader.ntHeader.OptionalHeader.SizeOfImage
		#entryPoint = self.peHeader.ntHeader.OptionalHeader.AddressOfEntryPoint
		
		if printOn:
			print("[Caution] loadToMemory is not COMPLETED!!!!!!!!!!\n")
			print("[LOAD PE FORMAT FILE]")
			print("BaseAddress: ", hex(baseAddr))
			print("Alignment: ", hex(alignment))
			#print("EntryPoint: ", hex(entryPoint))
		
		
		self.mapData = mmap(-1, mapSize, None, ACCESS_WRITE)
		
		if printOn:
			print("[Sections]")
		for section in self.peHeader.sectionTable:
			if not section.isAlloced:
				continue
			
			name = section.name
			vRva = section.VirtualAddress
			size = section.SizeOfRawData
			
			if printOn:
				print("\tName: ", name)
				print("\tSize: ", hex(size))
				print("\tVirtualAddress(RVA): ", hex(vRva))
			
			
			# Padding (alignment)
			"""
			if self.mapData.tell() % alignment != 0:
				cnt = alignment - (self.mapData.tell() % alignment)
				for i in range(cnt):
					self.mapData.write_byte(0)
			"""
			
			curPosB = self.mapData.tell()
			if vRva > curPosB:
				self.mapData.write(b"\x00" * (vRva - curPosB))
			
			if printOn:
				curPosA = self.mapData.tell()
				print("\tHead Position of MemoryMap: ", hex(curPosA))
			
			rawData = section.getRawData()
			res = self.mapData.write(rawData)
			self.mapData.flush()
			
			if printOn:
				print("\tRes from write(): ", hex(res))
				print("")
		
		#self.isLoaded = True
		self.mapData.seek(0)
	
	def dump(self, output="dump.bin"):
		dumpData = self.mapData.read()
		self.mapData.seek(0)
			
		if output != "":
			st = open(output, "wb")
			
			st.write(dumpData)
			st.flush()
			st.close()
		
		return dumpData
	
	def printAll(self):
		self.peHeader.printAll()

