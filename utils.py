import ast
import symtable
import errors

# Given an expression like a.b.c.d, will return the attribute associated with a
def get_inntermost_attribute(_ast: ast.Attribute):
    thing = _ast
    while type(thing.value) is not ast.Name:
        thing = thing.value
    return thing


# A special function that iterates over all functions in a source. This will iterate over global functions and
# member functions. Each iteration returns a (parent, node) pair. If the function is a class member function, the node
# is the class member function and the parent is the class. If the function is a global function, the node is the global
# function and the parent is None.
def function_iterator(_ast: ast.Module):
    for node in _ast.body:
        if type(node) is ast.FunctionDef:
            yield (None, node)
        if type(node) is ast.ClassDef:
            for member_function in filter(lambda n : type(n) is ast.FunctionDef, node.body):
                yield (node, member_function)


def variable_iterator(_ast: ast.FunctionDef):
    pass


def parameter_iterator(_ast):
    pass

# Recursively display the contents of a symbol table
def recursive_show(table: symtable.SymbolTable, level):
    nest = '\t' * level

    for symbol in table.get_symbols():
        print(f"{nest} symbol {symbol.get_name()} ({type(symbol)}) local: {symbol.is_local()}")

    for child in table.get_children():
        t = child.get_parameters() if type(child) is symtable.Function else ""
        print(f"{nest} {child.get_type()} {child.get_name()} {t}")
        recursive_show(child, level+1)


# Get a list of all globals, i.e. all top level nodes - currently this is a tuple of a dictionary of
# name-function node pairs, and a dictionary of name-class node pairs,
def get_globals(_ast: ast.Module):
    functions = {}
    classes = {}

    for node in _ast.body:
        if type(node) is ast.FunctionDef:
            functions[node.name] = node
        if type(node) is ast.ClassDef:
            functions = {}
            for f in node.body:
                if type(f) is ast.FunctionDef:
                    functions[f.name] = f
            classes[node.name] = (node, functions)

    return functions, classes