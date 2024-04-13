
#ifndef pycallc_pycallable_INCL_
#define pycallc_pycallable_INCL_

// NOTE use of only C-lang headers here
#include <stddef.h>
#include <stdint.h>


#ifdef __cplusplus
	extern "C"
	{
#endif

//! print simple hello message
void
hello
	();

//! Example of simple argument passing
double
multiply
	( float * const ptFloat
	, int const anInt
	);

//! Custom structure with spattering of types for example
struct CCustomType
{
	int anInt;
	double anDouble;
	size_t anSize;
	short anArrayOf5Short[5];
};

//! Add corresponding elements of each arg (one by ref, one by value)
bool
copy
	( struct CCustomType * const ptInto
	, struct CCustomType const from
	);



#ifdef __cplusplus
	}
#endif

#endif // pycallc_pycallable_INCL_

