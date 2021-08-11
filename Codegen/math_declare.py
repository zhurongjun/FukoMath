from typing import List, Tuple
from config import all_num_types 
from config import all_floating_types 
from config import all_integer_types 
from config import all_types 
from config import inline_marco

# dimension 
dimension_scale = [1]
dimension_vector = [2, 3, 4]
dimension_any = [1, 2, 3, 4]
dimension_vector3 = [3]

# call std methon 
def loop_call_std_method(func_name:str, params:str, dimension:int) -> str:
    calc_code = "std::{func_name}({params})".format(func_name = func_name, params = params.format(idx = "" if dimension == 1 else "[0]"))
    for idx in range(1, dimension):
        calc_code += ", std::{func_name}({params})".format(func_name = func_name, params = params.format(idx = "[{idx}]".format(idx = idx)))
    return calc_code

class vector_declares:
    # select per component c ? a : b
    select = (all_num_types, dimension_any)
    @staticmethod
    def gen_select(base_type:str, dimension:int) -> str:
        calc_code = "c{idx} ? a{idx} : b{idx}".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += ", c[{i}] ? a[{i}] : b[{i}]".format(i = i)

        return "{inline_marco} {base_type}{dimension} select({base_type}{dimension} a, {base_type}{dimension} b, bool{dimension} c) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )
    
    # select per component c ? a : b
    m_and = (all_types, dimension_any)
    @staticmethod
    def gen_and(base_type:str, dimension:int) -> str:
        calc_code = "x{idx} && y{idx}".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += ", x[{i}] && y[{i}]".format(i = i)

        return "{inline_marco} bool{dimension} and({base_type}{dimension} x, {base_type}{dimension} y) {{ return bool{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )

    # select per component c ? a : b
    m_or = (all_types, dimension_any)
    @staticmethod
    def gen_or(base_type:str, dimension:int) -> str:
        calc_code = "x{idx} || y{idx}".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += ", x[{i}] || y[{i}]".format(i = i)

        return "{inline_marco} bool{dimension} or({base_type}{dimension} x, {base_type}{dimension} y) {{ return bool{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )

    # abs	Absolute value (per component).	1¹
    abs = (all_num_types, dimension_any)
    @staticmethod
    def gen_abs(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} abs({base_type}{dimension} x) {{ return select(x, -x, x > 0); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # acos	Returns the arccosine of each component of x.	1¹
    acos = (all_floating_types, dimension_any)
    @staticmethod
    def gen_acos(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} acos({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("acos", "x{idx}", dimension)
        )
    
    # all	Test if all components of x are nonzero.	1¹
    all = (all_types, dimension_any)
    @staticmethod
    def gen_all(base_type:str, dimension:int) -> str:
        calc_code = "x{idx}".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += " && x[{i}]".format(i = i)

        return "{inline_marco} bool all({base_type}{dimension} x) {{ return {calc_code}; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )

    # any	Test if any component of x is nonzero.	1¹
    any = (all_types, dimension_any)
    @staticmethod
    def gen_any(base_type:str, dimension:int) -> str:
        calc_code = "x{idx}".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += " || x[{i}]".format(i = i)

        return "{inline_marco} bool any({base_type}{dimension} x) {{ return {calc_code}; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )
    
    # asin	Returns the arcsine of each component of x.	1¹
    asin = (all_floating_types, dimension_any)
    @staticmethod
    def gen_asin(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} asin({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("asin", "x{idx}", dimension)
        )

    # atan	Returns the arctangent of x.	1¹
    atan = (all_floating_types, dimension_any)
    @staticmethod
    def gen_atan(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} atan({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("atan", "x{idx}", dimension)
        )

    # atan2	Returns the arctangent of of two values (x,y).	1¹
    atan2 = (all_floating_types, dimension_any)
    @staticmethod
    def gen_atan2(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} atan2({base_type}{dimension} x, {base_type}{dimension} y) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("atan2", "x{idx}, y{idx}", dimension)
        )

    # ceil	Returns the smallest integer which is greater than or equal to x.	1¹
    ceil = (all_floating_types, dimension_any)
    @staticmethod
    def gen_ceil(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} ceil({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("ceil", "x{idx}", dimension)
        )

    # clamp	Clamps x to the range [min, max].	1¹
    clamp = (all_num_types, dimension_any)
    @staticmethod
    def gen_clamp(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} clamp({base_type}{dimension} x, {base_type} min, {base_type} max) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("clamp", "x{idx}, min, max", dimension)
        )

    # cos	Returns the cosine of x.	1¹
    cos = (all_floating_types, dimension_any)
    @staticmethod
    def gen_cos(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} cos({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("cos", "x{idx}", dimension)
        )

    # cosh	Returns the hyperbolic cosine of x.	1¹
    cosh = (all_floating_types, dimension_any)
    @staticmethod
    def gen_cosh(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} cosh({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("cosh", "x{idx}", dimension)
        )

    # cross	Returns the cross product of two 3D vectors.	1¹
    cross = (all_floating_types, dimension_vector3)
    @staticmethod
    def gen_cross(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} cross({base_type}{dimension} x, {base_type}{dimension} y) {{ return (x * y.yzx - x.yzx * y).yzx; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )
    
    # degrees	Converts x from radians to degrees.	1¹
    degrees = (all_floating_types, dimension_any)
    @staticmethod
    def gen_degrees(base_type:str, dimension:int) -> str:
        calc_code = "x{idx} / PI * 180".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += ", x[{i}] / PI * 180".format(i = i)

        return "{inline_marco} {base_type}{dimension} degrees({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )

    # dot	Returns the dot product of two vectors.	1
    dot = (all_num_types, dimension_any)
    @staticmethod
    def gen_dot(base_type:str, dimension:int) -> str:
        calc_code = "x{idx} * y{idx}".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += "+ x[{i}] * y[{i}]".format(i = i)

        return "{inline_marco} {base_type} dot({base_type}{dimension} x, {base_type}{dimension} y) {{ return {calc_code}; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )

    # sqrt	Square root (per component)	1¹
    sqrt = (all_floating_types, dimension_any)
    @staticmethod
    def gen_sqrt(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} sqrt({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("sqrt", "x{idx}", dimension)
        )

    # rsqrt	Returns 1 / sqrt(x)	1¹
    rsqrt = (all_floating_types, dimension_any)
    @staticmethod
    def gen_rsqrt(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} rsqrt({base_type}{dimension} x) {{ return 1 / sqrt(x); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # length	Returns the length of the vector v.	1¹
    length = (all_floating_types, dimension_any)
    @staticmethod
    def gen_length(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type} length({base_type}{dimension} x) {{ return {calc_code}; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = "abs(x)" if dimension == 1 else "sqrt(dot(x, x))"
        )

    # distance	Returns the distance between two points.	1¹
    distance = (all_floating_types, dimension_any)
    @staticmethod
    def gen_distance(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type} length({base_type}{dimension} x, {base_type}{dimension} y) {{ return {calc_code}; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = "abs(y - 1)" if dimension == 1 else "length(y - x)"
        )

    # exp	Returns the base-e exponent.	1¹
    exp = (all_floating_types, dimension_any)
    @staticmethod
    def gen_exp(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} exp({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("exp", "x{idx}", dimension)
        )

    # exp2	Base 2 exponent (per component).	1¹
    exp2 = (all_floating_types, dimension_any)
    @staticmethod
    def gen_exp2(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} exp2({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("exp2", "x{idx}", dimension)
        )

    # floor	Returns the greatest integer which is less than or equal to x.	1¹
    floor = (all_floating_types, dimension_any)
    @staticmethod
    def gen_floor(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} floor({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("floor", "x{idx}", dimension)
        )
    
    # fma	Returns the double-precision fused multiply-addition of a * b + c.	5
    fma = (all_floating_types, dimension_any)
    @staticmethod
    def gen_fma(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} fma({base_type}{dimension} a, {base_type}{dimension} b, {base_type}{dimension} c) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("fma", "a{idx}, b{idx}, c{idx}", dimension)
        )

    # fmod	Returns the floating point remainder of x/y.	1¹
    fmod = (all_floating_types, dimension_any)
    @staticmethod
    def gen_fmod(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} fmod({base_type}{dimension} x, {base_type}{dimension} y) {{ return _floating_mod(x, y); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # frac	Returns the fractional part of x.	1¹
    frac = (all_floating_types, dimension_any)
    @staticmethod
    def gen_frac(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} frac({base_type}{dimension} x) {{ return x - floor(x); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # frexp	Returns the mantissa and exponent of x.	2¹
    frexp = (all_floating_types, dimension_any)
    @staticmethod
    def gen_frexp(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} frexp({base_type}{dimension} x, {base_type}{dimension}& exp) {{ int{dimension} iexp; {base_type}{dimension} ret = {base_type}{dimension}({calc_code}); exp = iexp; return ret; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("frexp", "x{idx}, &iexp{idx}", dimension)
        )

    # isfinite	Returns true if x is finite, false otherwise.	1¹
    isfinite = (all_floating_types, dimension_any)
    @staticmethod
    def gen_isfinite(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} isfinite({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("isfinite", "x{idx}", dimension)
        )

    # isinf	Returns true if x is +INF or -INF, false otherwise.	1¹
    isinf = (all_floating_types, dimension_any)
    @staticmethod
    def gen_isinf(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} isinf({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("isinf", "x{idx}", dimension)
        )

    # isnan	Returns true if x is NAN or QNAN, false otherwise.	1¹
    isnan = (all_floating_types, dimension_any)
    @staticmethod
    def gen_isnan(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} isnan({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("isnan", "x{idx}", dimension)
        )

    # ldexp	Returns x * 2exp	1¹
    ldexp = (all_floating_types, dimension_any)
    @staticmethod
    def gen_ldexp(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} ldexp({base_type}{dimension} x, {base_type}{dimension} exp) {{ return x + exp2(exp); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # lerp	Returns x + s(y - x).	1¹
    lerp = (all_floating_types, dimension_any)
    @staticmethod
    def gen_lerp(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} lerp({base_type}{dimension} x, {base_type}{dimension} y, {base_type}{dimension} s) {{ return x + s * (y - x); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # log	Returns the base-e logarithm of x.	1¹
    log = (all_floating_types, dimension_any)
    @staticmethod
    def gen_log(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} log({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("log", "x{idx}", dimension)
        )

    # log10	Returns the base-10 logarithm of x.	1¹
    log10 = (all_floating_types, dimension_any)
    @staticmethod
    def gen_log10(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} log10({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("log10", "x{idx}", dimension)
        )

    # log2	Returns the base-2 logarithm of x.	1¹
    log2 = (all_floating_types, dimension_any)
    @staticmethod
    def gen_log2(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} log2({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("log2", "x{idx}", dimension)
        )
    
    # mad	Performs an arithmetic multiply/add operation on three values.	5
    mad = (all_num_types, dimension_any)
    @staticmethod
    def gen_mad(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} mad({base_type}{dimension} m, {base_type}{dimension} a, {base_type}{dimension} b) {{ return m * a + b; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # max Selects the greater of x and y.	1¹
    max = (all_num_types, dimension_any)
    @staticmethod
    def gen_max(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} max({base_type}{dimension} x, {base_type}{dimension} y) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("max", "x{idx}, y{idx}", dimension)
        )
    
    # min Selects the lesser of x and y.	1¹
    min = (all_num_types, dimension_any)
    @staticmethod
    def gen_min(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} min({base_type}{dimension} x, {base_type}{dimension} y) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("min", "x{idx}, y{idx}", dimension)
        )
    
    # modf	Splits the value x into fractional and integer parts.	1¹
    modf = (all_floating_types, dimension_any)
    @staticmethod
    def gen_modf(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} modf({base_type}{dimension} x, int{dimension}& ip) {{ {base_type}{dimension} fip; {base_type}{dimension} ret = {base_type}{dimension}({calc_code}); ip = (int{dimension})fip; return ret; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("modf", "x{idx}, &fip{idx}", dimension)
        )

    # normalize	Returns a normalized vector.	1¹
    normalize = (all_floating_types, dimension_any)
    @staticmethod
    def gen_normalize(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} normalize({base_type}{dimension} x) {{ return x / length(x); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # pow	Returns xy.	1¹
    pow = (all_floating_types, dimension_any)
    @staticmethod
    def gen_pow(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} pow({base_type}{dimension} x, {base_type}{dimension} y) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("pow", "x{idx}, y{idx}", dimension)
        )

    # radians	Converts x from degrees to radians.	1
    radians = (all_floating_types, dimension_any)
    @staticmethod
    def gen_radians(base_type:str, dimension:int) -> str:
        calc_code = "x{idx} / 180 * PI".format(idx = "" if dimension == 1 else "[0]")
        for i in range(1, dimension):
            calc_code += ", x[{i}] / 180 * PI".format(i = i)

        return "{inline_marco} {base_type}{dimension} radians({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = calc_code
        )

    # rcp	Calculates a fast, approximate, per-component reciprocal.	5
    rcp = (all_floating_types, dimension_any)
    @staticmethod
    def gen_rcp(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} rcp({base_type}{dimension} x) {{ return 1 / x; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # reflect	Returns a reflection vector.	1
    reflect = (all_floating_types, dimension_any)
    @staticmethod
    def gen_reflect(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} reflect({base_type}{dimension} i, {base_type}{dimension} n) {{ return i - 2 * n * dot(i, n); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # refract	Returns the refraction vector.	1¹
    refract = (all_floating_types, dimension_any)
    @staticmethod
    def gen_refract(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} refract({base_type}{dimension} i, {base_type}{dimension} n, {base_type} eta) {{ {base_type} ni = dot(n, i); {base_type} k = 1 - eta * eta * (1 - ni * ni); return select(0, eta * i - (eta * ni + sqrt(k)) * n, k >= 0); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # round	Rounds x to the nearest integer	1¹
    round = (all_floating_types, dimension_any)
    @staticmethod
    def gen_round(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} round({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("round", "x{idx}", dimension)
        )

    # saturate	Clamps x to the range [0, 1]	1
    saturate = (all_floating_types, dimension_any)
    @staticmethod
    def gen_saturate(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} saturate({base_type}{dimension} x) {{ return clamp(x, 0, 1); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # sign	Computes the sign of x.	1¹
    sign = (all_num_types, dimension_any)
    @staticmethod
    def gen_sign(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} sign({base_type}{dimension} x) {{ return select(0, select(-1, 1, x < 0), x == 0); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # sin	Returns the sine of x	1¹
    sin = (all_floating_types, dimension_any)
    @staticmethod
    def gen_sin(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} sin({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("sin", "x{idx}", dimension)
        )

    # sincos	Returns the sine and cosine of x.	1¹
    sincos = (all_floating_types, dimension_any)
    @staticmethod
    def gen_sincos(base_type:str, dimension:int) -> str:
        return "{inline_marco} void sincos({base_type}{dimension} x, {base_type}{dimension}& s, {base_type}{dimension}& c) {{ s = sin(x); c = cos(x); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )
    
    # sinh	Returns the hyperbolic sine of x	1¹
    sinh = (all_floating_types, dimension_any)
    @staticmethod
    def gen_sinh(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} sinh({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("sinh", "x{idx}", dimension)
        )

    # smoothstep	Returns a smooth Hermite interpolation between 0 and 1.	1¹
    smoothstep = (all_floating_types, dimension_any)
    @staticmethod
    def gen_smoothstep(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} smoothstep({base_type}{dimension} a, {base_type}{dimension} b, {base_type}{dimension} x) {{ {base_type}{dimension}  t = saturate((x - a) / (b - a)); return t * t * (3 - (2 - t)); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # step	Returns (x >= a) ? 1 : 0	1¹
    step = (all_floating_types, dimension_any)
    @staticmethod
    def gen_step(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} step({base_type}{dimension} x, {base_type}{dimension} a) {{ return select(1, 0, x >= a); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
        )

    # tan	Returns the tangent of x	1¹
    tan = (all_floating_types, dimension_any)
    @staticmethod
    def gen_tan(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} tan({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("tan", "x{idx}", dimension)
        )
    
    # tanh	Returns the hyperbolic tangent of x	1¹
    tanh = (all_floating_types, dimension_any)
    @staticmethod
    def gen_tanh(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} tanh({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("tanh", "x{idx}", dimension)
        )

    # trunc
    trunc = (all_floating_types, dimension_any)
    @staticmethod
    def gen_trunc(base_type:str, dimension:int) -> str:
        return "{inline_marco} {base_type}{dimension} trunc({base_type}{dimension} x) {{ return {base_type}{dimension}({calc_code}); }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , dimension = "" if dimension == 1 else dimension
            , calc_code = loop_call_std_method("trunc", "x{idx}", dimension)
        )

    ### unsupport 
    # dst	Calculates a distance vector.	5
    # faceforward	Returns -n * sign(dot(i, ng)).	1¹
    # lit	Returns a lighting vector (ambient, diffuse, specular, 1)	1¹
    # noise	Generates a random value using the Perlin-noise algorithm.	1¹
    
    # firstbithigh	Gets the location of the first set bit starting from the highest order bit and working downward, per component.	5
    # firstbithigh = (all_integer_types, dimension_any)

    # firstbitlow	Returns the location of the first set bit starting from the lowest order bit and working upward, per component.	5
    # firstbitlow = (all_integer_types, dimension_any)
    
    # countbits	Counts the number of bits (per component) in the input integer.	5
    # countbits = (all_integer_types, dimension_any)

    # reversebits	Reverses the order of the bits, per component.	5
    # reversebits = (all_integer_types, dimension_any)


def recurve_gen_determinant(val_name:str, matrix_idx:List[List[Tuple[int, int]]]) -> str:
    if len(matrix_idx) == 2:
        return "{val_name}[{a_r}][{a_c}] * {val_name}[{d_r}][{d_c}] - {val_name}[{b_r}][{b_c}] * {val_name}[{c_r}][{c_c}]".format(
              val_name = val_name
            , a_r = matrix_idx[0][0][0]
            , a_c = matrix_idx[0][0][1]
            , b_r = matrix_idx[0][1][0]
            , b_c = matrix_idx[0][1][1]
            , c_r = matrix_idx[1][0][0]
            , c_c = matrix_idx[1][0][1]
            , d_r = matrix_idx[1][1][0]
            , d_c = matrix_idx[1][1][1]
        )
    else:
        result = ""
        
        for i in range(0, len(matrix_idx[0])):
            # construct algebraic complement matrix 
            new_matrix_idx = matrix_idx.copy()
            for i in range(0, len(matrix_idx)):
                new_matrix_idx[i] = matrix_idx[i].copy()
            del new_matrix_idx[0]
            for vec in new_matrix_idx:
                del vec[i]

            # combine 
            result += "{sign} {val_name}[{v_r}][{v_c}] * ({code}) ".format(
                  sign = "+" if i % 2 == 0 else "-"
                , code = recurve_gen_determinant(val_name, new_matrix_idx)
                , val_name = val_name
                , v_r = matrix_idx[0][i][0]
                , v_c = matrix_idx[0][i][1]
            )

        return result[2:]

class matrix_declares:
    # determinant	Returns the determinant of the square matrix m.	1¹
    determinant = (all_floating_types, lambda row, col: row == col and row > 1)
    @staticmethod
    def gen_determinant(base_type:str, row_size:int, col_size:int) -> str:
        return "{inline_marco} {base_type} determinant({base_type}{row_size}x{col_size} x) {{ return {calc_code}; }}\n".format(
              inline_marco = inline_marco
            , base_type = base_type
            , row_size = row_size
            , col_size = col_size
            , calc_code = recurve_gen_determinant("x", [[(row, col) for col in range(0, col_size)] for row in range(0, row_size)])
        )

    # mul	Performs matrix multiplication using x and y.	1
    # mul(m, m) mul(m, s) mul(s, m) mul(m, v) mul(v, m)
    mul = (all_num_types, lambda row, col: row != 1 or col != 1)
    @staticmethod
    def gen_mul(base_type:str, row_size:int, col_size:int) -> str:
        result = ""

        # mul(m, m)
        rhs_row_size = col_size
        for rhs_col_size in range(1, 5):
            if rhs_col_size == 1 and row_size == 1 or rhs_row_size == 1 and rhs_col_size == 1:
                continue
            calc_code = ""

            # gen calc code 
            for result_row in range(0, row_size):
                for result_col in range(0, rhs_col_size):

                    # result[row][col] = dot(x[row], y[col])
                    for p in range(0, col_size):
                        calc_code += "x[{l_r}]{l_c_idx} * y[{r_r}]{r_c_idx} + ".format(
                              l_r = result_row
                            , l_c_idx = "" if col_size == 1 else "[{l_c}]".format(l_c = p)
                            , r_r = p
                            , r_c_idx = "" if rhs_col_size == 1 else "[{r_c}]".format(r_c = result_col))
                    calc_code = calc_code[0:-3] + ", "
            calc_code = calc_code[0:-2]

            result += "{inline_marco} {base_type}{row_size}x{rhs_col_size} mul({base_type}{row_size}x{col_size} x, {base_type}{rhs_row_size}x{rhs_col_size} y) {{ return {base_type}{row_size}x{rhs_col_size}({calc_code}); }}\n".format(
                inline_marco = inline_marco
            , base_type = base_type
            , row_size = row_size
            , col_size = col_size
            , rhs_row_size = rhs_row_size
            , rhs_col_size = rhs_col_size
            , calc_code =  calc_code)

        # mul(m, v)
        if col_size != 1:
            calc_code = ""
            
            # gen calc code 
            for result_row in range(0, row_size):
                
                # result[row][col] = dot(x[row], y[col])
                for p in range(0, col_size):
                    calc_code += "x[{l_r}]{l_c_idx} * y[{r_r}] + ".format(
                        l_r = result_row
                        , l_c_idx = "" if col_size == 1 else "[{l_c}]".format(l_c = p)
                        , r_r = p)
                calc_code = calc_code[0:-3] + ", "

            calc_code = calc_code[0:-2]

            result += "{inline_marco} {base_type}{row_size_v} mul({base_type}{row_size}x{col_size} x, {base_type}{col_size_v} y) {{ return {base_type}{row_size_v}({calc_code}); }}\n".format(
                    inline_marco = inline_marco
                , base_type = base_type
                , row_size = row_size
                , row_size_v = "" if row_size == 1 else row_size
                , col_size = col_size
                , col_size_v = "" if col_size == 1 else col_size
                , calc_code =  calc_code)

        # mul(v, m)
        if row_size != 1:
            calc_code = ""
            
            # gen calc code 
            for result_col in range(0, col_size):

                # result[row][col] = dot(x[row], y[col])
                for p in range(0, row_size):
                    calc_code += "x{l_c_idx} * y[{r_r}]{r_c_idx} + ".format(
                        l_c_idx = "" if row_size == 1 else "[{l_c}]".format(l_c = p)
                        , r_r = p
                        , r_c_idx = "" if col_size == 1 else "[{r_c}]".format(r_c = result_col))
                calc_code = calc_code[0:-3] + ", "

            calc_code = calc_code[0:-2]

            result += "{inline_marco} {base_type}{col_size_v} mul({base_type}{row_size_v} x, {base_type}{row_size}x{col_size} y) {{ return {base_type}{col_size_v}({calc_code}); }}\n".format(
                inline_marco = inline_marco
                , base_type = base_type
                , row_size = row_size
                , row_size_v = "" if row_size == 1 else row_size
                , col_size = col_size
                , col_size_v = "" if col_size == 1 else col_size
                , calc_code =  calc_code)


        # mul(m, s)
        calc_code = ""
        for row in range(0, row_size):
            for col in range(0, col_size):
                calc_code += "x[{row}]{col_idx} * y, ".format(
                    row = row
                    , col_idx = "" if col_size == 1 else "[{col}]".format(col = col)
                )
        calc_code = calc_code[0:-2]

        result += "{inline_marco} {base_type}{row_size}x{col_size} mul({base_type}{row_size}x{col_size} x, {base_type} y) {{ return {base_type}{row_size}x{col_size}({calc_code}); }}\n".format(
            inline_marco = inline_marco
            , base_type = base_type
            , row_size = row_size
            , col_size = col_size
            , calc_code = calc_code
        )

        # mul(s, m)

        return result
    
    # transpose	Returns the transpose of the matrix m.	1
    transpose = (all_num_types, lambda row, col: row != 1 or col != 1)
    @staticmethod
    def gen_transpose(base_type:str, row_size:int, col_size:int) -> str:
        calc_code = ""

        # gen calc code 
        for col in range(0, col_size):
            for row in range(0, row_size):
                calc_code += "x[{row}]{col_idx}, ".format(
                    row = row
                    , col_idx = "" if col_size == 1 else "[{col}]".format(col = col)
                )
        calc_code = calc_code[0:-2]

        return "{inline_marco} {base_type}{col_size}x{row_size} transpose({base_type}{row_size}x{col_size} x) {{ return {base_type}{col_size}x{row_size}({calc_code}); }}\n".format(
            inline_marco = inline_marco
            , base_type = base_type
            , col_size = col_size
            , row_size = row_size
            , calc_code = calc_code
        )

    # inverse 
    inverse = (all_floating_types, lambda row, col: row == col and row > 1)
    @staticmethod
    def gen_inverse(base_type:str, row_size:int, col_size:int) -> str:
        return ""

    
