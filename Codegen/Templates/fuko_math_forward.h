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

template<typename T>
FORCEINLINE T _mod(T a, T b)
{{
	if constexpr (std::is_same_v<T, float> || std::is_same_v<T, double>)
	{{
		return std::fmod(a, b);
	}}
	else
	{{
		return a % b;
	}}
}}

template<typename T>
struct is_swizzle;

template<typename T>
struct is_swizzle
{{
	static constexpr bool value = false;
}};

template<typename T>
static constexpr bool is_swizzle_v = is_swizzle<T>::value;

// forward declares 
{forward_declares}
}}
