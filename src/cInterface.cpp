
#include "pycallable.h"

// can use C++ inside this implementation
#include <iostream>
#include <limits>


// NOTE: Has C-interface
void
hello
	()
{
	// but (optionally) can use C++ inside implementation functions
	std::cout << "hello from c/c++ code\n";
}

// NOTE: Has C-interface
double
multiply
	( float * const ptFloat
	, int const anInt
	)
{
	// can CPP constructs - templates, language, etc...
	double result{ std::numeric_limits<double>::quiet_NaN() };
	if (ptFloat)
	{
		result = static_cast<double>(*ptFloat) * static_cast<double>(*ptFloat);
	}
	return result;
}

