import ast
import symtable

import custom_nodes
import custom_unparser
import deduction
import errors
import sugar_v
import symbol_table
import mangler
import m_types
from collections import OrderedDict

import translator
from requirements import resolve_function


# A special function that iterates over all functions in a source. This will iterate over global functions and
# member functions. Each iteration returns a (parent, node) pair. If the function is a class member function, the node
# is the class member function and the parent is the class. If the function is a global function, the node is the global
# function and the parent is None.
def function_iterator(_ast: ast.Module):
    for node in _ast.body:
        if type(node) is ast.FunctionDef:
            yield None, node
        if type(node) is ast.ClassDef:
            for member_function in filter(lambda n : type(n) is ast.FunctionDef, node.body):
                yield node, member_function


# Recursively display the contents of a symbol table
def recursive_show(table: symtable.SymbolTable, level):
    nest = '\t' * level

    for symbol in table.get_symbols():
        print(f"{nest} symbol {symbol.get_name()} ({type(symbol)}) local: {symbol.is_local()}")

    for child in table.get_children():
        t = child.get_parameters() if type(child) is symtable.Function else ""
        print(f"{nest} {child.get_type()} {child.get_name()} {t}")
        recursive_show(child, level+1)



def analysis(source):
    my_ast = ast.parse(source, mode='exec')
    table = symtable.symtable(source, "", compile_type="exec")

    # Convert certain operations in to their syntactic sugar equivalent
    sugar_v.sugar(my_ast)

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
    t = symbol_table.Table(my_ast, table)
    print(t)
    print("Symbol table stuff is broken atm come back later")

    print("##################################")
    print("Mangler and Demangler tests")
    print("##################################")

    bodies = [
        mangler.Function([m_types.Integer(), mangler.Class([m_types.Boolean()], mangler.Name("s"))]),

        mangler.Function([m_types.Char(), mangler.Class([m_types.Boolean()], mangler.Name("s"))]),

        mangler.Class([mangler.Class([m_types.Boolean()], mangler.Name("s")),
                       mangler.Class([m_types.Integer()], mangler.Name("t"))]),

        mangler.Function([m_types.Vector(m_types.Integer()), m_types.String(),
                          mangler.Class([m_types.Floating()], mangler.Name("complex")), m_types.Floating()]),

        mangler.Function([m_types.Dictionary(m_types.String(), m_types.Integer())]),

        mangler.Function([]),

    ]

    mangler.mangler_demanger_test(bodies, True)

    print("All tests passed")

    print("##################################")
    print("Deduce types")
    print("##################################")

    translator.translate(t)


