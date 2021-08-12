import gen_test
from types import FunctionType
from typing import List
import gen_swizzle
import gen_type
import gen_math
import gen_dependency
import config
import shutil
import sys
import codegen_util as util
from pathlib import Path

# paths 
codgen_root_dir = Path(__file__).parent
project_root_dir = codgen_root_dir.parent
cpp_root_dir = project_root_dir / "FukoMath"
test_root_dir = project_root_dir / "FukoTest"
swizzle_dir =   cpp_root_dir / "Swizzle"
types_dir =     cpp_root_dir / "Types"
math_dir =      cpp_root_dir / "Math"

# file paths 
make_script_path = project_root_dir / "premake.lua"
forward_file_path = cpp_root_dir / "fuko_math_forward.h"
deferred_file_path = cpp_root_dir / "fuko_math_deferred.h"
facade_file_path = cpp_root_dir / "fuko_math.h"
dependencies_file_path = cpp_root_dir / "fuko_math_dependencies.h"

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
    if test_root_dir.exists():
        shutil.rmtree(test_root_dir)
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
    test_root_dir.mkdir(parents=True)

    # copy swizzle.h 
    swizzle_template_path = codgen_root_dir / config.swizzle_template_path
    if swizzle_template_path.exists():
        swizzle_template : str
        with swizzle_template_path.open() as f:
            swizzle_template = f.read()
        with (swizzle_dir / "swizzle.h").open("w+") as f:
            f.write(swizzle_template.format(
                inline_marco = config.inline_marco
                , math_namespace = config.math_namespace))
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
            f.write(str.format(forward_template
            , forward_declares = gen_type.gen_forward_declare_vector(config.vector_type_list) 
            + gen_type.gen_forward_declare_matrix(config.matrix_type_list)
            , math_namespace = config.math_namespace))
    else:
        print("lost forward template file\n")
        exit()
    
    # gen type codes  
    for type in full_type_list:
        implicit_types = config.vector_type_list.copy()
        implicit_types.remove(type)

        # write file 
        with (types_dir / (type + ".h")).open("w+") as f:
            f.write('''#pragma once\n#include "../fuko_math_forward.h"\n#include "../Swizzle/swizzle.h"\n\n''')
            
            # begin namespace 
            if config.enable_namespace:
                f.write(begin_namespace())
            
            # gen vector codes 
            if type in config.vector_type_list:
                f.write(gen_type.gen_type_code_vector(type, implicit_types))

            # gen matrix types
            if type in config.matrix_type_list:
                f.write(gen_type.gen_type_code_matrix(type))

            # end namespace 
            if config.enable_namespace:
                f.write(end_namespace())
    
    # gen dependencies 
    with dependencies_file_path.open("w+") as f:
        # add pragma and forward 
        f.write('''#pragma once\n#include "fuko_math_forward.h"\n''')
        
        # add type include 
        for type in config.vector_type_list:
            f.write(str.format('''#include "Types/{type}.h"\n''', type = type))
        f.write("\n")

        # begin namespace 
        if config.enable_namespace:
            f.write(begin_namespace())

        # implicit convertions 
        f.write(gen_dependency.gen_implicit_conversion(config.vector_type_list))

        # asxxx convertions 
        f.write(gen_dependency.gen_asxxx_conversion(config.asxxx_type_list))

        # end namespace 
        if config.enable_namespace:
            f.write(end_namespace())

    # gen deferred file 
    deferred_template_file_path = codgen_root_dir / config.deferred_file_template_path
    if deferred_template_file_path.exists():
            deferred_template : str 

            # read template 
            with deferred_template_file_path.open() as f:
                deferred_template = f.read()
            
            # write 
            with deferred_file_path.open("w+") as f:
                f.write(deferred_template.format(
                    inline_marco = config.inline_marco
                    , math_namespace = config.math_namespace
                ))
    else:
        print("lost deferred template file\n")
        exit()

    # gen util math 
    with (math_dir/ "util_math.h").open("w+") as f:
        # add pragma and forward 
        f.write('''#pragma once\n#include "fuko_math_forward.h"\n''')
        
        # add type include 
        for type in config.vector_type_list:
            f.write(str.format('''#include "Types/{type}.h"\n''', type = type))
        f.write("\n")

        # begin namespace 
        if config.enable_namespace:
            f.write(begin_namespace())
        
        # increment & decrement 
        f.write(gen_math.gen_vector_increment_decrement(config.arithmetic_type_list))

        # arithmetic 
        f.write(gen_math.gen_vector_arithmetic(config.arithmetic_type_list))

        # arithmetic assign 
        f.write(gen_math.gen_vector_arithmetic_assign(config.arithmetic_type_list))

        # swizzle arithmetic 
        f.write(gen_math.gen_swizzle_arithmetic())

        # swizzle arithmetic assign 
        f.write(gen_math.gen_swizzle_arithmetic_assign())

        # end namespace 
        if config.enable_namespace:
            f.write(end_namespace())

    # gen per type math 
    for type in full_type_list :
        math_file_path = math_dir / str.format("{base_type}_math.h", base_type = type)
        with  math_file_path.open("w+") as f:
            # add pragma and forward 
            f.write('''#pragma once\n#include <cmath>\n#include <algorithm>\n#include "util_math.h"\n#include "../fuko_math_forward.h"\n''')

            # add type include 
            f.write(str.format('''#include "../Types/{type}.h"\n\n''', type = type))

            # begin namespace 
            if config.enable_namespace:
                f.write(begin_namespace())

            # gen code 
            if type in config.vector_type_list:
                f.write(gen_math.gen_vertor_math(type))
            if type in config.matrix_type_list:
                f.write(gen_math.gen_matrix_math(type))

            # end namespace 
            if config.enable_namespace:
                f.write(end_namespace())
    
    # gen facade file 
    facade_file_template_path = codgen_root_dir / config.facade_file_template_path
    if facade_file_template_path.exists():
        facade_file_template : str 

        # read template 
        with facade_file_template_path.open() as f:
            facade_file_template = f.read()

        # gen includes 
        type_includes = ""
        math_includes = '''#include "Math/util_math.h"\n'''

        for type in full_type_list:
            type_includes += '''#include "Types/{type}.h"\n'''.format(type = type)
            math_includes += '''#include "Math/{type}_math.h"\n'''.format(type = type)

        # write 
        with facade_file_path.open("w+") as f:
            f.write(facade_file_template.format(
                type_includes = type_includes
                , math_includes = math_includes))
    else:
        print("lost facade file template file\n")
        exit()

    # gen testscript 
    test_vector_path = test_root_dir / "test_vector.h"
    test_matrix_path = test_root_dir / "test_matrix.h"
    test_math_path = test_root_dir / "test_math.h"
    test_exec_path = test_root_dir / "main.cpp"
    with test_vector_path.open("w+") as f:
        f.write('''#pragma once
#include "fuko_math.h"\n\n''')
        f.write(gen_test.gen_vector_test(config.vector_type_list))
    with test_matrix_path.open("w+") as f:
        f.write('''#pragma once
#include "fuko_math.h"\n\n''')
        f.write(gen_test.gen_matrix_test(config.matrix_type_list))
    with test_math_path.open("w+") as f:
        f.write('''#pragma once
#include "fuko_math.h"\n\n''')
        f.write(gen_test.gen_math_test(full_type_list))
    with test_exec_path.open("w+") as f:
        f.write(gen_test.gen_exec_test())

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
