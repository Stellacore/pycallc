"""
Demonstrate call into C-library, ../src/libpycallc_clib.so
"""

import ctypes as ct

if "__main__" == __name__:

	teststat = 0  # be optimistic

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
	fdata = ct.c_float(2.)
	twobythree = pymultiply(ct.byref(fdata), 3)

	if not (6 == twobythree):
		print("ERROR: multiply: twobythree to be 6")
		teststat = 1
	else:
		print("py call to multiply okay")

	#
	# Example passing custom class (arg by reference, return by value)
	#

	# specify python class for which _fields_ member
	# must match CCustomType declaration below
	class CtCustomType(ct.Structure):
		_fields_ = [
		  ("anInt", ct.c_int)
		, ("anDouble", ct.c_double)
		, ("anSize", ct.c_size_t)
		, ("anArrayOf5Short", ct.c_short * 5)
		]

	# to specify this as return type
	pycopy = lib.copy
	pycopy.restype = ct.c_bool
	pycopy.argtypes = [ct.POINTER(CtCustomType), CtCustomType]

	# python data objects (using ctypes classes)
	sdata = (ct.c_short * 5)(1, 2, 3, 4, 5)
	source = CtCustomType(1, 1., 1, sdata)
	copy = CtCustomType()
	okay = pycopy(ct.byref(copy), source)
	if (okay):
		# simple test
		same = (
			   (source.anInt == copy.anInt)
			and (source.anDouble == copy.anDouble)
			and (source.anSize == copy.anSize)
			and (source.anArrayOf5Short[0] == copy.anArrayOf5Short[0])
			and (source.anArrayOf5Short[1] == copy.anArrayOf5Short[1])
			and (source.anArrayOf5Short[2] == copy.anArrayOf5Short[2])
			and (source.anArrayOf5Short[3] == copy.anArrayOf5Short[3])
			and (source.anArrayOf5Short[4] == copy.anArrayOf5Short[4])
			)
		if not same:
			print("ERROR: on copy contents")
			teststat = 1
			print(
				  "\ncopy.anInt", copy.anInt
				, "\ncopy.anDouble", copy.anDouble
				, "\ncopy.anSize", copy.anSize
				# Note this is a ctypes objects - for values ref below
				, "\ncopy.anArrayOf5Short", copy.anArrayOf5Short
				)
			# access array within CtCustomType
			for aShort in copy.anArrayOf5Short:
				print(aShort, end=" ")
			print()

		else:
			print("py call to copy okay")

	else:
		print("ERROR: on copy call (ptr argument null?)")
		teststat = 1

