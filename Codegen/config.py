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
implicit_convert_dic =  { "float":  ["double"]
                        , "double": []
                        , "int":    ["double", "float", "uint"]
                        , "uint":   ["double", "float"]
                        , "bool":   ["double", "float", "int", "uint"] }
floating_type_mod_list = ["float", "double"]

# enviroment 
enable_namespace = True
math_namespace = "fuko::math"
inline_marco = "FORCEINLINE"
enable_matrix_swizzle = False

# math 
all_num_types = ["float", "double", "int", "uint"]
all_floating_types = ["float", "double"]
all_integer_types = ["int", "uint"]
all_types = ["float", "double", "int", "uint", "bool"]