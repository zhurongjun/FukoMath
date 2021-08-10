#pragma once
#include "../fuko_math_forward.h"
#include <stdint.h>
#include <type_traits>
template<bool enable_assignment, typename base_type, typename target_type, uint32_t... sequence>
struct Swizzle;

// swizzle with assign  
template<typename base_type, typename target_type, uint32_t... sequence>
struct Swizzle<true, base_type, target_type, sequence...>
{
	using this_type = Swizzle < true, base_type, target_type, sequence...>;

	FORCEINLINE operator target_type() const noexcept
	{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[sizeof...(sequence)] = { self[sequence]... };
		return *reinterpret_cast<target_type*>(pad);
	}

	FORCEINLINE target_type operator=(target_type rhs) noexcept
	{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);

		assign(self, prhs, std::make_index_sequence<sizeof...(sequence)>());

		return *reinterpret_cast<target_type*>(this);
	}

	FORCEINLINE this_type& operator++()
	{
		increment(reinterpret_cast<base_type*>(this));
		return *this;
	}

	FORCEINLINE this_type& operator--()
	{
		decrement(reinterpret_cast<base_type*>(this));
		return *this;
	}

	FORCEINLINE target_type operator++(int)
	{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[sizeof...(sequence)] = { self[sequence]... };
		target_type old_val = *reinterpret_cast<target_type*>(pad);
		increment(reinterpret_cast<base_type*>(this));
		return old_val;
	}

	FORCEINLINE target_type operator--(int)
	{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[sizeof...(sequence)] = { self[sequence]... };
		target_type old_val = *reinterpret_cast<target_type*>(pad);
		decrement(reinterpret_cast<base_type*>(this));
		return old_val;
	}

private:
	template<size_t... indices>
	FORCEINLINE static void assign(base_type* self, base_type* rhs, std::index_sequence<indices...> seq) noexcept
	{
		base_type tmp[] = { self[sequence] = rhs[indices]... };
	}

	template<size_t... indices>
	FORCEINLINE static void increment(base_type* self) noexcept
	{
		base_type tmp[] = { ++self[sequence]... };
	}

	template<size_t... indices>
	FORCEINLINE static void decrement(base_type* self) noexcept
	{
		base_type tmp[] = { --self[sequence]... };
	}
};

// swizzle without assign 
template<typename base_type, typename target_type, uint32_t... sequence>
struct Swizzle<false, base_type, target_type, sequence...>
{
	using this_type = Swizzle < true, base_type, target_type, sequence...>;

	FORCEINLINE operator target_type() const noexcept
	{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[sizeof...(sequence)] = { self[sequence]... };
		return *reinterpret_cast<target_type*>(pad);
	}

private:
	template<size_t... indices>
	FORCEINLINE static void assign(base_type* self, base_type* rhs, std::index_sequence<indices...> seq) noexcept
	{
		base_type tmp[] = { self[sequence] = rhs[indices]... };
	}
};

// + - * / %
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator + (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) { return lsh + target_type(rsh); }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator + (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) { return target_type(lsh) + rsh; }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator - (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) { return lsh - target_type(rsh); }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator - (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) { return target_type(lsh) - rsh; }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator * (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) { return lsh * target_type(rsh); }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator * (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) { return target_type(lsh) * rsh; }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator / (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) { return lsh / target_type(rsh); }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator / (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) { return target_type(lsh) / rsh; }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator % (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) { return lsh % target_type(rsh); }
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> FORCEINLINE target_type operator % (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) { return target_type(lsh) % rsh; }

// += -= *= /= %=

// > < <= >= == != 

// + - sign 

// ! bool not 
