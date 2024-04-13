
#include "pycallable.h"

// can use C++ inside this implementation
#include <iostream>

// NOTE: Has C-interface
void
hello
	()
{
	// but (optionally) can use C++ inside implementation functions
	std::cout << "hello from c/c++ code\n";
}


