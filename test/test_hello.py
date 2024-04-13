"""
Demonstrate call into C-library, ../src/libpycallc_clib.so
"""

import ctypes as ct

if "__main__" == __name__:

	# access the shared c-library
	lib = ct.CDLL("../src/libpycallc_clib.so")

	# get python function and specify stack frame layout
	pyhello = lib.hello
	pyhello.restype = None
	pyhello.argtypes = None

	# call python function
	pyhello()

