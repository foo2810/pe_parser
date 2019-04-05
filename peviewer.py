from system import *

if __name__ == "__main__":
	try:
		sys = System()
		sys.init()
		sys.run()
		sys.fin()
	except KeyboardInterrupt:
		sys.fin()
