from typing import List

# templates 
swizzle_template_path = "./Templates/swizzle.h"
forward_file_template_path = "./Templates/fuko_math_forward.h"
deferred_file_template_path = "./Templates/fuko_math_deferred.h"
make_script_template_path = "./Templates/premake.lua"

# vector & matrix codegen types  
vector_type_list = ["float", "double", "int", "uint", "bool"]
matrix_type_list = ["float", "double", "int", "uint"]
asxxx_type_list = ["float", "int", "uint"]
arithmetic_type_list = ["float", "double", "int", "uint"]
implicit_convert_dic =  { "float":  ["double", "bool"]
                        , "double": ["bool"]
                        , "int":    ["double", "float", "bool", "uint"]
                        , "uint":   ["double", "float", "bool"]
                        , "bool":   ["double", "float", "int", "uint"] }
floating_type_mode_list = ["float", "double"]

# enviroment 
enable_namespace = True
math_namespace = "fuko::math"
inline_marco = "FORCEINLINE"
enable_matrix_swizzle = False

# math 