from typing import List
import gen_swizzle
import gen_type
import config
import shutil
import sys
import codegen_util as util
from pathlib import Path

# paths 
codgen_root_dir = Path(__file__).parent
project_root_dir = codgen_root_dir.parent
cpp_root_dir = project_root_dir / "FukoMath"
swizzle_dir =   cpp_root_dir / "Swizzle"
types_dir =     cpp_root_dir / "Types"
math_dir =      cpp_root_dir / "Math"
make_script_path = project_root_dir / "premake.lua"
forward_file_path = cpp_root_dir / "fuko_math_forward.h"
deferred_file_path = cpp_root_dir / "fuko_math_deferred.h"

# lists 
full_type_list = set(config.vector_type_list).union(config.matrix_type_list)

def begin_namespace() -> str:
    return str.format("namespace {math_namespace}\n{{\n", math_namespace = config.math_namespace)

def end_namespace() -> str:
    return "}"

if __name__ == "__main__" :
    # clean up dir 
    if cpp_root_dir.exists():
        shutil.rmtree(cpp_root_dir)
    if make_script_path.exists():
        make_script_path.unlink()

    # clean up option 
    if "cleanup" in sys.argv:
        workspace_dir =  project_root_dir / "workspace"
        if workspace_dir.exists():
            shutil.rmtree(workspace_dir)
        exit()

    # gen dir 
    swizzle_dir.mkdir(parents=True)
    types_dir.mkdir(parents=True)
    math_dir.mkdir(parents=True)

    # copy swizzle.h 
    swizzle_template_path = codgen_root_dir / config.swizzle_template_path
    if swizzle_template_path.exists():
        shutil.copyfile(str(swizzle_template_path), str(swizzle_dir / "swizzle.h"))
    else:
        print("lost swizzle template file\n")
        exit()

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
    for type in full_type_list:
        implicit_types = config.vector_type_list.copy()
        implicit_types.remove(type)

        # write file 
        with (types_dir / (type + ".h")).open("w+") as f:
            f.write('''#pragma once\n#include "../fuko_math_forward.h"\n\n''')
            
            # end namespace 
            if config.enable_namespace:
                f.write(begin_namespace())
            
            # gen vector codes 
            if type in config.vector_type_list:
                f.write(gen_type.gen_type_code_vector(type, implicit_types))

            # gen matrix types
            if type in config.matrix_type_list:
                f.write(gen_type.gen_type_code_matrix(type))

            # begin namespace 
            if config.enable_namespace:
                f.write(end_namespace())
    
    # gen dependencies 
    dependencies_file_path = cpp_root_dir / "fuko_math_dependencies.h"
    with dependencies_file_path.open("w+") as f:
        pass

    # gen deferred file 
    deferred_template_file_path = codgen_root_dir / config.deferred_file_template_path
    if deferred_template_file_path.exists():
            deferred_template : str 

            # read template 
            with deferred_template_file_path.open() as f:
                deferred_template = f.read()
            
            # write 
            with deferred_file_path.open("w+") as f:
                pass
    else:
        print("lost deferred template file\n")
        exit()

    # gen math 
    for type in full_type_list :
        math_file_path = math_dir / str.format("{base_type}_math.h", base_type = type)
        with  math_file_path.open("w+") as f:
            if type in config.vector_type_list:
                pass
            if type in config.matrix_type_list:
                pass
    
    # gen makescript 
    make_script_template_path = codgen_root_dir / config.make_script_template_path
    if make_script_template_path.exists():
        make_script_template : str 
       
        # read template 
        with make_script_template_path.open() as f:
            make_script_template = f.read()

        # write 
        with make_script_path.open("w+") as f:
            f.write(make_script_template)
    else:
        print("lost make script template file\n")
        exit()
