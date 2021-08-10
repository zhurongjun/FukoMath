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

// constant 
const float PI = 3.1415926535897932384626433832795028841971f;

// floating mod 
// See http://http.developer.nvidia.com/Cg/fmod.html for reference
// This implementation does not follow the reference
// float2 c = frac(abs(a/b))*abs(b);
// return (a < 0) ? -c : c; 
template<typename T>
FORCEINLINE T _floating_mod(T a, T b)
{{
	T adb = a / b;
	T abs_adb = adb > 0 ? adb : - adb;
	T abs_b = b > 0 ? b : -b;
	T frac_abs_adb = abs_adb - static_cast<int>(abs_adb);
	T c = frac_abs_adb * abs_b;
	return a < 0 ? -c : c;
}}

// forward declares 
{forward_declares}
}}
