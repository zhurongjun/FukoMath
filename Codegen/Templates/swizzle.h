#pragma once
#include "../fuko_math_forward.h"
#include <stdint.h>

namespace {math_namespace}
{{
template<bool enable_assignment, typename base_type, typename target_type, uint32_t x> struct Swizzle1;
template<bool enable_assignment, typename base_type, typename target_type, uint32_t x, uint32_t y> struct Swizzle2;
template<bool enable_assignment, typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z> struct Swizzle3;
template<bool enable_assignment, typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z, uint32_t w> struct Swizzle4;

// swizzle1 with assign  
template<typename base_type, typename target_type, uint32_t x>
struct Swizzle1<true, base_type, target_type, x>
{{
	using this_type = Swizzle1<true, base_type, target_type, x>;

	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} this_type& operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		return *this;
	}}

	{inline_marco} this_type& operator++()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		++self[x];
		return *this;
	}}

	{inline_marco} this_type& operator--()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		--self[x];
		return *this;
	}}

	{inline_marco} target_type operator++(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x] }};
		++self[x];
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator--(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x] }};
		--self[x];
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

// swizzle1 without assign 
template<typename base_type, typename target_type, uint32_t x>
struct Swizzle1<false, base_type, target_type, x>
{{
	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

// swizzle2 with assign  
template<typename base_type, typename target_type, uint32_t x, uint32_t y>
struct Swizzle2<true, base_type, target_type, x, y>
{{
	using this_type = Swizzle2<true, base_type, target_type, x, y>;

	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} this_type& operator=(base_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		self[x] = rhs;
		self[y] = rhs;
		return *this;
	}}
	
	{inline_marco} this_type& operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		self[y] = prhs[0];
		return *this;
	}}

	{inline_marco} this_type& operator++()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		++self[x];
		++self[y];
		return *this;
	}}

	{inline_marco} this_type& operator--()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		--self[x];
		--self[y];
		return *this;
	}}

	{inline_marco} target_type operator++(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x], self[y] }};
		++self[x];
		++self[y];
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator--(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x], self[y] }};
		--self[x];
		--self[y];
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x], -self[y] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

// swizzle2 without assign 
template<typename base_type, typename target_type, uint32_t x, uint32_t y>
struct Swizzle2<false, base_type, target_type, x, y>
{{
	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x], -self[y] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

// swizzle3 with assign  
template<typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z>
struct Swizzle3<true, base_type, target_type, x, y, z>
{{
	using this_type = Swizzle3<true, base_type, target_type, x, y, z>;

	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} this_type& operator=(base_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		self[x] = rhs;
		self[y] = rhs;
		self[z] = rhs;
		return *this;
	}}
	
	{inline_marco} this_type& operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		self[y] = prhs[0];
		self[z] = prhs[0];
		return *this;
	}}
	
	{inline_marco} this_type& operator++()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		++self[x];
		++self[y];
		++self[z];
		return *this;
	}}

	{inline_marco} this_type& operator--()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		--self[x];
		--self[y];
		--self[z];
		return *this;
	}}

	{inline_marco} target_type operator++(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z] }};
		++self[x];
		++self[y];
		++self[z];
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator--(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z] }};
		--self[x];
		--self[y];
		--self[z];
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x], -self[y], -self[z] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

// swizzle3 without assign 
template<typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z>
struct Swizzle3<false, base_type, target_type, x, y, z>
{{
	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x], -self[y], -self[z] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

// swizzle4 with assign  
template<typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z, uint32_t w>
struct Swizzle4<true, base_type, target_type, x, y, z, w>
{{
	using this_type = Swizzle4<true, base_type, target_type, x, y, z, w>;

	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z], self[w] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} this_type& operator=(base_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		self[x] = rhs;
		self[y] = rhs;
		self[z] = rhs;
		self[w] = rhs;
		return *this;
	}}
	
	{inline_marco} this_type& operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		self[y] = prhs[0];
		self[z] = prhs[0];
		self[w] = prhs[0];
		return *this;
	}}

	{inline_marco} this_type& operator++()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		++self[x];
		++self[y];
		++self[z];
		++self[w];
		return *this;
	}}

	{inline_marco} this_type& operator--()
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		--self[x];
		--self[y];
		--self[z];
		--self[w];
		return *this;
	}}

	{inline_marco} target_type operator++(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z], self[w] }};
		++self[x];
		++self[y];
		++self[z];
		++self[w];
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator--(int)
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z], self[w] }};
		--self[x];
		--self[y];
		--self[z];
		--self[w];
		return *reinterpret_cast<target_type*>(pad);
	}}
	
	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z], self[w] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x], -self[y], -self[z], -self[w] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

// swizzle4 without assign 
template<typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z, uint32_t w>
struct Swizzle4<false, base_type, target_type, x, y, z, w>
{{
	{inline_marco} operator target_type() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z], self[w] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator+() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ self[x], self[y], self[z], self[w] }};
		return *reinterpret_cast<target_type*>(pad);
	}}

	{inline_marco} target_type operator-() const noexcept
	{{
		const base_type* self = reinterpret_cast<const base_type*>(this);
		base_type pad[] = {{ -self[x], -self[y], -self[z], -self[w] }};
		return *reinterpret_cast<target_type*>(pad);
	}}
}};

template<bool enable_assignment, typename base_type, typename target_type, uint32_t x>
struct is_swizzle<Swizzle1<enable_assignment, base_type, target_type, x>> {{ static constexpr bool value = true; }};
template<bool enable_assignment, typename base_type, typename target_type, uint32_t x, uint32_t y>
struct is_swizzle<Swizzle2<enable_assignment, base_type, target_type, x, y>> {{ static constexpr bool value = true; }};
template<bool enable_assignment, typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z>
struct is_swizzle<Swizzle3<enable_assignment, base_type, target_type, x, y, z>> {{ static constexpr bool value = true; }};
template<bool enable_assignment, typename base_type, typename target_type, uint32_t x, uint32_t y, uint32_t z, uint32_t w>
struct is_swizzle<Swizzle4<enable_assignment, base_type, target_type, x, y, z, w>> {{ static constexpr bool value = true; }};
}}