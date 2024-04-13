# pycallc - Example Python calling C/C++ code (with ctypes)

## Basic Concept

The ctypes module is part of python proper and therefore available on
all python distributions. From
[Python documention](https://docs.python.org/3/library/ctypes.html)

	"ctypes is a foreign function library for Python. It provides
	C compatible data types, and allows calling functions in DLLs
	or shared libraries. It can be used to wrap these libraries in
	pure Python."

Notes:

* Code in this repo is compatible with python3.

* Code in this repo is compatible with linux environment.

* The C-code to be called must be in a sharable object/library
  (e.g. .so on linux)

Basic concepts are outlined in the following.

### Python Application Code

* Python code should import ctypes module e.g.

	import ctypes as ct

* Access the C object code

    lib = ct.CDLL("path/libname.so")

* Call functions per [Python Interface Code](#Python-Interface-Code)
  section below.

### C/C++ Interface Code

* Header files should be straight C - e.g. For compilation

	* Directly specified in native C code

	* From C++ environment by using external linkage
	  [extern "C"](https://en.cppreference.com/w/cpp/language/language_linkage)

	* Use only types and keywords available in C

* Use #ifdefs to make header compatible with both C and C++, i.e.

	#ifdef __cplusplus
    extern "C"
    {
	#endif

	... Header declarations using only C langague types!

	#ifdef __cplusplus
    } // extern "C"
	#endif

### C/C++ Implementation Code

* Function interfaces must be pure C code, but internal implementation
  can freely use C++ (e.g. construct classes, call other C++ code, etc)

* For linking

	* Compile as position independent code (e.g. -fPIC for gcc)

	* Organize object code into a shared library (e.g. -shared for gcc)

### Python Interface Code

Use the ctypes python module to describe the stack frame associated with
the C function interfaces.

* Construct a python object that represents the shared library. E.g.,

    import ctypes as ct
    lib = ct.CDLL("path/libname.so")

* Construct a python object for (each/any) function to be called. E.g.,

    pyfunc = lib.func

* Call the python function and use the results as is normal from within python.

   	resval = pyfunc(args)
	print("resval:", resval)

#### Example with Custom Struct and Array

* Use the python function object to specify the C-style stack frame
  layout for the (each) particular function. In particular
  (cf. callsum.py, sum.c for this specific example).

	* Specify the return type using the c_... types provided by ctype. E.g.,

    	pyfunc.restype = ct.c_double  # or whatever type (use 'None' for void)

	* Specify the agument types as a python list. E.g.,

    	pyfunc.argtypes = [ct.POINTER(ct.c_float), ct.c_size_t]


* Ref ./test/test_pycallc.py

* Note there are
  [many ctypes](https://docs.python.org/3/library/ctypes.html#fundamental-data-types). These may be used individualy as illustrated above to describe
  simple interfaces. Alternatively, python inheritance from ctype's python
  'Structure' type can be used to describe custome data types. E.g.,

	* In Python (Note the requirement of populating the \_fields\_ member
	  with a list of named ctype types. E.g.,

		```
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

		# invoke c function from python
		okay = pycopy(ct.byref(copy), source)
		```

	* In C or within extern "C"{} header section

		```
		// declare the custom type (must match CtCustomType._fields_ spec)
		struct CCustomType
		{
			int anInt;
			double anDouble;
			size_t anSize;
			short anArrayOf5Short[5];
		};

		// Declare the custom return type
		bool
		copy
			( struct CCustomType * const ptInto
			, struct CCustomType const from
			);
		```

