from typing import List

# math info type 
class math_method_info:
    def __init__(self, template:str, support_types:List[str]) -> None:
        self.template = template
        self.support_types = support_types
        return

# templates 
swizzle_template_path = "./Templates/swizzle.h"
forward_file_template_path = "./Templates/fuko_math_forward.h"
deferred_file_template_path = "./Templates/fuko_math_deferred.h"

# vector & matrix codegen types  
vector_type_list = ["float", "double", "int", "uint", "bool"]
matrix_type_list = ["float", "double", "int", "uint"]

# enviroment 
math_namespace = "fuko::math"
inline_marco = "FORCEINLINE"
enable_namespace = True

# math 