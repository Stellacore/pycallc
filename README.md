# pycallc - Example Python call C/C++ (via ctypes)

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

The basic points are summarized in the following bullets. A detailed
description is provided in section
[Python Interface Code](#Python-Interface-Code)


* Python code should import ctypes module e.g.

	```
	import ctypes as ct
	```

* Access the C object code

	```
    lib = ct.CDLL("path/libname.so")
	```

* Then specify details about each function to be used. This includes

	* get python object for the function

	* specify the function result return type (using ctype python objects)

	* specify the function argument types (using ctype python objects)

### C/C++ Interface Code

The C/C++ header files should be expressed using only C-langugage standards
(which includes "#ifdef" logic which can contain non-C constructs).

Ref [example interface](./include/pycallable.h)

* Header files should be straight C - e.g. For compilation

	* Directly specified in native C code

	* From C++ environment by using external linkage
	  [extern "C"](https://en.cppreference.com/w/cpp/language/language_linkage)

	* Use only types and keywords available in C

* Use #ifdefs to make header compatible with both C and C++, i.e.

	```
	#ifdef __cplusplus
    extern "C"
    {
	#endif

	// ... Header declarations using only C langague types!

	#ifdef __cplusplus
    } // extern "C"
	#endif
	```

### C/C++ Implementation Code

Function interfaces must be pure C code, but internal implementation
can freely use C++ (e.g. construct classes, call other C++ code, etc).

Ref [example implementation](./src/cInterface.cpp)

For linking

* Compile as position independent code (e.g. -fPIC for gcc)
  Ref compiler options in [top level CMakeLists.txt](./CMakeLists.txt#L62)
  in the BUILD_FLAGS_FOR_GCC variable.

* Organize object code into a shared library (e.g. -shared for gcc)
  Ref library options in [src/CMakeLists.txt](./src/CMakeLists.txt#L37)
  which uses the cmake 'SHARED' keyword to build the library.

### Python Interface Code

Use the ctypes python module to describe the stack frame associated with
the C function interfaces.

Ref [example python code](./test/test_pycallc.py)

* Construct a python object that represents the shared library. E.g.,

	```
    import ctypes as ct
    lib = ct.CDLL("path/libname.so")
	```

* Construct a python object for (each/any) function to be called. E.g.,

	```
    pyfunc = lib.func
	```

* Call the python function and use the results as is normal from within python.
	```
   	resval = pyfunc(args)
	print("resval:", resval)
	```

#### Example with Custom Struct and Array

* Use the python function object to specify the C-style stack frame
  layout for the (each) particular function. In particular
  (cf. callsum.py, sum.c for this specific example).

	* Specify the return type using the c_... types provided by ctype. E.g.,

		```
		pyfunc.restype = ct.c_double  # or whatever type (use 'None' for void)
		```

	* Specify the agument types as a python list. E.g.,

		```
		pyfunc.argtypes = [ct.POINTER(ct.c_float), ct.c_size_t]
		```


* Ref the compilable/running [Example code](./test/test_pycallc.py)

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

	
## Project Build and Test

This project can be built using [CMake](ihttps://cmake.org/). E.g.,

	```
	$ cd /tmp
	$ git clone https://github.com/Stellacore/pycallc.git
	$ mkdir /tmp/tmpbuild # or anywhere
	$ cd /tmp/tmpbuild
		&& cmake -DCMAKE_BUILD_TYPE=Release /tmp/pycallc/
		&& cmake --build . --target all -j `nproc`
		&& ctest
	```

The shared library is located in
	```
	/tmp/tmpbuild/src/libpycallc_clib.so
	```

To run the python script directly from the build directory (which
contains the

	```
	$ cd /tmp/tmpbuild/test
		&& bash -c \
			"/usr/bin/python3 /tmp/tmpbuild/pycallc/test/test_pycallc.py"
	```

