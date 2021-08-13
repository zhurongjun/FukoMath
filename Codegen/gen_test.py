from typing import List
import config
import gen_swizzle
import codegen_util as util

def gen_vector_test(type_list:List[str]) -> str:
    result = ""
    # begin function 
    result += "void test_vector()\n{{\n\tusing namespace {math_namespace};\n".format(math_namespace = config.math_namespace)

    # build test code 
    for type in type_list:
        result += "\t// {type} test\n\t{{\n".format(type = type)

        # basic var 
        for dimension in range(1, 5):
            result += "\t\t{base_type}{type_dimension} va{dimension} = 4, vb{dimension} = 99999;\n".format(
                base_type = type
                , type_dimension = "" if dimension == 1 else dimension
                , dimension = dimension
            )

        # test swizzle 
        for dimension in range(2, 5):
            comp : List[int] = []
            all_case : List[gen_swizzle.case_info] = []
            for target_dimension in range(1, 5):
                comp.clear()
                all_case.clear()
                gen_swizzle.recursive_gen_components(target_dimension, dimension, comp, all_case)
                for case in all_case:
                    has_assign = gen_swizzle.has_assign(case.components, dimension)
                    
                    swizzle_code = ""
                    for cp in case.components:
                        swizzle_code += util.math_swizzle_pad[cp]
                    
                    if has_assign:
                        result += "\t\tva{dimension}.{swizzle_code} = vb{dimension}.{swizzle_code};\n".format(dimension = dimension, swizzle_code = swizzle_code)
                        result += "\t\tva{dimension}.{swizzle_code} = vb1;\n".format(dimension = dimension, swizzle_code = swizzle_code)
                        if type in config.all_num_types:
                            for op in ["+", "-", "*", "/", "%"]:
                                result += "\t\tva{dimension}.{swizzle_code} {op} vb{dimension}.{swizzle_code};\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op, target_dimension = target_dimension)
                                result += "\t\tva{dimension}.{swizzle_code} {op} vb1;\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op, target_dimension = target_dimension)

                            for op in ["+", "-"]:
                                result += "\t\t{op}vb{dimension}.{swizzle_code};\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op, target_dimension = target_dimension)
                                
                            if target_dimension <= 2:
                                for op in ["+=", "-=", "*=", "/=", "%="]:
                                    result += "\t\tva{dimension}.{swizzle_code} {op} vb{dimension}.{swizzle_code};\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op)
                                    result += "\t\tva{dimension}.{swizzle_code} {op} vb1;\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op)
                    else:
                        
                        if type in config.all_num_types:
                            '''
                            for op in ["+", "-", "*", "/", "%"]:
                                result += "\t\tva{dimension}.{swizzle_code} {op} vb{dimension}.{swizzle_code};\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op, target_dimension = target_dimension)
                                result += "\t\tva{dimension}.{swizzle_code} {op} vb1;\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op, target_dimension = target_dimension)

                            for op in ["+", "-"]:
                                result += "\t\t{op}vb{dimension}.{swizzle_code};\n".format(dimension = dimension, swizzle_code = swizzle_code, op = op, target_dimension = target_dimension)
                            '''
                        result += "\t\tvb{target_dimension} = va{dimension}.{swizzle_code};\n".format(dimension = dimension, swizzle_code = swizzle_code, target_dimension = target_dimension)


        result += "\n\t}\n"

    # end function 
    result += "\n}"

    return result

def gen_matrix_test(type_list:List[str]) -> str:
    result = ""
    # begin function 
    result += "void test_matrix()\n{\n"

    # buidl test code 
    result += '''\n\tstd::cout << "test_matrix" << std::endl;'''

    # end function 
    result += "\n}"
    
    return result

def gen_math_test(type_list:List[str]) -> str:
    result = ""
    # begin function 
    result += "void test_math()\n{\n"

    # buidl test code 
    result += '''\n\tstd::cout << "test_math" << std::endl;'''

    # end function 
    result += "\n}"
    
    return result

def gen_exec_test() -> str:
    return'''#include <iostream>
#include "fuko_math.h"
#include "test_vector.h"
#include "test_matrix.h"
#include "test_math.h"

int main()
{
    test_vector();
    test_matrix();
    test_math();

	std::cout << "shit world" << std::endl;
	return 0;
}    
'''