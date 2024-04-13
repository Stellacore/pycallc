"""
Demonstrate call into C-library, ../src/libpycallc_clib.so
"""

import ctypes as ct

if "__main__" == __name__:

	# access the shared c-library
	lib = ct.CDLL("../src/libpycallc_clib.so")

	#
	# Simple example - with no arguments and no return value
	#

	# get python function and specify stack frame layout
	pyhello = lib.hello
	pyhello.restype = None
	pyhello.argtypes = None

	# call python function
	pyhello()

	#
	# Another example - with arguments and return value
	#

	# get function from the library
	pymultiply = lib.multiply
	pymultiply.restype = ct.c_double
	pymultiply.argtypes = [ct.POINTER(ct.c_float), ct.c_size_t]
	# that accepts pointer to data
	fdata = (ct.c_float * 1)(2.)  # and array (of one) floating point type
	twobythree = pymultiply(fdata, 3);
	print("twobythree:", twobythree)

	#
	# Example passing custom class (arg by reference, return by value)
	#

