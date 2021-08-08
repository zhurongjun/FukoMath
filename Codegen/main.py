from typing import List
import gen_swizzle
import gen_type
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

    # write swizzle.h 
    f = (swizzle_dir / "swizzle.h").open("w+")
    f.write(util.swizzle_template)
    f.close()

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

    # gen vector types 
    f = (types_dir / "float.h").open("w+")
    f.write(gen_type.gen_type_code("float"))
    f.close()


