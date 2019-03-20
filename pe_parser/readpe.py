# PE Reader

from pe_parser.parse_pe import *

class PEReader:
	def __init__(self, pefile):
		self.filename = os.path.abspath(pefile)
		
		if not os.path.exists(pefile):
			raise FileNotFoundError
		
		self.parser = PEParser(pefile)
	
	def parse(self):
		if self.parser.parse():
			return True
		else:
			return False
	
	## MSDOS Header
	
	def getMSDosHeader(self):
		msdosHeader = self.parser.getMSDosHeader()
		
		d = {
			"e_magic": msdosHeader.e_magic,
			"e_cblp": msdosHeader.e_cblp,
			"e_cp": msdosHeader.e_cp,
			"e_crlc": msdosHeader.e_crlc,
			"e_cparhdr": msdosHeader.e_cparhdr,
			"e_minalloc": msdosHeader.e_minalloc,
			"e_ss": msdosHeader.e_ss,
			"e_sp": msdosHeader.e_sp,
			"e_csum": msdosHeader.e_csum,
			"e_ip": msdosHeader.e_ip,
			"e_cs": msdosHeader.e_cs,
			"e_lfarlc": msdosHeader.e_lfarlc,
			"e_ovno": msdosHeader.e_ovno,
			"e_res": msdosHeader.e_res,
			"e_oemid": msdosHeader.e_oemid,
			"e_oeminfo": msdosHeader.e_oeminfo,
			"e_res2": msdosHeader.e_res2,
			"e_lfanew": msdosHeader.e_lfanew,
		}
		
		return d
	
	## NT Header
	
	def getNTHeader(self):
		ntHeader = self.parser.getNTHeader()
		d = {
			"Signature": ntHeader.Signature,
		}
		
		return d
	
	## File Header
	
	def getFileHeader(self):
		fileHeader = self.parser.getFileHeader()
		
		d = {
			"Machine": fileHeader.Machine,
			"NumberOfSections": fileHeader.NumberOfSections,
			"TimeDataStamp": fileHeader.TimeDataStamp,
			"PointerToSymbolTable": fileHeader.PointerToSymbolTable,
			"NumberOfSymbols": fileHeader.NumberOfSymbols,
			"SizeOfOptionalHeader": fileHeader.SizeOfOptionalHeader,
			"Characteristics": hex(fileHeader.Characteristics),
		}
		
		return d
		
	## Optional Header
	
	def getOptionalHeader(self):
		optHeader = self.parser.getOptionalHeader()
		
		d = {
			"Magic": optHeader.Magic, 
			"MajorLinkerVersion": optHeader.MajorLinkerVersion,
			"MinorLinkerVersion": optHeader.MinorLinkerVersion,
			"SizeOfCode": optHeader.SizeOfCode,
			"SizeOfInitializedData": optHeader.SizeOfInitializedData,
			"SizeOfUninitializedData": optHeader.SizeOfUninitializedData,
			"AddressOfEntryPoint": optHeader.AddressOfEntryPoint,
			"BaseOfCode": optHeader.BaseOfCode,
			"BaseOfData": optHeader.BaseOfData,
			
			"ImageBase": optHeader.ImageBase, 
			"SectionAlignment": optHeader.SectionAlignment,
			"FileAlignment": optHeader.FileAlignment,
			"MajorOperatingSystemVersion": optHeader.MajorOperatingSystemVersion,
			"MinorOperatingSystemVersion": optHeader.MinorOperatingSystemVersion,
			"MajorImageVersion": optHeader.MajorImageVersion,
			"MinorImageVersion": optHeader.MinorImageVersion,
			"MajorSubsystemVersion": optHeader.MajorSubsystemVersion,
			"MinorSubsystemVersion": optHeader.MinorSubsystemVersion,
			"Win32VersionValue": optHeader.Win32VersionValue,
			"SizeOfImage": optHeader.SizeOfImage,
			"SizeOfHeaders": optHeader.SizeOfHeaders,
			"CheckSum": optHeader.CheckSum,
			"Subsystem": optHeader.Subsystem,
			"DllCharacteristics": optHeader.DllCharacteristics,
			"SizeOfStackReserve": optHeader.SizeOfStackReserve,
			"SizeOfStackCommit": optHeader.SizeOfStackCommit,
			"SizeOfHeapReserve": optHeader.SizeOfHeapReserve,
			"SizeOfHeapCommit": optHeader.SizeOfHeapCommit,
			"LoaderFlags": optHeader.LoaderFlags,
			"NumberOfRvaAndSizes": optHeader.NumberOfRvaAndSizes,
			"DataDirectory": "DATADIRECTORY_DUMMY",
		}
		
		return d
	
	## About Section Table
	
	def getSectionList(self):
		sectionTable = self.parser.getSectionTable()
		return list(map(lambda x: x.name, sectionTable))
	
	def getSectionHeader(self, sname):
		sectionTable = self.parser.getSectionTable()
		for s in sectionTable:
			if s.name.lower() == sname.lower():
				sHeader = dict()
				sHeader["Name"] = s.name
				sHeader["Misc"] = s.Misc
				sHeader["VirtualAddress"] = s.VirtualAddress
				sHeader["SizeOfRawData"] = s.SizeOfRawData
				sHeader["PointerToRawData"] = s.PointerToRawData
				sHeader["PointerToRelocations"] = s.PointerToRelocations
				sHeader["PointerToLinenumbers"] = s.PointerToLinenumbers
				sHeader["NumberOfRelocations"] = s.NumberOfRelocations
				sHeader["NumberOfLinenumbers"] = s.NumberOfLinenumbers
				sHeader["Characteristics"] = s.Characteristics
				return sHeader
	
	## About Import Table
	
	def getImportFunctionList(self, dllName):
		importTable = self.parser.getImportTable()
		for i in importTable:
			if i.Name.lower() == dllName.lower():
				return list(map(lambda x: x.AddressOfData.Name, i))
		
		return None
					
	
	def getImportDllList(self):
		importTable = self.parser.getImportTable()
		return list(map(lambda x: x.Name, importTable))
	
	def getImportDllInfo(self, dllName):
		importTable = self.parser.getImportTable()
		for i in importTable:
			if i.Name.lower() == dllName.lower():
				dllInfo = dict()
				dllInfo["Union"] = i.Union
				dllInfo["TimeDataStamp"] = i.TimeDataStamp
				dllInfo["ForwarderChain"] = i.ForwarderChain
				dllInfo["NameRVA"] = i.nameRVA
				dllInfo["Name"] = i.Name
				dllInfo["NumberOfEntry"] = i.numberOfEntry
				return dllInfo
		
		return None
	
	def getImportFunctionInfo(self, func, dllName=None):
		importTable = self.parser.getImportTable()
		for i in importTable:
			if dllName is not None:
				if i.Name.lower() != dllName.lower():
					continue
			for f in i:
				if f.AddressOfData.Name.lower() == func.lower():
					fInfo = dict()
					fInfo["Name"] = f.AddressOfData.Name
					fInfo["Rva"] = byteToIntLE(f.Union)
					return fInfo
		return None
	
	
	## About Export Table
	
	def getExportFuncNameList(self):
		exportTable = self.parser.getExportTable()
		
		return list(map(lambda x: x[1], exportTable))

	def getExportFuncAddr(self, funcName):
		exportTable = self.parser.getExportTable()
		
		for o, n in exportTable:
			if funcName.lower() == n.lower():
				return exportTable.exportAddressTable[o]
		return None
	
	def isExported(self, func):
		exportTable = self.parser.getExportTable()
		return exportTable.isExported(self.getExportFuncAddr(func))
	
	# エクスポートされた関数のvrvaを渡す
	def getExportName(self, addr):
		exportTable = self.parser.getExportTable()
		return exportTable.getExportName(addr)
	
	## About Relocation Table
	
	def getBaseRelocationList(self):
		pass
	
	def getRelocationEntryList(self, base):
		pass
	
	def getRelocationInfo(self, base, ord):
		pass
	