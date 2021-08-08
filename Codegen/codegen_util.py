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
