from typing import List
import config
import math_declare
import codegen_util as util

# Swizzle op tempalte 
swizzle_op_swizzle_template = '''template<bool has_assign_l, bool has_assign_r, typename base_type_l, typename base_type_r, typename target_type_l, typename target_type_r{template_code_l}{template_code_r}> 
{inline_marco} {return_type} operator {op} (
      const Swizzle{dimension}<has_assign_l, base_type_l, target_type_l{assign_code_l}>& lhs
    , const Swizzle{dimension}<has_assign_r, base_type_r, target_type_r{assign_code_r}>& rhs) noexcept 
{{ 
    const base_type_l* pLhs = reinterpret_cast<const base_type_l*>(&lhs);
    const base_type_r* pRhs = reinterpret_cast<const base_type_r*>(&rhs);

    return {return_type}({op_code}); 
}}\n'''

swizzle_op_scalar_template = '''template<bool has_assign_l, typename base_type_l, typename base_type_r, typename target_type_l{template_code_l}, typename = std::enable_if_t<!is_swizzle_v<std::remove_cv_t<base_type_r>>, void>> 
{inline_marco} {return_type} operator {op} (
      const Swizzle{dimension}<has_assign_l, base_type_l, target_type_l{assign_code_l}>& lhs
    , const base_type_r rhs) noexcept 
{{ 
    const base_type_l* pLhs = reinterpret_cast<const base_type_l*>(&lhs);
    
    return {return_type}({op_code}); 
}}\n'''

scalar_op_swizzle_template = '''template<bool has_assign_r, typename base_type_l, typename base_type_r, typename target_type_r{template_code_r}, typename = std::enable_if_t<!is_swizzle_v<std::remove_cv_t<base_type_l>>, void>> 
{inline_marco} {return_type} operator {op} (
      const base_type_l lhs
    , const Swizzle{dimension}<has_assign_r, base_type_r, target_type_r{assign_code_r}>& rhs) noexcept 
{{ 
    const base_type_r* pRhs = reinterpret_cast<const base_type_r*>(&rhs);
    
    return {return_type}({op_code}); 
}}\n'''

# Swizzle assign op tempalte 
swizzle_op_swizzle_assign_template = '''template<bool has_assign_l, bool has_assign_r, typename base_type_l, typename base_type_r, typename target_type_l, typename target_type_r{template_code_l}{template_code_r}> 
{inline_marco} Swizzle{dimension}<has_assign_l, base_type_l, target_type_l{assign_code_l}>& operator {op}= (
      Swizzle{dimension}<has_assign_l, base_type_l, target_type_l{assign_code_l}>& lhs
    , const Swizzle{dimension}<has_assign_r, base_type_r, target_type_r{assign_code_r}>& rhs) noexcept 
{{ 
    base_type_l* pLhs = reinterpret_cast<base_type_l*>(&lhs);
    const base_type_r* pRhs = reinterpret_cast<const base_type_r*>(&rhs);

    base_type_l pad[] = {{ {op_code} }};
    
{assign_op_code}
    return lhs; 
}}\n'''

swizzle_op_scalar_assign_template = '''template<bool has_assign_l, typename base_type_l, typename base_type_r, typename target_type_l{template_code_l}, typename = std::enable_if_t<!is_swizzle_v<std::remove_cv_t<base_type_r>>, void>> 
{inline_marco} Swizzle{dimension}<has_assign_l, base_type_l, target_type_l{assign_code_l}>& operator {op}= (
      Swizzle{dimension}<has_assign_l, base_type_l, target_type_l{assign_code_l}>& lhs
    , const base_type_r rhs) noexcept 
{{ 
    base_type_l* pLhs = reinterpret_cast<base_type_l*>(&lhs);
    
{assign_op_code}
    return lhs; 
}}\n'''

util_op_template = ", {lhs} {op} {rhs}"
mod_op_template = ", _mod({lhs}, {rhs})"
util_assign_op_template = "\t\t{lhs} = {pad};\n"
util_assign_op_s_template = "\t\t{lhs} = {lhs} {op} {rhs};\n"
util_mod_assign_op_s_template = "\t\t{lhs} = _mod({lhs}, {rhs});\n"

def gen_swizzle_op(template:str, dimension:int, op_template:str, op:str, return_type:str, swizzle_l:bool, swizzle_r:bool, assign_op_template:str = "") -> str:
    template_code_l = ""
    template_code_r = ""
    assign_code_l = ""
    assign_code_r = ""
    op_code = ""
    assign_op_code = ""
    
    # gen template code 
    for d in range(0, dimension):
        template_code_l += ", uint32_t {comp}_l".format(comp = util.math_swizzle_pad[d])
        template_code_r += ", uint32_t {comp}_r".format(comp = util.math_swizzle_pad[d])
        assign_code_l += ", {comp}_l".format(comp = util.math_swizzle_pad[d])
        assign_code_r += ", {comp}_r".format(comp = util.math_swizzle_pad[d])
        op_code += op_template.format(
            lhs = "pLhs[{d}_l]".format(d = util.math_swizzle_pad[d]) if swizzle_l else "lhs"
            , rhs = "pRhs[{d}_r]".format(d = util.math_swizzle_pad[d]) if swizzle_r else "rhs"
            , op = op)
        assign_op_code += assign_op_template.format(
            lhs = "pLhs[{d}_l]".format(d = util.math_swizzle_pad[d]) if swizzle_l else "lhs"
            , rhs = "pRhs[{d}_r]".format(d = util.math_swizzle_pad[d]) if swizzle_r else "rhs"
            , pad = "pad[{d}]".format(d = d)
            , op = op)
    op_code = op_code[2:]

    # gen final code 
    return template.format(
          template_code_l = template_code_l
        , dimension = dimension
        , template_code_r = template_code_r
        , assign_code_l = assign_code_l
        , assign_code_r = assign_code_r
        , inline_marco = config.inline_marco
        , return_type = return_type
        , op_code = op_code
        , assign_op_code = assign_op_code
        , op = op)

# gen vector ++ --
def gen_vector_increment_decrement(type_list:List[str]) -> str:
    result = ""
    
    return result

    for op in ["++", "--"]:
        for type in type_list:
            result += str.format("// {type} {op}\n", type = type, op = op)
            for dimension in range(2, 5):
                increment_code = ""
                for idx in range(0, dimension):
                    increment_code += str.format("{op}v.pad[{idx}]; ", op = op, idx = idx)

                # gen forward increment code 
                result += str.format("{inline_marco} {type}{dimension}& operator{op}({type}{dimension}& v) noexcept {{ {increment_code}return v; }}\n"
                , op = op
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , increment_code = increment_code) 

                # gen deferred increment code 
                result += str.format("{inline_marco} {type}{dimension} operator{op}({type}{dimension}& v, int) noexcept {{ {type}{dimension} old_val = v; {op}v; return old_val; }}\n"
                , op = op
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension) 
            result += "\n"

    return result

# gen vector operator + - * / % > < >= <= == != 
def gen_vector_arithmetic(type_list:List[str]) -> str:
    result = ""

    return result
    
    for type in type_list:
        # gen +-*/
        for op in ["+", "-", "*", "/"]:
            result += str.format("// {type} {op} {type}\n", type = type, op = op)
            for dimension in range(2, 5):
                # gen op code 
                op_code = str.format("lsh[0] {op} rsh[0]", op = op)
                for idx in range(1, dimension):
                    op_code += str.format(", lsh[{idx}] {op} rsh[{idx}]", idx = idx, op = op)
                
                # gen final code 
                result += str.format("{inline_marco} {type}{dimension} operator {op} (const {type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ return {type}{dimension}({op_code}); }}\n"
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , op = op
                , op_code = op_code)

        # gen % 
        result += str.format("// {type} {op} {type}\n", type = type, op = "%")
        for dimension in range(2, 5):
            op_code : str

            # gen op code 
            if type in config.floating_type_mod_list:
                op_code = "_mod(lsh{idx}, rsh{idx})".format(idx = "" if dimension == 1 else "[0]")
                for idx in range(1, dimension):
                    op_code += str.format(", _mod(lsh{idx}, rsh{idx})", idx = "" if dimension == 1 else "[{dimension}]".format(dimension = dimension))
            else:
                op_code = str.format("lsh[0] {op} rsh[0]", op = "%")
                for idx in range(1, dimension):
                    op_code += str.format(", lsh[{idx}] {op} rsh[{idx}]", idx = idx, op = "%")
            
            # gen final code 
            result += str.format("{inline_marco} {type}{dimension} operator {op} (const {type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ return {type}{dimension}({op_code}); }}\n"
            , inline_marco = config.inline_marco
            , type = type
            , dimension = "" if dimension == 1 else dimension
            , op = "%"
            , op_code = op_code)

        # gen compare 
        for op in [">", "<", ">=", "<=", "==", "!="]:
            result += str.format("// {type} {op} {type}\n", type = type, op = op)
            for dimension in range(2, 5):
                # gen op code 
                op_code = str.format("lsh[0] {op} rsh[0]", op = op)
                for idx in range(1, dimension):
                    op_code += str.format(", lsh[{idx}] {op} rsh[{idx}]", idx = idx, op = op)
                
                # gen final code 
                result += str.format("{inline_marco} bool{dimension} operator {op} (const {type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ return bool{dimension}({op_code}); }}\n"
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , op = op
                , op_code = op_code)

        # gen sign 
        if type in config.minus_type_list:
            for op in ["+", "-"]:
                result += str.format("// {op} {type}\n", type = type, op = op)
                for dimension in range(2, 5):
                    # gen op code 
                    op_code = str.format("{op}x[0]", op = op)
                    for idx in range(1, dimension):
                        op_code += str.format(", {op}x[{idx}]", idx = idx, op = op)
                    
                    # gen final code 
                    result += str.format("{inline_marco} {type}{dimension} operator {op} (const {type}{dimension}& x) noexcept {{ return {type}{dimension}({op_code}); }}\n"
                    , inline_marco = config.inline_marco
                    , type = type
                    , dimension = dimension
                    , op = op
                    , op_code = op_code)
        
        # gen bool not(!) 
        result += str.format("// {op} {type}\n", type = type, op = "!")
        for dimension in range(2, 5):
            # gen op code 
            op_code = str.format("{op}x[0]", op = "!")
            for idx in range(1, dimension):
                op_code += str.format(", {op}x[{idx}]", idx = idx, op = "!")
            
            # gen final code 
            result += str.format("{inline_marco} bool{dimension} operator {op} (const {type}{dimension}& x) noexcept {{ return bool{dimension}({op_code}); }}\n"
            , inline_marco = config.inline_marco
            , type = type
            , dimension = dimension
            , op = "!"
            , op_code = op_code)

    return result

# gen vector operator += -= *= /= %= 
def gen_vector_arithmetic_assign(type_list:List[str]) -> str:
    result = ""

    return result
    
    for type in type_list:
        for op in ["+", "-", "*", "/", "%"]:
            result += str.format("// {type} {op}= {type}\n", type = type, op = op)
            for dimension in range(2, 5):
                result += str.format("{inline_marco} {type}{dimension}& operator {op}= ({type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ lsh = lsh {op} rsh; return lsh; }}\n"
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , op = op)

    return result

# gen swizzle operator + - * / % > < >= <= == != 
def gen_swizzle_arithmetic() -> str:
    result = ""

    # gen +-*/
    for op in ["+", "-", "*", "/"]:
        for dimension in range(1, 5):
            result += gen_swizzle_op(swizzle_op_swizzle_template, dimension, util_op_template, op, "target_type_l", True, True)
            result += gen_swizzle_op(swizzle_op_scalar_template,  dimension, util_op_template, op, "target_type_l", True, False)
            result += gen_swizzle_op(scalar_op_swizzle_template,  dimension, util_op_template, op, "target_type_r", False, True)
    
    # gen %
    for op in ["%"]:
        for dimension in range(1, 5):
            result += gen_swizzle_op(swizzle_op_swizzle_template, dimension, mod_op_template, op, "target_type_l", True, True)
            result += gen_swizzle_op(swizzle_op_scalar_template,  dimension, mod_op_template, op, "target_type_l", True, False)
            result += gen_swizzle_op(scalar_op_swizzle_template,  dimension, mod_op_template, op, "target_type_r", False, True)

    # gen > < >= <= == !=
    for op in [">", "<", ">=", "<=", "==", "!="]:
        for dimension in range(1, 5):
            result += gen_swizzle_op(swizzle_op_swizzle_template, dimension, util_op_template, op, "bool{d}".format(d = "" if dimension == 1 else dimension), True, True)
            result += gen_swizzle_op(swizzle_op_scalar_template,  dimension, util_op_template, op, "bool{d}".format(d = "" if dimension == 1 else dimension), True, False)
            result += gen_swizzle_op(scalar_op_swizzle_template,  dimension, util_op_template, op, "bool{d}".format(d = "" if dimension == 1 else dimension), False, True)

    return result

# gen swizzle operator += -= *= /= %= 
def gen_swizzle_arithmetic_assign() -> str:
    result = ""

    # gen +-*/
    for op in ["+", "-", "*", "/"]:
        for dimension in range(1, 5):
            result += gen_swizzle_op(swizzle_op_swizzle_assign_template, dimension, util_op_template, op, "target_type_l", True, True, util_assign_op_template)
            result += gen_swizzle_op(swizzle_op_scalar_assign_template,  dimension, util_op_template, op, "target_type_l", True, False, util_assign_op_s_template)
    
    # gen %
    for op in ["%"]:
        for dimension in range(1, 5):
            result += gen_swizzle_op(swizzle_op_swizzle_assign_template, dimension, mod_op_template, op, "target_type_l", True, True, util_assign_op_template)
            result += gen_swizzle_op(swizzle_op_scalar_assign_template,  dimension, mod_op_template, op, "target_type_l", True, False, util_mod_assign_op_s_template)

    return result

# gen vector math for per type 
def gen_vertor_math(base_type:str) -> str:
    result = ""

    for k,v in math_declare.vector_declares.__dict__.items():
        # check support function 
        if type(v) == tuple and base_type in v[0]:
            fun_name = str(k) if k[0:2] != "m_" else k[2:]
            result += "// {fun_name} \n".format(fun_name = fun_name)
            
            # get attr 
            if hasattr(math_declare.vector_declares, "gen_" + fun_name):
                f = getattr(math_declare.vector_declares, "gen_" + fun_name)
                
                # each dimension 
                for dimension in range(1, 5):
                    if dimension in v[1]:
                        result += f(base_type, dimension)
            result += "\n"

    return result

# gen matrix math for per type 
def gen_matrix_math(base_type:str) -> str:
    result = ""

    for k,v in math_declare.matrix_declares.__dict__.items():
        # check support function 
        if type(v) == tuple and base_type in v[0]:
            fun_name = str(k) if k[0:2] != "m_" else k[2:]
            result += "// {fun_name} \n".format(fun_name = fun_name)
            
            # get attr 
            if hasattr(math_declare.matrix_declares, "gen_" + fun_name):
                f = getattr(math_declare.matrix_declares, "gen_" + fun_name)
                
                # each matrix dimension 
                for row_size in range(1, 5):
                    for col_size in range(1,5):
                        if v[1](row_size, col_size):
                            result += f(base_type, row_size, col_size)
            result += "\n"

    return result