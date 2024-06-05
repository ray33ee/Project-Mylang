import ast
import symtable

import custom_nodes
import custom_unparser
import errors
import ir
import sugar
import symbol_table
import mangler
import m_types
from collections import OrderedDict

import deduction


def analysis(source):
    # Create a python AST from the source code
    my_ast = ast.parse(source, mode='exec')

    # Create a python symtable from the source code
    table = symtable.symtable(source, "", compile_type="exec")

    # Convert certain operations in to their syntactic sugar equivalent
    sugar.sugar(my_ast)

    print("##################################")
    print("Abstract Syntax Tree")
    print("##################################")

    print(ast.dump(my_ast, indent=4))

    print("##################################")
    print("Unparsed content")
    print("##################################")

    print(custom_unparser.unparse(my_ast))

    print("##################################")
    print("Symbol Table")
    print("##################################")

    # Get the Mylang AST
    t = symbol_table.Table(my_ast, table)
    print(t)

    print("##################################")
    print("Mangler and Demangler tests")
    print("##################################")

    mangler.run_mangler_tests()

    print("##################################")
    print("Deduce types")
    print("##################################")

    d = deduction.deduce(t)

    print(d)
    print(d.symbol_map)


