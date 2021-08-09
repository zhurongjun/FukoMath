from typing import List
import gen_swizzle
import gen_type
import config
import shutil
import sys
import codegen_util as util
from pathlib import Path

codgen_root_dir = Path(__file__).parent
project_root_dir = codgen_root_dir.parent
cpp_root_dir = project_root_dir / "FukoMath"
swizzle_dir =   cpp_root_dir / "Swizzle"
types_dir =     cpp_root_dir / "Types"
math_dir =      cpp_root_dir / "Math"

def begin_namespace() -> str:
    return str.format("namespace {math_namespace}\n{{\n", math_namespace = config.math_namespace)

def end_namespace() -> str:
    return "}"


if __name__ == "__main__" :
    # clean up dir 
    if cpp_root_dir.exists():
        shutil.rmtree(cpp_root_dir)

    # clean up option 
    if "cleanup" in sys.argv:
        exit()

    # gen dir 
    swizzle_dir.mkdir(parents=True)
    types_dir.mkdir(parents=True)
    math_dir.mkdir(parents=True)

    # copy swizzle.h 
    swizzle_template_path = codgen_root_dir / config.swizzle_template_path
    shutil.copyfile(str(swizzle_template_path), str(swizzle_dir / "swizle.h"))

    # gen vector swizzle 
    for src_size in range(2, 5):
        with (swizzle_dir / str.format("swizzle{size}", size = src_size)).open("w+") as f:
            f.write('#include "swizzle.h"')
            f.write(gen_swizzle.gen_swizzle_code_vector(src_size))

    # gen matrix swizzle 
    if config.enable_matrix_swizzle:
        for row_size in range(1, 5):
            for col_size in range(1, 5):
                if row_size != 1 or col_size != 1:
                    with (swizzle_dir / str.format("swizzle{row}x{col}", row = row_size, col = col_size)).open("w+") as f:
                        f.write('#include "swizzle.h"')
                        f.write(gen_swizzle.gen_swizzle_code_matrix(row_size, col_size))

    # gen forward file 
    forward_file_path = cpp_root_dir / "fuko_math_forward.h"
    forward_template_file_path = codgen_root_dir / config.forward_file_template_path
    if forward_template_file_path.exists():
        forward_template : str 

        # read template 
        with forward_template_file_path.open() as f:
            forward_template = f.read()
        
        # write 
        with forward_file_path.open("w+") as f:
            f.write(str.format(forward_template, 
            forward_declares = gen_type.gen_forward_declare_vector(config.vector_type_list) 
            + gen_type.gen_forward_declare_matrix(config.matrix_type_list)))
    else:
        print("lost forward template file\n")
        exit()
    
    # gen type codes  
    for type in config.vector_type_list:
        implicit_types = config.vector_type_list.copy()
        implicit_types.remove(type)

        # write file 
        with (types_dir / (type + ".h")).open("w+") as f:
            f.write('''#pragma once\n#include "../fuko_math_forward.h"\n\n''')
            
            # end namespace 
            if config.enable_namespace:
                f.write(begin_namespace())
            
            # gen vector codes 
            f.write(gen_type.gen_type_code_vector(type, implicit_types))

            # gen matrix types
            f.write(gen_type.gen_type_code_matrix(type))

            # begin namespace 
            if config.enable_namespace:
                f.write(end_namespace())
    
    # gen dependencies 
    dependencies_file_path = cpp_root_dir / "fuko_math_dependencies.h"
    with dependencies_file_path.open("w+") as f:
        pass

    # gen deferred file 

    # gen math 
    