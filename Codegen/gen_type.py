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
        case_str += ") noexcept : pad { "

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
    
    type_name = base_type_name + str(size)

    # gen basic swizzle init 
    result += str.format("\t{inline_marco} {type_name}() noexcept : pad {{ 0 }}{{}}\n", inline_marco = config.inline_marco, type_name = type_name)
    result += str.format("\t{inline_marco} {type_name}({base_type} n) noexcept : pad {{ ", inline_marco = config.inline_marco, type_name = type_name, base_type = base_type_name)
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
        assign_code = ""
        for comp in range(0, i):
            assign_code += ", {comp}".format(comp = comp)
        # begin struct 
        result += str.format("struct {base_type}{dimension} : Swizzle{dimension}<true, {base_type}, {base_type}{dimension}{assign_code}>\n{{\n", base_type = base_type_name, dimension = i, assign_code = assign_code)
        
        # gen constructor 
        result += "\t// constructor\n"
        result += gen_constructor_vector(base_type_name, i)

        # gen convert constructor 
        result += "\n\t// convert constructor\n"
        for implicit_type in implicit_convert_types:
            result += str.format("\t{inline_marco} {convert_type}{base_type}{dimension}(const {implicit_type}{dimension}& v) noexcept;\n"
            , convert_type =  "" if base_type_name in config.implicit_convert_dic[implicit_type] else "explicit "
            , base_type = base_type_name
            , implicit_type = implicit_type
            , dimension = i
            , inline_marco = config.inline_marco)

        # gen swizzle convert constructor 
        result += "\n\t// swizzle convert constructor\n"
#        result += '''\ttemplate<>
#\t{inline_marco} {base_type}{dimension}'''

        # gen access operator 
        result += "\n\t// access operator"
        result += str.format('''
\t{inline_marco} {base_type}& operator[](int index) noexcept {{ return pad[index]; }}
\t{inline_marco} {base_type} operator[](int index) const noexcept {{ return pad[index]; }}
'''
    , base_type = base_type_name
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
        result += "};\n"

        # is swizzle
        result += "template<> struct is_swizzle<{base_type}{dimension}> {{ static constexpr bool value = true; }};\n\n".format(base_type = base_type_name, dimension = i)

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
                matrix_type_name = str.format("{base_type}{row_size}x{col_size}", base_type = base_type_name, row_size = row_size, col_size = col_size)

                # begin struct 
                result += str.format("struct {matrix_name}\n{{\n", matrix_name = matrix_type_name)

                # gen default constructor 
                result += "\t// constructor\n"
                result += str.format("\t{inline_marco} {matrix_name}() noexcept : pad {{ 0 }} {{}}\n", inline_marco = config.inline_marco, matrix_name = matrix_type_name)
                result += str.format("\t{inline_marco} {matrix_name}({base_type} n) noexcept : pad {{ ", inline_marco = config.inline_marco, base_type = base_type_name, matrix_name = matrix_type_name)
                for i in range(0, row_size * col_size):
                    result += "n, "
                result = result[0:-2]
                result += " } {}\n" 

                # gen vector constructor 
                if col_size != 1:
                    param_str = ""
                    assign_str = ""

                    for row in range(0, row_size):
                        param_str += str.format("{base_type}{col_size} vec{row}, ", base_type = base_type_name, col_size = col_size, row = row)
                        for vec_idx in range(0, col_size):
                            assign_str += str.format("vec{row}[{vec_idx}], ", row = row, vec_idx = vec_idx)

                    param_str = param_str[0:-2]
                    assign_str = assign_str[0:-2]
                    result += str.format("\t{inline_marco} {matrix_name}({param_str}) : pad {{ {assign_str} }} {{}}\n"
                        , inline_marco = config.inline_marco
                        , matrix_name = matrix_type_name
                        , param_str = param_str
                        , assign_str = assign_str)

                # gen val constructor 
                param_str = ""
                assign_str = ""
                for row in range(0, row_size):
                    for col in range(0, col_size):
                        param_str += str.format("{base_type} _{row}{col}, ", base_type = base_type_name, row = row, col = col)
                        assign_str += str.format("_{row}{col}, ", row = row, col = col)
                param_str = param_str[0:-2]
                assign_str = assign_str[0:-2]

                result += str.format("\t{inline_marco} {matrix_name}({param_str}) : pad {{ {assign_str} }} {{}}\n\n"
                , inline_marco = config.inline_marco
                , matrix_name = matrix_type_name
                , param_str = param_str
                , assign_str = assign_str)

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
