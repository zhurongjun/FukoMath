#pragma once

// per compiler define 
#if defined(__clang__) || defined(__GNUG__)

	#define FORCEINLINE inline __attribute__((always_inline))

#elif defined(_MSC_VER)

	#define FORCEINLINE __forceinline

#else

    #error Unrecognized compiler

#endif

// TODO. simd define 

// TODO. disable warning 

namespace {math_namespace}
{{
// type alias 
using uint = unsigned int;

// forward declares 
{forward_declares}
}}
