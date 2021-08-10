from typing import List
import config
import math_declare

# gen vector ++ --
def gen_vector_increment_decrement(type_list:List[str]) -> str:
    result = ""
    
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

# gen vector operator + - * / % 
def gen_vector_arithmetic(type_list:List[str]) -> str:
    result = ""
    
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
            if type in config.floating_type_mode_list:
                op_code = "_floating_mod(lsh[0], rsh[0])"
                for idx in range(1, dimension):
                    op_code += str.format(", _floating_mod(lsh[0], rsh[0])", idx = idx)
            else:
                op_code = str.format("lsh[0] {op} rsh[0]", op = "%")
                for idx in range(1, dimension):
                    op_code += str.format(", lsh[{idx}] {op} rsh[{idx}]", idx = idx, op = "%")
            
            # gen final code 
            result += str.format("{inline_marco} {type}{dimension} operator {op} (const {type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ return {type}{dimension}({op_code}); }}\n"
            , inline_marco = config.inline_marco
            , type = type
            , dimension = dimension
            , op = "%"
            , op_code = op_code)


    return result

# gen vector operator += -= *= /= %= 
def gen_vector_arithmetic_assign(type_list:List[str]) -> str:
    result = ""
    
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

# gen vector math for per type 
def gen_vertor_math(base_type:str) -> str:
    result = ""

    for k,v in math_declare.vector_declares.__dict__.items():
        if type(v) == tuple and base_type in v[0]:
            for dimension in range(1, 5):
                if dimension in v[1]:
                    result += "// {fun_name} {base_type} {dimension}\n".format(fun_name = k, base_type = base_type, dimension = dimension)

    return result
