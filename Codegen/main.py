from typing import List
import gen_swizzle
import gen_type
import config
import shutil
import codegen_util as util
from pathlib import Path

root_dir = Path(__file__).parent
swizzle_dir = root_dir.parent / "FukoMath" / "Swizzle"
types_dir = root_dir.parent / "FukoMath" / "Types"
math_dir = root_dir.parent / "FukoMath" / "Math"


if __name__ == "__main__" :
    # check dir 
    if swizzle_dir.exists() == False:
        swizzle_dir.mkdir(parents=True)
    if types_dir.exists() == False:
        types_dir.mkdir(parents=True)
    if math_dir.exists() == False:
        math_dir.mkdir(parents=True)

    # copy swizzle.h 
    swizzle_template_path = root_dir / config.swizzle_template_path
    shutil.copyfile(str(swizzle_template_path), str(swizzle_dir / "swizle.h"))

    # gen vector swizzle 
    for src_size in range(2, 5):
        f = (swizzle_dir / str.format("swizzle{size}", size = src_size)).open("w+")
        f.write('#include "swizzle.h"')
        f.write(gen_swizzle.gen_swizzle_code_vector(src_size))
        f.close()

    # gen matrix swizzle 
    for row_size in range(1, 5):
        for col_size in range(1, 5):
            if row_size != 1 or col_size != 1:
                f = (swizzle_dir / str.format("swizzle{row}x{col}", row = row_size, col = col_size)).open("w+")
                f.write('#include "swizzle.h"')
                f.write(gen_swizzle.gen_swizzle_code_matrix(row_size, col_size))
                f.close()

    # gen common file  

    # gen vector types 
    for type in config.vector_type_list:
        f = (types_dir / (type + ".h")).open("w+")
        implicit_types = config.vector_type_list.copy()
        implicit_types.remove(type)
        f.write(gen_type.gen_type_code(type, implicit_types))
        f.close()

    # gen vector convert 

    # gen matrix types 

    # gen math 
    