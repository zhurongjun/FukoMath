#pragma once
#include "../fuko_math_forward.h"
#include <stdint.h>
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

	{inline_marco} target_type operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		return *reinterpret_cast<target_type*>(this);
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

	{inline_marco} target_type operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		self[y] = prhs[1];
		return *reinterpret_cast<target_type*>(this);
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

	{inline_marco} target_type operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		self[y] = prhs[1];
		self[z] = prhs[2];
		return *reinterpret_cast<target_type*>(this);
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

	{inline_marco} target_type operator=(target_type rhs) noexcept
	{{
		base_type* self = reinterpret_cast<base_type*>(this);
		base_type* prhs = reinterpret_cast<base_type*>(&rhs);
		self[x] = prhs[0];
		self[y] = prhs[1];
		self[z] = prhs[2];
		self[w] = prhs[3];
		return *reinterpret_cast<target_type*>(this);
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
