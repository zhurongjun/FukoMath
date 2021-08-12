from typing import List
import codegen_util as util

# swizzle case info 
class case_info:
    def __init__(self, has_assign:bool, components:List[int]) -> None:
        self.has_assign = has_assign
        self.components = components
        return

# check if has assign 
def has_assign(comp:List[int], base_type_len:int) -> bool:
    check_pad = [False] * base_type_len
    for i in comp:
        if check_pad[i] == True:
            return False
        check_pad[i] = True
    return True

# recusive gen swizzle component cases 
def recursive_gen_components(len:int, case_count:int, comp:List[int], all_cases:List[case_info]) -> None:
    if (len == 1):
        # gen code 
        for i in range(0, case_count):
            comp.append(i)
            all_cases.append(case_info(False, comp.copy()))
            comp.pop()
    else:
        # recursive 
        for i in range(0, case_count):
            comp.append(i)
            recursive_gen_components(len - 1, case_count, comp, all_cases)
            comp.pop()
    return

# gen code for single swizzle case 
def gen_swizzle_case_code(cur_case:case_info, swizzle_pad:list) -> str:
    # basic template str 
    template_str = "Swizzle{case_count}<{has_assign}, {type_marco}, "

    # out type 
    template_str += "{combine_marco}({type_marco}, {case_count})" if len(cur_case.components) > 1 else "{type_marco}"

    # component index 
    for i in cur_case.components:
        template_str += ", " + str(i)

    # end template 
    template_str += "> "

    # member name 
    for i in cur_case.components:
        template_str += swizzle_pad[i] 
    
    # end member 
    template_str += ";"
    
    # fill template 
    return template_str.format(has_assign = "true" if cur_case.has_assign else "false"
        , type_marco = util.swizzle_type_marco
        , combine_marco = util.swizzle_combine_marco
        , case_count = len(cur_case.components))

# gen code for single vector 
def gen_swizzle_code_vector(vector_size:int) -> str:
    # init global data 
    result_str = util.define_combine_marco + "\n\n"
    all_cases : List[case_info] = []
    temp_comps : List[int] = []

    # loop for swizzle output code 
    for swizzle_size in range(1, 5):
        result_str += str.format("// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!swizzle{vector_size}_{out_size}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n"
        , vector_size = vector_size
        , out_size = swizzle_size)

        # gen cases 
        all_cases.clear()
        recursive_gen_components(swizzle_size, vector_size, temp_comps, all_cases)

        # check assign 
        for case in all_cases:
            case.has_assign = has_assign(case.components, vector_size)

        # gen math code 
        for case in all_cases:
            result_str += gen_swizzle_case_code(case, util.math_swizzle_pad) + "\n"

        result_str += "// ================================================color code================================================\n"

        # gen color code 
        for case in all_cases:
            result_str += gen_swizzle_case_code(case, util.color_swizzle_pad) + "\n"

        result_str += "\n\n"
    
    # undefine combine marco  
    result_str += util.undefine_combine_marco

    return result_str

# gen code for matrix 
def gen_swizzle_code_matrix(row_size:int, col_size:int) ->str:
    # init pad 
    matrix_pad_from_zero : List[str] = []
    matrix_pad_from_one : List[str] = []
    for row in range(0, row_size):
        for col in range(0, col_size):
            matrix_pad_from_zero.append(str.format("_m{row_count}{col_count}", row_count = row, col_count = col))
            matrix_pad_from_one.append(str.format("_{row_count}{col_count}", row_count = row + 1, col_count = col + 1))

    # init global data 
    result_str = util.define_combine_marco + "\n\n"
    all_cases : List[case_info] = []
    temp_comps : List[int] = []
    matrix_size = row_size * col_size;

    # loop for swizzle output code 
    for swizzle_size in range(1, 5):
        result_str += str.format("// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!swizzle{row_size}x{col_size}_{out_size}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n"
        , row_size = row_size
        , col_size = col_size
        , out_size = swizzle_size)

        # gen cases 
        all_cases.clear()
        recursive_gen_components(swizzle_size, matrix_size, temp_comps, all_cases)

        # check assign 
        for case in all_cases:
            case.has_assign = has_assign(case.components, matrix_size)

        # gen from zero code 
        for case in all_cases:
            result_str += gen_swizzle_case_code(case, matrix_pad_from_zero) + "\n"

        result_str += "// ================================================from one================================================\n"

        # gen from one code 
        for case in all_cases:
            result_str += gen_swizzle_case_code(case, matrix_pad_from_one) + "\n"

        result_str += "\n\n"

    # undefine combine marco  
    result_str += util.undefine_combine_marco

    return result_str
