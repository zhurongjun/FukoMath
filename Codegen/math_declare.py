from typing import List
import config

# abs	Absolute value (per component).	1¹
# acos	Returns the arccosine of each component of x.	1¹
# all	Test if all components of x are nonzero.	1¹
# any	Test if any component of x is nonzero.	1¹
# asin	Returns the arcsine of each component of x.	1¹
# atan	Returns the arctangent of x.	1¹
# atan2	Returns the arctangent of of two values (x,y).	1¹
# ceil	Returns the smallest integer which is greater than or equal to x.	1¹
# clamp	Clamps x to the range [min, max].	1¹
# cos	Returns the cosine of x.	1¹
# cosh	Returns the hyperbolic cosine of x.	1¹
#  countbits	Counts the number of bits (per component) in the input integer.	5
# cross	Returns the cross product of two 3D vectors.	1¹
# degrees	Converts x from radians to degrees.	1¹
# determinant	Returns the determinant of the square matrix m.	1¹
# distance	Returns the distance between two points.	1¹
# dot	Returns the dot product of two vectors.	1
# dst	Calculates a distance vector.	5
# exp	Returns the base-e exponent.	1¹
# exp2	Base 2 exponent (per component).	1¹
# faceforward	Returns -n * sign(dot(i, ng)).	1¹
# firstbithigh	Gets the location of the first set bit starting from the highest order bit and working downward, per component.	5
# firstbitlow	Returns the location of the first set bit starting from the lowest order bit and working upward, per component.	5
#  floor	Returns the greatest integer which is less than or equal to x.	1¹
# fma	Returns the double-precision fused multiply-addition of a * b + c.	5
# fmod	Returns the floating point remainder of x/y.	1¹
# frac	Returns the fractional part of x.	1¹
# frexp	Returns the mantissa and exponent of x.	2¹
# isfinite	Returns true if x is finite, false otherwise.	1¹
# isinf	Returns true if x is +INF or -INF, false otherwise.	1¹
# isnan	Returns true if x is NAN or QNAN, false otherwise.	1¹
# ldexp	Returns x * 2exp	1¹
# length	Returns the length of the vector v.	1¹
# lerp	Returns x + s(y - x).	1¹
# lit	Returns a lighting vector (ambient, diffuse, specular, 1)	1¹
# log	Returns the base-e logarithm of x.	1¹
# log10	Returns the base-10 logarithm of x.	1¹
# log2	Returns the base-2 logarithm of x.	1¹
# mad	Performs an arithmetic multiply/add operation on three values.	5
# max	Selects the greater of x and y.	1¹
# min	Selects the lesser of x and y.	1¹
# modf	Splits the value x into fractional and integer parts.	1¹
# mul	Performs matrix multiplication using x and y.	1
# noise	Generates a random value using the Perlin-noise algorithm.	1¹
# normalize	Returns a normalized vector.	1¹
# pow	Returns xy.	1¹
# radians	Converts x from degrees to radians.	1
# rcp	Calculates a fast, approximate, per-component reciprocal.	5
# reflect	Returns a reflection vector.	1
# refract	Returns the refraction vector.	1¹
# reversebits	Reverses the order of the bits, per component.	5
# round	Rounds x to the nearest integer	1¹
# rsqrt	Returns 1 / sqrt(x)	1¹
# saturate	Clamps x to the range [0, 1]	1
# sign	Computes the sign of x.	1¹
# sin	Returns the sine of x	1¹
# sincos	Returns the sine and cosine of x.	1¹
# sinh	Returns the hyperbolic sine of x	1¹
# smoothstep	Returns a smooth Hermite interpolation between 0 and 1.	1¹
# sqrt	Square root (per component)	1¹
# step	Returns (x >= a) ? 1 : 0	1¹
# tan	Returns the tangent of x	1¹
# tanh	Returns the hyperbolic tangent of x	1¹
# transpose	Returns the transpose of the matrix m.	1
# trunc