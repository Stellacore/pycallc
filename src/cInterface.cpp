
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
		result = static_cast<double>(*ptFloat) * static_cast<double>(anInt);
	}
	return result;
}

// NOTE: Has C-interface
bool
copy
	( struct CCustomType * const ptInto
	, struct CCustomType const from
	)
{
	bool okay{ false };
	if (ptInto)
	{
		ptInto->anInt = from.anInt;
		ptInto->anDouble = from.anDouble;
		ptInto->anSize = from.anSize;
		for (size_t nn{0u} ; nn < 5u ; ++nn)
		{
			ptInto->anArrayOf5Short[nn] = from.anArrayOf5Short[nn];
		}
		okay = true;
	}
	return okay;
}

