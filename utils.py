import ast
import symtable

import custom_nodes
import custom_unparser
import deduction
import errors
import symbol_table
import sugar
import mangler
import m_types
from requirements import resolve_function

# Given an expression like a.b.c.d, will return the attribute associated with a
def get_innermost_attribute(_ast: ast.Attribute):
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
            yield None, node
        if type(node) is ast.ClassDef:
            for member_function in filter(lambda n : type(n) is ast.FunctionDef, node.body):
                yield node, member_function


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

def analysis(source):
    my_ast = ast.parse(source, mode='exec')
    table = symtable.symtable(source, "", compile_type="exec")

    # Convert certain operations in to their syntactic sugar equivalent
    sugar.resolve_special_functions(my_ast)


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
    print("First function first argument Requirements")
    print("##################################")

    #it = function_iterator(my_ast)
    #_, first_func = next(it)
    #first_arg = first_func.args.args[0]

    #resolve_function(first_func)
    print("Requirements not yet implemented")

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

    deduction.deduce_main(t)




# Function which extracts the names of member variables for all classes in a program
# Returns a dict mapping class names to a list of member variables
def resolve_member_variables(_ast: ast.Module):
    member_mapping = {}

    # Get all the classes in the outermost scope
    for class_node in filter(lambda node : type(node) is ast.ClassDef, _ast.body):
        members = set()

        # Get the '__init__' function for the class, if it has one
        init = None
        for node in class_node.body:
            if type(node) is not ast.FunctionDef:
                raise errors.NestedClassException(class_node, node)
            if node.name == "__init__":
                init = node
                break
        # If the class has no init function this is an error
        if init == None:
            raise errors.ClassMissingInitException(class_node)
        else:

            # Get any assignments (a = b) in the initialiser
            for assignment in filter(lambda node : type(node) is ast.Assign, node.body):
                # Get any assignment target that is an SelfMemberVariable
                for attribute in filter(lambda node : type(node) is custom_nodes.SelfMemberVariable, assignment.targets):

                    members.add(attribute.id)

        member_mapping[class_node.name] = members

    return member_mapping
