from typing import List
import config

def gen_type_implicit_conversion(base_type:str, implicit_types:List[str]) -> str:
    result = ""

    for dimension in range(2, 5):
        for implicit_type in implicit_types:
            # gen assign code 
            assign_code = ""
            for i in range(0, dimension):
                assign_code += str.format("({implicit_type})pad[{idx}], ", implicit_type = implicit_type, idx = i)
            assign_code = assign_code[0:-2]
            
            # add implicit type case 
            result += str.format("{inline_marco} {base_type}{dimension}::operator {implicit_type}{dimension}() const noexcept {{ return {implicit_type}{dimension}({assign_code}); }}\n"
            , inline_marco = config.inline_marco
            , base_type = base_type
            , implicit_type = implicit_type
            , dimension = dimension
            , assign_code = assign_code)
        result += "\n"

    return result

def gen_implicit_conversion(type_list:List[str]) -> str:
    result = ""

    for type in type_list:
        # find implicit types 
        implicit_types = type_list.copy()
        implicit_types.remove(type)

        # gen code 
        result += str.format("// {base_type} implicit conversion\n", base_type = type)
        result += gen_type_implicit_conversion(type, implicit_types)

    return result
        

# gen asxxx


# gen vector operator + - * / %, and assign version 
# gen vector ++ --
