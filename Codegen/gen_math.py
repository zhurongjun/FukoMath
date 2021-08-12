from typing import List
import config
import math_declare
import codegen_util as util

# gen vector ++ --
def gen_vector_increment_decrement(type_list:List[str]) -> str:
    result = ""
    
    for op in ["++", "--"]:
        for type in type_list:
            result += str.format("// {type} {op}\n", type = type, op = op)
            for dimension in range(2, 5):
                increment_code = ""
                for idx in range(0, dimension):
                    increment_code += str.format("{op}v.pad[{idx}]; ", op = op, idx = idx)

                # gen forward increment code 
                result += str.format("{inline_marco} {type}{dimension}& operator{op}({type}{dimension}& v) noexcept {{ {increment_code}return v; }}\n"
                , op = op
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , increment_code = increment_code) 

                # gen deferred increment code 
                result += str.format("{inline_marco} {type}{dimension} operator{op}({type}{dimension}& v, int) noexcept {{ {type}{dimension} old_val = v; {op}v; return old_val; }}\n"
                , op = op
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension) 
            result += "\n"

    return result

# gen vector operator + - * / % > < >= <= == != 
def gen_vector_arithmetic(type_list:List[str]) -> str:
    result = ""
    
    for type in type_list:
        # gen +-*/
        for op in ["+", "-", "*", "/"]:
            result += str.format("// {type} {op} {type}\n", type = type, op = op)
            for dimension in range(2, 5):
                # gen op code 
                op_code = str.format("lsh[0] {op} rsh[0]", op = op)
                for idx in range(1, dimension):
                    op_code += str.format(", lsh[{idx}] {op} rsh[{idx}]", idx = idx, op = op)
                
                # gen final code 
                result += str.format("{inline_marco} {type}{dimension} operator {op} (const {type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ return {type}{dimension}({op_code}); }}\n"
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , op = op
                , op_code = op_code)

        # gen % 
        result += str.format("// {type} {op} {type}\n", type = type, op = "%")
        for dimension in range(2, 5):
            op_code : str

            # gen op code 
            if type in config.floating_type_mod_list:
                op_code = "_floating_mod(lsh{idx}, rsh{idx})".format(idx = "" if dimension == 1 else "[0]")
                for idx in range(1, dimension):
                    op_code += str.format(", _floating_mod(lsh{idx}, rsh{idx})", idx = "" if dimension == 1 else "[{dimension}]".format(dimension = dimension))
            else:
                op_code = str.format("lsh[0] {op} rsh[0]", op = "%")
                for idx in range(1, dimension):
                    op_code += str.format(", lsh[{idx}] {op} rsh[{idx}]", idx = idx, op = "%")
            
            # gen final code 
            result += str.format("{inline_marco} {type}{dimension} operator {op} (const {type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ return {type}{dimension}({op_code}); }}\n"
            , inline_marco = config.inline_marco
            , type = type
            , dimension = "" if dimension == 1 else dimension
            , op = "%"
            , op_code = op_code)

        # gen compare 
        for op in [">", "<", ">=", "<=", "==", "!="]:
            result += str.format("// {type} {op} {type}\n", type = type, op = op)
            for dimension in range(2, 5):
                # gen op code 
                op_code = str.format("lsh[0] {op} rsh[0]", op = op)
                for idx in range(1, dimension):
                    op_code += str.format(", lsh[{idx}] {op} rsh[{idx}]", idx = idx, op = op)
                
                # gen final code 
                result += str.format("{inline_marco} bool{dimension} operator {op} (const {type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ return bool{dimension}({op_code}); }}\n"
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , op = op
                , op_code = op_code)

        # gen sign 
        if type in config.minus_type_list:
            for op in ["+", "-"]:
                result += str.format("// {op} {type}\n", type = type, op = op)
                for dimension in range(2, 5):
                    # gen op code 
                    op_code = str.format("{op}x[0]", op = op)
                    for idx in range(1, dimension):
                        op_code += str.format(", {op}x[{idx}]", idx = idx, op = op)
                    
                    # gen final code 
                    result += str.format("{inline_marco} {type}{dimension} operator {op} (const {type}{dimension}& x) noexcept {{ return {type}{dimension}({op_code}); }}\n"
                    , inline_marco = config.inline_marco
                    , type = type
                    , dimension = dimension
                    , op = op
                    , op_code = op_code)
        
        # gen bool not(!) 
        result += str.format("// {op} {type}\n", type = type, op = "!")
        for dimension in range(2, 5):
            # gen op code 
            op_code = str.format("{op}x[0]", op = "!")
            for idx in range(1, dimension):
                op_code += str.format(", {op}x[{idx}]", idx = idx, op = "!")
            
            # gen final code 
            result += str.format("{inline_marco} bool{dimension} operator {op} (const {type}{dimension}& x) noexcept {{ return bool{dimension}({op_code}); }}\n"
            , inline_marco = config.inline_marco
            , type = type
            , dimension = dimension
            , op = "!"
            , op_code = op_code)

    return result

# gen vector operator += -= *= /= %= 
def gen_vector_arithmetic_assign(type_list:List[str]) -> str:
    result = ""
    
    for type in type_list:
        for op in ["+", "-", "*", "/", "%"]:
            result += str.format("// {type} {op}= {type}\n", type = type, op = op)
            for dimension in range(2, 5):
                result += str.format("{inline_marco} {type}{dimension}& operator {op}= ({type}{dimension}& lsh, const {type}{dimension}& rsh) noexcept {{ lsh = lsh {op} rsh; return lsh; }}\n"
                , inline_marco = config.inline_marco
                , type = type
                , dimension = dimension
                , op = op)

    return result

# gen swizzle operator + - * / % > < >= <= == != 
def gen_swizzle_arithmetic() -> str:
    result = ""
    
    # gen +-*/
    for op in ["+", "-", "*", "/"]:
        result += str.format("// swizzle {op} vector\n", op = op)
        for dimension in range(1, 5):
            #################################################### swizzle vector ####################################################
            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format(", pLsh[{swizzle_idx}] {op} pRsh[{idx}]", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op)
            op_code = op_code[2:]

            # gen template code 
            template_code = ""
            assign_code = ""
            for idx in range(0, dimension):
                template_code += ", uint32_t {name}".format(name = util.math_swizzle_pad[idx])
                assign_code += ", {name}".format(name = util.math_swizzle_pad[idx])
            
            # gen final code 
            result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& lsh, const target_type& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code)

            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format(", pLsh[{idx}] {op} pRsh[{swizzle_idx}]", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op)
            op_code = op_code[2:]

            # gen final code 
            result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const target_type& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code)

            #################################################### swizzle scalar ####################################################
            if dimension != 1:
            # gen op code 
                op_code = ""
                for idx in range(0, dimension):
                    op_code += str.format(", pLsh[{swizzle_idx}] {op} rsh", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op)
                op_code = op_code[2:]

                # gen final code 
                result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& lsh, const base_type& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);

    return target_type({op_code}); 
}}\n'''.format(
                inline_marco = config.inline_marco
                , dimension = dimension
                , op = op
                , op_code = op_code
                , template_code = template_code
                , assign_code = assign_code)

                # gen op code 
                op_code = ""
                for idx in range(0, dimension):
                    op_code += str.format(", lsh {op} pRsh[{swizzle_idx}]", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op)
                op_code = op_code[2:]

                # gen final code 
                result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const base_type& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& rsh) noexcept 
{{ 
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
                inline_marco = config.inline_marco
                , dimension = dimension
                , op = op
                , op_code = op_code
                , template_code = template_code
                , assign_code = assign_code)

            #################################################### swizzle siwzzle ####################################################
            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format(", pLsh[{swizzle_idx}] {op} pRsh[{swizzle_idx}_r]", swizzle_idx = util.math_swizzle_pad[idx], op = op)
            op_code = op_code[2:]

            # gen template code 
            template_code_r = ""
            assign_code_r = ""
            for idx in range(0, dimension):
                template_code_r += ", uint32_t {name}_r".format(name = util.math_swizzle_pad[idx])
                assign_code_r += ", {name}_r".format(name = util.math_swizzle_pad[idx])

            # gen final code 
            result += '''template<bool has_assign, bool has_assign_r, typename base_type, typename target_type{template_code}{template_code_r}> 
{inline_marco} target_type operator {op} (const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& lsh, const Swizzle{dimension}<has_assign_r, base_type, target_type{assign_code_r}>& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code
            , template_code_r  = template_code_r
            , assign_code_r = assign_code_r)


    # gen %
    op = "%"
    result += str.format("// swizzle {op} vector\n", op = op)
    for dimension in range(1, 5):
        #################################################### swizzle vector ####################################################
        # gen op code 
        op_code = ""
        for idx in range(0, dimension):
            op_code += str.format(", _mod(pLsh[{swizzle_idx}], pRsh[{idx}])", idx = idx, swizzle_idx = util.math_swizzle_pad[idx])
        op_code = op_code[2:]

        # gen template code 
        template_code = ""
        assign_code = ""
        for idx in range(0, dimension):
            template_code += ", uint32_t {name}".format(name = util.math_swizzle_pad[idx])
            assign_code += ", {name}".format(name = util.math_swizzle_pad[idx])
        
        # gen final code 
        result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& lsh, const target_type& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
        inline_marco = config.inline_marco
        , dimension = dimension
        , op = op
        , op_code = op_code
        , template_code = template_code
        , assign_code = assign_code)

        # gen op code 
        op_code = ""
        for idx in range(0, dimension):
            op_code += str.format(", _mod(pLsh[{idx}], pRsh[{swizzle_idx}])", idx = idx, swizzle_idx = util.math_swizzle_pad[idx])
        op_code = op_code[2:]

        # gen final code 
        result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const target_type& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
        inline_marco = config.inline_marco
        , dimension = dimension
        , op = op
        , op_code = op_code
        , template_code = template_code
        , assign_code = assign_code)

        #################################################### swizzle scalar ####################################################
        if dimension != 1:
        # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format(", _mod(pLsh[{swizzle_idx}], rsh)", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op)
            op_code = op_code[2:]

            # gen final code 
            result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& lsh, const base_type& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);

    return target_type({op_code}); 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code)

            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format(", _mod(lsh, pRsh[{swizzle_idx}])", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op)
            op_code = op_code[2:]

            # gen final code 
            result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type operator {op} (const base_type& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& rsh) noexcept 
{{ 
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code)


        #################################################### swizzle swizzle ####################################################
        # gen op code 
        op_code = ""
        for idx in range(0, dimension):
            op_code += str.format(", _mod(pLsh[{swizzle_idx}], pRsh[{swizzle_idx}_r])", swizzle_idx = util.math_swizzle_pad[idx])
        op_code = op_code[2:]

        # gen template code 
        template_code_r = ""
        assign_code_r = ""
        for idx in range(0, dimension):
            template_code_r += ", uint32_t {name}_r".format(name = util.math_swizzle_pad[idx])
            assign_code_r += ", {name}_r".format(name = util.math_swizzle_pad[idx])

        # gen final code 
        result += '''template<bool has_assign, typename base_type, typename target_type{template_code}{template_code_r}> 
{inline_marco} target_type operator {op} (const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code_r}>& rsh) noexcept 
{{ 
    const base_type* pLsh = reinterpret_cast<const base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

    return target_type({op_code}); 
}}\n'''.format(
        inline_marco = config.inline_marco
        , dimension = dimension
        , op = op
        , op_code = op_code
        , template_code = template_code
        , assign_code = assign_code
        , template_code_r  = template_code_r
        , assign_code_r = assign_code_r)
    return result

# gen swizzle operator += -= *= /= %= 
def gen_swizzle_arithmetic_assign() -> str:
    result = ""
    
    # gen +-*/
    for op in ["+=", "-=", "*=", "/="]:
        result += str.format("// swizzle {op} vector\n", op = op)
        for dimension in range(1, 5):
            #################################################### swizzle vector ####################################################
            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format("\tpLsh[{swizzle_idx}] = pLsh[{swizzle_idx}] {op} pRsh[{idx}];\n", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op[:1])

            # gen template code 
            template_code = ""
            assign_code = ""
            for idx in range(0, dimension):
                template_code += ", uint32_t {name}".format(name = util.math_swizzle_pad[idx])
                assign_code += ", {name}".format(name = util.math_swizzle_pad[idx])
            
            # gen final code 
            result += '''template<typename base_type, typename target_type{template_code}> 
{inline_marco} Swizzle{dimension}<true, base_type, target_type{assign_code}>& operator {op} (Swizzle{dimension}<true, base_type, target_type{assign_code}>& lsh, const target_type& rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

{op_code}
    return lsh; 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code)

            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format("\tpLsh[{idx}] = pLsh[{idx}] {op} pRsh[{swizzle_idx}];\n", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op[:1])

            # gen final code 
            result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type& operator {op} (target_type& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

{op_code}
    return lsh; 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code)

            #################################################### swizzle scalar ####################################################
            if dimension != 1:
                # gen op code 
                op_code = ""
                for idx in range(0, dimension):
                    op_code += str.format("\tpLsh[{swizzle_idx}] = pLsh[{swizzle_idx}] {op} rsh;\n", idx = idx, swizzle_idx = util.math_swizzle_pad[idx], op = op[:1])
                
                # gen final code 
                result += '''template<typename base_type, typename target_type{template_code}> 
{inline_marco} Swizzle{dimension}<true, base_type, target_type{assign_code}>& operator {op} (Swizzle{dimension}<true, base_type, target_type{assign_code}>& lsh, const base_type rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);

{op_code}
    return lsh; 
}}\n'''.format(
                inline_marco = config.inline_marco
                , dimension = dimension
                , op = op
                , op_code = op_code
                , template_code = template_code
                , assign_code = assign_code)

            #################################################### swizzle swizzle ####################################################
            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format("\tpLsh[{swizzle_idx}] = pLsh[{swizzle_idx}] {op} pRsh[{swizzle_idx}_r];\n", swizzle_idx = util.math_swizzle_pad[idx], op = op[:1])

            # gen template code 
            template_code_r = ""
            assign_code_r = ""
            for idx in range(0, dimension):
                template_code_r += ", uint32_t {name}_r".format(name = util.math_swizzle_pad[idx])
                assign_code_r += ", {name}_r".format(name = util.math_swizzle_pad[idx])

            # gen final code 
            result += '''template<bool has_assign, typename base_type, typename target_type{template_code}{template_code_r}> 
{inline_marco} Swizzle{dimension}<true, base_type, target_type{assign_code}>& operator {op} (Swizzle{dimension}<true, base_type, target_type{assign_code}>& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code_r}>& rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

{op_code}
    return lsh; 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code
            , template_code_r  = template_code_r
            , assign_code_r = assign_code_r)


    # gen %=
    op = "%="
    result += str.format("// swizzle {op} vector\n", op = op)
    for dimension in range(1, 5):
        #################################################### swizzle vector ####################################################
        # gen op code 
        op_code = ""
        for idx in range(0, dimension):
            op_code += str.format("\tpLsh[{swizzle_idx}] = _mod(pLsh[{swizzle_idx}], pRsh[{idx}]);\n", idx = idx, swizzle_idx = util.math_swizzle_pad[idx])

        # gen template code 
        template_code = ""
        assign_code = ""
        for idx in range(0, dimension):
            template_code += ", uint32_t {name}".format(name = util.math_swizzle_pad[idx])
            assign_code += ", {name}".format(name = util.math_swizzle_pad[idx])
        
        # gen final code 
        result += '''template<typename base_type, typename target_type{template_code}> 
{inline_marco} Swizzle{dimension}<true, base_type, target_type{assign_code}>& operator {op} (Swizzle{dimension}<true, base_type, target_type{assign_code}>& lsh, const target_type& rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

{op_code}
    return lsh; 
}}\n'''.format(
        inline_marco = config.inline_marco
        , dimension = dimension
        , op = op
        , op_code = op_code
        , template_code = template_code
        , assign_code = assign_code)

         # gen op code 
        op_code = ""
        for idx in range(0, dimension):
            op_code += str.format("\tpLsh[{idx}] = _mod(pLsh[{idx}], pRsh[{swizzle_idx}]);\n", idx = idx, swizzle_idx = util.math_swizzle_pad[idx])

        # gen final code 
        result += '''template<bool has_assign, typename base_type, typename target_type{template_code}> 
{inline_marco} target_type& operator {op} (target_type& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code}>& rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

{op_code}
    return lsh; 
}}\n'''.format(
        inline_marco = config.inline_marco
        , dimension = dimension
        , op = op
        , op_code = op_code
        , template_code = template_code
        , assign_code = assign_code)

        #################################################### swizzle scalar ####################################################
        if dimension != 1:
            # gen op code 
            op_code = ""
            for idx in range(0, dimension):
                op_code += str.format("\tpLsh[{swizzle_idx}] = _mod(pLsh[{swizzle_idx}], rsh);\n", idx = idx, swizzle_idx = util.math_swizzle_pad[idx])

            # gen template code 
            template_code = ""
            assign_code = ""
            for idx in range(0, dimension):
                template_code += ", uint32_t {name}".format(name = util.math_swizzle_pad[idx])
                assign_code += ", {name}".format(name = util.math_swizzle_pad[idx])
            
            # gen final code 
            result += '''template<typename base_type, typename target_type{template_code}> 
{inline_marco} Swizzle{dimension}<true, base_type, target_type{assign_code}>& operator {op} (Swizzle{dimension}<true, base_type, target_type{assign_code}>& lsh, const base_type rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);

{op_code}
    return lsh; 
}}\n'''.format(
            inline_marco = config.inline_marco
            , dimension = dimension
            , op = op
            , op_code = op_code
            , template_code = template_code
            , assign_code = assign_code)

        #################################################### swizzle swizzle ####################################################
        # gen op code 
        op_code = ""
        for idx in range(0, dimension):
            op_code += str.format("\tpLsh[{swizzle_idx}] = _mod(pLsh[{swizzle_idx}], pRsh[{swizzle_idx}_r]);\n", swizzle_idx = util.math_swizzle_pad[idx])

        # gen template code 
        template_code_r = ""
        assign_code_r = ""
        for idx in range(0, dimension):
            template_code_r += ", uint32_t {name}_r".format(name = util.math_swizzle_pad[idx])
            assign_code_r += ", {name}_r".format(name = util.math_swizzle_pad[idx])

        # gen final code 
        result += '''template<bool has_assign, typename base_type, typename target_type{template_code}{template_code_r}> 
{inline_marco} Swizzle{dimension}<true, base_type, target_type{assign_code}>& operator {op} (Swizzle{dimension}<true, base_type, target_type{assign_code}>& lsh, const Swizzle{dimension}<has_assign, base_type, target_type{assign_code_r}>& rsh) noexcept 
{{ 
    base_type* pLsh = reinterpret_cast<base_type*>(&lsh);
    const base_type* pRsh = reinterpret_cast<const base_type*>(&rsh);

{op_code}
    return lsh; 
}}\n'''.format(
        inline_marco = config.inline_marco
        , dimension = dimension
        , op = op
        , op_code = op_code
        , template_code = template_code
        , assign_code = assign_code
        , template_code_r  = template_code_r
        , assign_code_r = assign_code_r)
    return result

# gen vector math for per type 
def gen_vertor_math(base_type:str) -> str:
    result = ""

    for k,v in math_declare.vector_declares.__dict__.items():
        # check support function 
        if type(v) == tuple and base_type in v[0]:
            fun_name = str(k) if k[0:2] != "m_" else k[2:]
            result += "// {fun_name} \n".format(fun_name = fun_name)
            
            # get attr 
            if hasattr(math_declare.vector_declares, "gen_" + fun_name):
                f = getattr(math_declare.vector_declares, "gen_" + fun_name)
                
                # each dimension 
                for dimension in range(1, 5):
                    if dimension in v[1]:
                        result += f(base_type, dimension)
            result += "\n"

    return result

# gen matrix math for per type 
def gen_matrix_math(base_type:str) -> str:
    result = ""

    for k,v in math_declare.matrix_declares.__dict__.items():
        # check support function 
        if type(v) == tuple and base_type in v[0]:
            fun_name = str(k) if k[0:2] != "m_" else k[2:]
            result += "// {fun_name} \n".format(fun_name = fun_name)
            
            # get attr 
            if hasattr(math_declare.matrix_declares, "gen_" + fun_name):
                f = getattr(math_declare.matrix_declares, "gen_" + fun_name)
                
                # each matrix dimension 
                for row_size in range(1, 5):
                    for col_size in range(1,5):
                        if v[1](row_size, col_size):
                            result += f(base_type, row_size, col_size)
            result += "\n"

    return result