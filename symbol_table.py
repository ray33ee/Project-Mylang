import ast
import symtable

import custom_nodes
import custom_unparser
import errors
import members
import utils

import logging

logger = logging.getLogger(__name__)

# A class representing a variable in a symbol table
class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


# A class representing a function in a symbol table
class Function:
    def __init__(self, ast_node):
        self.name = ast_node.name
        self.ast_node = ast_node
        self.variables = []

        # Get the table from the ast_node itself by unparsing, then using this code in a symtable
        func_code = custom_unparser.unparse(ast_node)

        t = symtable.symtable(func_code, "", "exec")

        if len(t.get_children()) == 0:
            logger.critical("Could not get symbol table from function. Hint: This might be caused by a  missing entry in the custom unparser if a new node was created")
            raise "Could not resolve symbol table for function"


        table = t.get_children()[0]

        for t in table.get_symbols():
            if type(t) is symtable.Symbol:
                # Only add variable symbols, not function calls
                if t.is_local():
                    self.variables.append(Variable(t.get_name()))

    def __str__(self):
        return f"{self.name} {self.ast_node} {self.variables}"


class Class:
    def __init__(self, node, member_variables):
        self.name = node.name
        self.functions = []
        self.node = node
        self.member_variables = member_variables

        for statement in node.body:
            if type(statement) is ast.FunctionDef or type(statement) is custom_nodes.InitFunctionDef:
                self.functions.append(Function(statement))
            else:
                raise "Classes can only contain function definitions"

    def __contains__(self, item):

        for func in self.functions:
            if func.name == item:
                return True

        return False

    def __getitem__(self, item):

        funcs = []

        for func in self.functions:
            if func.name == item:
                funcs.append(func)

        if len(funcs) == 0:
            logger.error(f"No such function {item} in class {self.name}")
            raise "Function not found in class"

        return funcs


# Mylang tables are simpler than python tables, since python allows nested functions, classes, and all sorts of
# topologies, whereas mylang does not. Mylang can have a list of functions and a list of classes. Each class contains
# a list of functions. Each function contains a list of variables. This structure is emulated in the Table class:
class Table:

    def __init__(self, mod: ast.Module):

        self.functions = []
        self.classes = []

        member_variables = members.resolve_members(mod)

        logger.debug("Member Map:")
        logger.debug(member_variables)

        for statement in mod.body:
            if isinstance(statement, ast.FunctionDef):
                self.functions.append(Function(statement))
            elif type(statement) is ast.ClassDef:
                self.classes.append(Class(statement, list(map(lambda x: Variable(x), member_variables[statement.name]))))
            else:
                raise "Top level objects can only be classes or functions"



    def get_main(self):
        try:
            mains = self["main"]
            if len(mains) != 1:
                raise "Too many main functions, source must contain exactly one"
            return mains[0]
        except KeyError:
            raise errors.MainFunctionMissing()

    def __str__(self):
        s = ""
        for f in self.functions:
            s += str(f) + "\n"
            for v in f.variables:
                s += "    " + str(v) + "\n"

        for c in self.classes:
            s += f"{c.name} {c.node}\n"

            for m in c.member_variables:
                s += "    " + str(m) + " <Class Member Variable>\n"

            for f in c.functions:
                s += "    " + str(f) + "\n"
                for v in f.variables:
                    s += "        " + str(v) + "\n"
        return s


    def __contains__(self, item):

        for func in self.functions:
            if func.name == item:
                return True

        for cl in self.classes:
            if cl.name == item:
                return True

        return False

    def __getitem__(self, item):

        for cl in self.classes:
            if cl.name == item:
                return cl

        funcs = []

        for func in self.functions:
            if func.name == item:
                funcs.append(func)


        if len(funcs) == 0:
            logger.error(f"No such global function or class named {item}")
            raise "Function not found in class"

        return funcs
