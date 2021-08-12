#pragma once

// swizzle ops 
// + - * / %
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator + (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) {{ return lsh + target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator - (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) {{ return lsh - target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator * (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) {{ return lsh * target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator / (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) {{ return lsh / target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator % (const target_type& lsh, const Swizzle<has_assign, base_type, target_type, sequence...> rsh) {{ if constexpr(std::is_same_v<target_type, float> || std::is_same_v<target_type, double>) return {math_namespace}::fmod(lsh, target_type(rsh)); else return lsh % target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator + (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) {{ return target_type(lsh) + rsh; }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator - (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) {{ return target_type(lsh) - rsh; }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator * (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) {{ return target_type(lsh) * rsh; }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator / (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) {{ return target_type(lsh) / rsh; }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator % (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const target_type& rsh) {{ if constexpr(std::is_same_v<target_type, float> || std::is_same_v<target_type, double>) return {math_namespace}::fmod(target_type(lsh), rsh); else return target_type(lsh) % rsh; }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator + (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const Swizzle<has_assign, base_type, target_type, sequence...>& rsh) {{ return target_type(lsh) + target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator - (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const Swizzle<has_assign, base_type, target_type, sequence...>& rsh) {{ return target_type(lsh) - target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator * (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const Swizzle<has_assign, base_type, target_type, sequence...>& rsh) {{ return target_type(lsh) * target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator / (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const Swizzle<has_assign, base_type, target_type, sequence...>& rsh) {{ return target_type(lsh) / target_type(rsh); }}
template<bool has_assign, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator % (const Swizzle<has_assign, base_type, target_type, sequence...> lsh, const Swizzle<has_assign, base_type, target_type, sequence...>& rsh) {{ if constexpr(std::is_same_v<target_type, float> || std::is_same_v<target_type, double>) return {math_namespace}::fmod(target_type(lsh), target_type(rsh)); else return target_type(lsh) % target_type(rsh); }}


// += -= *= /= %=
template<typename rhs_type, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator += (Swizzle<true, base_type, target_type, sequence...>& lsh, const rhs_type& rsh) {{ return lsh = lsh + target_type(rsh); }}
template<typename rhs_type, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator -= (Swizzle<true, base_type, target_type, sequence...>& lsh, const rhs_type& rsh) {{ return lsh = lsh - target_type(rsh); }}
template<typename rhs_type, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator *= (Swizzle<true, base_type, target_type, sequence...>& lsh, const rhs_type& rsh) {{ return lsh = lsh * target_type(rsh); }}
template<typename rhs_type, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator /= (Swizzle<true, base_type, target_type, sequence...>& lsh, const rhs_type& rsh) {{ return lsh = lsh / target_type(rsh); }}
template<typename rhs_type, typename base_type, typename target_type, uint32_t... sequence> {inline_marco} target_type operator %= (Swizzle<true, base_type, target_type, sequence...>& lsh, const rhs_type& rsh) {{ return lsh = lsh % target_type(rsh); }}

// > < <= >= == != 

// + - sign 

// ! bool not 

// undef 
#undef {inline_marco}

// TODO. disable warning 
