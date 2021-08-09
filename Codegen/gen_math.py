from typing import List
import config

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
                result += str.format("{inline_marco} {type}{dimension}& operator{op}({type}{dimension}& v) {{ {increment_code}return v; }}\n"
                , op = op
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , increment_code = increment_code) 

                # gen deferred increment code 
                result += str.format("{inline_marco} {type}{dimension} operator{op}({type}{dimension}& v, int) {{ {type}{dimension} old_val = v; {op}v; return old_val; }}\n"
                , op = op
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension) 
            result += "\n"

    return result

def gen_vector_arithmetic(type_list:List[str]) -> str:
    pass

def gen_vector_arithmetic_assign(type_list:List[str]) -> str:
    pass

# gen vector operator + - * / %, and assign version 