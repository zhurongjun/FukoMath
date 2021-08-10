from typing import List
import config
from config import all_num_types 
from config import all_floating_types 
from config import all_integer_types 
from config import all_types 
from config import bool_only 
from config import uint_only 

# dimension 
dimension_scale = [1]
dimension_vector = [2, 3, 4]
dimension_any = [1, 2, 3, 4]
dimension_vector3 = [3]

class vector_declares:
    # abs	Absolute value (per component).	1¹
    abs = (all_num_types, dimension_any)

    # acos	Returns the arccosine of each component of x.	1¹
    acos = (all_floating_types, dimension_any)
    
    # all	Test if all components of x are nonzero.	1¹
    all = (all_types, dimension_any)

    # any	Test if any component of x is nonzero.	1¹
    any = (all_types, dimension_any)
    
    # asin	Returns the arcsine of each component of x.	1¹
    asin = (all_floating_types, dimension_any)
    
    # atan	Returns the arctangent of x.	1¹
    atan = (all_floating_types, dimension_any)

    # atan2	Returns the arctangent of of two values (x,y).	1¹
    atan2 = (all_floating_types, dimension_any)
    
    # ceil	Returns the smallest integer which is greater than or equal to x.	1¹
    ceil = (all_floating_types, dimension_any)

    # clamp	Clamps x to the range [min, max].	1¹
    clamp = (all_num_types, dimension_any)

    # cos	Returns the cosine of x.	1¹
    cos = (all_floating_types, dimension_any)

    # cosh	Returns the hyperbolic cosine of x.	1¹
    cosh = (all_floating_types, dimension_any)

    # countbits	Counts the number of bits (per component) in the input integer.	5
    countbits = (uint_only, dimension_any)

    # cross	Returns the cross product of two 3D vectors.	1¹
    cross = (all_floating_types, dimension_vector3)
    
    # degrees	Converts x from radians to degrees.	1¹
    degrees = (all_floating_types, dimension_any)
        
    # distance	Returns the distance between two points.	1¹
    distance = (all_floating_types, dimension_any)

    # dot	Returns the dot product of two vectors.	1
    dot = (all_num_types, dimension_any)

    # exp	Returns the base-e exponent.	1¹
    exp = (all_floating_types, dimension_any)

    # exp2	Base 2 exponent (per component).	1¹
    exp2 = (all_floating_types, dimension_any)

    # firstbithigh	Gets the location of the first set bit starting from the highest order bit and working downward, per component.	5
    firstbithigh = (uint_only, dimension_any)

    # firstbitlow	Returns the location of the first set bit starting from the lowest order bit and working upward, per component.	5
    firstbitlow = (uint_only, dimension_any)
    
    # floor	Returns the greatest integer which is less than or equal to x.	1¹
    floor = (all_floating_types, dimension_any)
    
    # fma	Returns the double-precision fused multiply-addition of a * b + c.	5
    fma = (all_floating_types, dimension_any)

    # fmod	Returns the floating point remainder of x/y.	1¹
    fmod = (all_floating_types, dimension_any)

    # frac	Returns the fractional part of x.	1¹
    frac = (all_floating_types, dimension_any)

    # frexp	Returns the mantissa and exponent of x.	2¹
    frexp = (all_floating_types, dimension_any)

    # isfinite	Returns true if x is finite, false otherwise.	1¹
    isfinite = (all_floating_types, dimension_any)

    # isinf	Returns true if x is +INF or -INF, false otherwise.	1¹
    isinf = (all_floating_types, dimension_any)

    # isnan	Returns true if x is NAN or QNAN, false otherwise.	1¹
    isnan = (all_floating_types, dimension_any)

    # ldexp	Returns x * 2exp	1¹
    ldexp = (all_floating_types, dimension_any)
    
    # length	Returns the length of the vector v.	1¹
    length = (all_floating_types, dimension_any)

    # lerp	Returns x + s(y - x).	1¹
    lerp = (all_floating_types, dimension_any)

    # log	Returns the base-e logarithm of x.	1¹
    log = (all_floating_types, dimension_any)

    # log10	Returns the base-10 logarithm of x.	1¹
    log10 = (all_floating_types, dimension_any)

    # log2	Returns the base-2 logarithm of x.	1¹
    log2 = (all_floating_types, dimension_any)
    
    # mad	Performs an arithmetic multiply/add operation on three values.	5
    mad = (all_num_types, dimension_any)

    # max	Selects the greater of x and y.	1¹
    max = (all_num_types, dimension_any)
    
    # min	Selects the lesser of x and y.	1¹
    min = (all_num_types, dimension_any)
    
    # modf	Splits the value x into fractional and integer parts.	1¹
    modf = (all_floating_types, dimension_any)

    # normalize	Returns a normalized vector.	1¹
    normalize = (all_floating_types, dimension_any)

    # pow	Returns xy.	1¹
    pow = (all_floating_types, dimension_any)

    # radians	Converts x from degrees to radians.	1
    radians = (all_floating_types, dimension_any)

    # rcp	Calculates a fast, approximate, per-component reciprocal.	5
    rcp = (all_floating_types, dimension_any)

    # reflect	Returns a reflection vector.	1
    reflect = (all_floating_types, dimension_any)

    # refract	Returns the refraction vector.	1¹
    refract = (all_floating_types, dimension_any)

    # reversebits	Reverses the order of the bits, per component.	5
    reversebits = (uint_only, dimension_any)

    # round	Rounds x to the nearest integer	1¹
    round = (all_floating_types, dimension_any)
    
    # rsqrt	Returns 1 / sqrt(x)	1¹
    rsqrt = (all_floating_types, dimension_any)

    # saturate	Clamps x to the range [0, 1]	1
    saturate = (all_floating_types, dimension_any)

    # sign	Computes the sign of x.	1¹
    sign = (all_num_types, dimension_any)

    # sin	Returns the sine of x	1¹
    sin = (all_floating_types, dimension_any)

    # sincos	Returns the sine and cosine of x.	1¹
    sincos = (all_floating_types, dimension_any)
    
    # sinh	Returns the hyperbolic sine of x	1¹
    sinh = (all_floating_types, dimension_any)
    
    # smoothstep	Returns a smooth Hermite interpolation between 0 and 1.	1¹
    smoothstep = (all_floating_types, dimension_any)
    
    # sqrt	Square root (per component)	1¹
    sqrt = (all_floating_types, dimension_any)
    
    # step	Returns (x >= a) ? 1 : 0	1¹
    step = (all_floating_types, dimension_any)

    # tan	Returns the tangent of x	1¹
    tan = (all_floating_types, dimension_any)
    
    # tanh	Returns the hyperbolic tangent of x	1¹
    tanh = (all_floating_types, dimension_any)

    # trunc
    trunc = (all_floating_types, dimension_any)

    ### unsupport 
    # dst	Calculates a distance vector.	5
    # faceforward	Returns -n * sign(dot(i, ng)).	1¹
    # lit	Returns a lighting vector (ambient, diffuse, specular, 1)	1¹
    # noise	Generates a random value using the Perlin-noise algorithm.	1¹

class matrix_declares:
    pass
    # determinant	Returns the determinant of the square matrix m.	1¹
    # mul	Performs matrix multiplication using x and y.	1
    # transpose	Returns the transpose of the matrix m.	1
    