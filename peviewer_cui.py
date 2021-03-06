# Main

import os
import sys
from pathlib import Path
from pe_parser.parse_pe import *
#from pe_parser.loadPE import *


def main():
	args = sys.argv
	argc = len(args)
	if argc < 2:
		print("Usage: %s <file> [<options>]\n" % args[0])
		print("[Option]")
		print("h: Show header Info")
		print("l: Map file and dump the data")
		print("I: Show import table")
		print("E: Show export table")
		print("R: Show relocation table")
		print("a: Do everything")
		print("t: For debug (Nothing)")
		print("")
		exit(1)
	elif argc == 2:
		option = "h"
	else:
		option = args[2]
		
	filename = args[1]
	path = Path(filename)
	if not path.exists():
		print("Error: FileNotFound")
		exit(1)
		
	print(path.name + "\n")
	
	peReader = PEParser(str(path))
	peReader.parse()
	
	## Reader
	if "h" in option or "a" in option:		
		peReader.printAll()
	
	"""
	dumpFile = Path("./dump.bin")
	dump = b""
	if dumpFile.exists():
		st = dumpFile.open("rb")
		dump = st.read()
		st.close()
	else:
		print("Error: dump.bin dose not exists")
		sys.exit(1)
	"""
	
	## ImportTable
	if "I" in option or "a" in option:
		peReader.dumpImportTable(flg=1)
	
	if "E" in option or "a" in option:
		peReader.dumpExportTable()
	
	## RelocationTable
	if "R" in option or "a" in option:
		peReader.dumpRelocationTable()
		
	## [Test] ExportTable
	if "t" in option:
		pass
	
	
if __name__ == "__main__":
	main()
