from typing import List

def gen_vector_test(type_list:List[str]) -> str:
    result = ""
    # begin function 
    result += "void test_vector()\n{"

    # buidl test code 
    result += '''\tstd::cout << "test_vector" << std::endl;'''

    # end function 
    result += "\n}"

    return result

def gen_matrix_test(type_list:List[str]) -> str:
    result = ""
    # begin function 
    result += "void test_matrix()\n{"

    # buidl test code 
    result += '''\tstd::cout << "test_matrix" << std::endl;'''

    # end function 
    result += "\n}"
    
    return result

def gen_math_test(type_list:List[str]) -> str:
    result = ""
    # begin function 
    result += "void test_math()\n{"

    # buidl test code 
    result += '''\tstd::cout << "test_math" << std::endl;'''

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