from typing import List
import codegen_util as util
import config

def recursive_gen_constructor(base_type_name:str, raw_size:int, remain_size:int, case_cache:List[int], result:List[str]) -> None:
    if remain_size == 0: # gen code 
        # begin constructor 
        case_str = str.format("{type}(", type = base_type_name + str(raw_size))

        # gen params 
        cur_count = 0
        for count in case_cache:
            case_str += base_type_name + str(count) + " " if count > 1 else base_type_name + " "
            for i in range(0, count):
                case_str += util.math_swizzle_pad[cur_count]
                cur_count += 1
            case_str += ", "

        # end params, begin initializer    
        case_str = case_str[0:-2]
        case_str += ") : pad { "

        # gen initializer 
        cur_count = 0
        for count in case_cache:
            if count == 1:
                case_str += util.math_swizzle_pad[cur_count] + ", "
                cur_count += 1
            else:
                param_str = ""
                base_count = 0
                
                # gen param str 
                for i in range(0, count):
                    param_str += util.math_swizzle_pad[cur_count]
                    cur_count += 1
                
                # gen swizzle 
                for i in range(0, count):
                    case_str += param_str + "." + util.math_swizzle_pad[base_count] + ", "
                    base_count += 1
        
        # end constructor 
        case_str = case_str[0:-2]
        case_str += " } {}"

        result.append(case_str)
    else: # recusive 
        for i in range(1, remain_size + 1):
            if i == raw_size: continue
            case_cache.append(i)
            recursive_gen_constructor(base_type_name, raw_size, remain_size - i, case_cache, result)
            case_cache.pop()

def gen_constructor_vector(base_type_name:str, size:int) -> str:
    result = ""
    
    # gen basic swizzle init 
    result += "\t" + config.inline_marco + " " + base_type_name + str(size) + "() : pad { 0 } {}\n"
    result += "\t" + config.inline_marco + " " + base_type_name + str(size) + "(float n) : pad { "
    for i in range(0, size):
        result += "n, "
    result = result[0:-2]
    result += " } {}\n"

    # gen swizzle init 
    case_cache : List[int] = []
    swizzle_result : List[str] = []
    recursive_gen_constructor(base_type_name, size, size, case_cache, swizzle_result)
    for s in swizzle_result:
        result += "\t" + config.inline_marco + " " + s + "\n"

    return result

def gen_type_code_vector(base_type_name:str, implicit_convert_types:List[str] = []) ->str:
    result = ""
  
    # gen structures 
    for i in range(2, 5):
        # begin struct 
        result += str.format("struct {base_type}{dimension}\n{{\n", base_type = base_type_name, dimension = i)
        
        # gen constructor 
        result += "\t// constructor\n"
        result += gen_constructor_vector(base_type_name, i)

        # gen access operator 
        result += "\n\t// access operator"
        result += str.format('''
\t{inline_marco} {base_type}& operator[](int index) noexcept {{ return pad[index]; }}
\t{inline_marco} {base_type} operator[](int index) const noexcept {{ return pad[index]; }}
'''
    , base_type = base_type_name
    , inline_marco = config.inline_marco)

        # gen implicit convert operator 
        result += "\n\t// implicit convert operator\n"
        for implicit_type in implicit_convert_types:
            result += str.format("\t{inline_marco} operator {base_type}{dimension}() const noexcept;\n"
            , base_type = implicit_type
            , dimension = i
            , inline_marco = config.inline_marco)

        # gen union 
        result += str.format('''
    union
\t{{
\t\t{base_type} pad[{dimension}];
\t\t#define {type_marco} {base_type}
\t\t#include "../Swizzle/swizzle{dimension}"
\t\t#undef {type_marco}
\t}};
'''
    , base_type = base_type_name
    , dimension = i
    , type_marco = util.swizzle_type_marco)

        # end struct 
        result += "};\n\n"

    return result;

def gen_forward_declare_vector(type_list:List[int]) -> str:
    result = ""
    
    for type in type_list:
        for dimension in range(2, 5):
            result += str.format("struct {type_name}{dimension};\n", type_name = type,  dimension = dimension);
    
    return result

def gen_type_code_matrix(base_type_name:str) -> str:
    result = ""

    for row_size in range(1, 5):
        for col_size in range(1, 5):
            if row_size == 1 and col_size == 1:
                continue
            else:
                # begin struct 
                result += str.format("struct {base_type}{row_size}x{col_size}\n{{\n", base_type = base_type_name, row_size = row_size, col_size = col_size)

                # gen default constructor 

                # gen vector constructor 

                # gen access operator 
                result += "\t// access operator"
                if col_size == 1:
                    result += str.format('''
\t{inline_marco} {base_type}& operator[](int index) noexcept {{ return pad[index]; }}
\t{inline_marco} {base_type} operator[](int index) const noexcept {{ return pad[index]; }}
'''                 
                    , base_type = base_type_name
                    , inline_marco = config.inline_marco)
                else:
                    result += str.format('''
\t{inline_marco} {base_type}{dimension}& operator[](int index) noexcept {{ return (({base_type}{dimension}*)pad)[index]; }}
\t{inline_marco} {base_type}{dimension} operator[](int index) const noexcept {{ return (({base_type}{dimension}*)pad)[index]; }}
'''
                    , base_type = base_type_name
                    , inline_marco = config.inline_marco
                    , dimension = col_size)

                # begin union 
                result += "\n\tunion\n\t{\n"

                # gen pad 
                result += str.format("\t\t{base_type} pad[{pad_size}];\n", base_type = base_type_name, pad_size = row_size * col_size)

                # gen siwzzle 
                if config.enable_matrix_swizzle:
                    result += str.format("\t\t#define {type_marco} {base_type}\n", type_marco = util.swizzle_type_marco, base_type = base_type_name)
                    result += str.format('''\t\t#include "../Swizzle/swizzle{row_size}x{col_size}"\n''', row_size = row_size, col_size = col_size)
                    result += str.format("\t\t#undef {type_marco}\n", type_marco = util.swizzle_type_marco)

                # end union 
                result += "\t};\n"

                # end struct 
                result += "};\n\n"

    return result

def gen_forward_declare_matrix(typelist:List[int]) -> str:
    result = ""

    for type in typelist:
        for row_size in range(1, 5):
            for col_size in range(1, 5):
                if row_size == 1 and col_size == 1:
                    continue
                else:
                    result += str.format("struct {type_name}{row_size}x{col_size};\n", type_name = type, row_size = row_size, col_size = col_size)
    
    return result

