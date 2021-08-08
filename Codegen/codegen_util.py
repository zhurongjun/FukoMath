define_combine_marco = '''
#ifndef SWIZZLE_COMBINE
    #define SWIZZLE_COMBINE(a, b) _SWIZZLE_COMBINE(a, b)
    #define _SWIZZLE_COMBINE(a, b) a##b
#endif
'''

undefine_combine_marco = '''
#ifdef SWIZZLE_COMBINE
	#undef SWIZZLE_COMBINE
#endif
#ifdef _SWIZZLE_COMBINE
	#undef _SWIZZLE_COMBINE
#endif
'''

swizzle_type_marco = "SWIZZLE_BASE_TYPE"
swizzle_combine_marco = "SWIZZLE_COMBINE"

math_swizzle_pad = ['x', 'y', 'z', 'w']
color_swizzle_pad = ['r', 'g', 'b', 'a']

swizzle_template = '''#pragma once
#include <stdint.h>
#include <type_traits>
template<bool enable_assignment, typename base_type, typename target_type, uint32_t... sequence>
struct Swizzle;

template<typename base_type, typename target_type, uint32_t... sequence>
struct Swizzle<true, base_type, target_type, sequence...>
{
	__forceinline operator target_type() const noexcept
	{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[sizeof...(sequence)] = { self[sequence]... };
		return *reinterpret_cast<target_type*>(pad);
	}

	__forceinline target_type operator=(target_type rhs) noexcept
	{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);

		assign(self, prhs, std::make_index_sequence<sizeof...(sequence)>());

		return *reinterpret_cast<target_type*>(this);
	}

private:
	template<size_t... indices>
	__forceinline void assign(base_type* self, base_type* rhs, std::index_sequence<indices...> seq) noexcept
	{
		base_type tmp[] = { self[sequence] = rhs[indices]... };
	}
};
template<typename base_type, typename target_type, uint32_t... sequence>
struct Swizzle<false, base_type, target_type, sequence...>
{
	__forceinline operator target_type() const noexcept
	{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[sizeof...(sequence)] = { self[sequence]... };
		return *reinterpret_cast<target_type*>(pad);
	}

private:
	template<size_t... indices>
	__forceinline void assign(base_type* self, base_type* rhs, std::index_sequence<indices...> seq) noexcept
	{
		base_type tmp[] = { self[sequence] = rhs[indices]... };
	}
};
'''