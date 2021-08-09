#pragma once

// per compiler define 
#if defined(__clang__) || defined(__GNUG__)

	#define FORCEINLINE inline __attribute__((always_inline))

#elif defined(_MSC_VER)

	#define FORCEINLINE __forceinline

#else

    #error Unrecognized compiler

#endif

// forward declares 
{forward_declares}
// TODO. simd define 

// TODO. disable warning 
