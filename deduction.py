import ast

import custom_nodes
import errors
import m_types
import symbol_table
from collections import OrderedDict
import ir


def deduce(table: symbol_table.Table):
    t = Deduction(table)
    t.visit_FunctionDef(table.get_main().ast_node)
    return t.working_tree_node



class TypeTree:
    def __init__(self, name, arg_types, node, parent, parent_class):
        self.function_name = name
        arg_map = {key.arg: value for key, value in zip(node.args.args, arg_types)}
        if parent_class:
            member_types = parent_class.member_types
        else:
            member_types = OrderedDict()
        self.node = node
        self.parent = parent
        self.symbol_map = {**arg_map, **dict(member_types)}
        self.child_trees = []
        self.ret_type = None
        self.parent_class = parent_class # None if the function is a global function, UserClass node if the function is a member function

    def __repr__(self):
        return f"TypeTree(name='{self.function_name}', map={self.symbol_map}, children={self.child_trees}, class={self.parent_class}, ret_type={self.ret_type})"



# Translator walks the nodes and a) resolves types and b) converts code into IR
class Deduction(ast.NodeVisitor):

    # A list that can be used as a key in dictionaries
    class HashableList:

        def __init__(self, iterable=[]):
            self.l = list(iterable)

        def __hash__(self):
            h = 0

            for item in self.l:
                h ^= hash(item)

            return h

        def __eq__(self, other):
            return self.l == other.l

    # Given a built-in type (expr), a function name (func) and a list of argument types (...) we can determine the
    # return type of the function expr.func(...) using the following structure
    built_in_returns = {
        m_types.Boolean(): {
            "__bool__": { HashableList(): m_types.Boolean() },
            "__float__": { HashableList(): m_types.Floating() },
            "__int__": { HashableList(): m_types.Integer() },
            "__index__": { HashableList(): m_types.ID() },
            "__str__": { HashableList(): m_types.String() },
            "__fmt__": { HashableList(): m_types.String() },
            "__bytes__": { HashableList(): m_types.Bytes() },
            "__len__": { HashableList(): m_types.ID() },

            "__hash__": { HashableList(): m_types.Integer() },

            "__real__": { HashableList(): m_types.Floating() },
            "__imag__": { HashableList(): m_types.Floating() },

            "__one__": { HashableList(): m_types.Boolean() },
            "__zero__": { HashableList(): m_types.Boolean() },
        },

        m_types.Floating(): {
            "__add__": { HashableList([m_types.Floating()]): m_types.Floating(), HashableList([m_types.Integer()]): m_types.Floating()},
            "__real__": { HashableList(): m_types.Floating()  },
            "__imag__": { HashableList(): m_types.Floating()  },
        },

        m_types.Integer(): {
            "__add__": { HashableList([m_types.Integer()]): m_types.Integer(), HashableList([m_types.Floating()]): m_types.Floating() },
            "__real__": { HashableList(): m_types.Integer()  },
            "__imag__": { HashableList(): m_types.Integer()  },
        },
    }

    def __init__(self, table: symbol_table.Table):
        self.whole_table = table

        self.working_tree_node = TypeTree("main", [], table.get_main().ast_node, None, None)


    # Assert that all the expressions in args are the same type, then return this type. Otherwise raise an exception
    def assert_same_type(self, *args):
        pass

    def traverse(self, node):
        if isinstance(node, list):
            return [self.visit(n) for n in node]
        else:
            return self.visit(node)


    # Given a list of potential functions and a list of agruments, choose the most appropriate function template
    def match_function(self, arg_list, candidates):
        return candidates[0]


    def visit_Constant(self, node):
        if isinstance(node.value, bool):
            return m_types.Boolean()
        elif isinstance(node.value, int):
            return m_types.Integer()
        elif isinstance(node.value, float):
            return m_types.Floating()
        elif isinstance(node.value, str):
            return m_types.String()
        else:
            raise NotImplemented()

    def visit_Name(self, node):
        return self.working_tree_node.symbol_map[node.id]


    def visit_Tuple(self, node):
        return m_types.Ntuple(self.traverse(node.elts))

    def visit_MyCall(self, node):
        # First we need to find out whether this node represents:
        # a) a function call
        # b) a callable object call
        # c) a constructor call

        # first we check for any local variables with the name
        if node.id in self.working_tree_node.symbol_map:
            # Convert the mycall 'identifier(...)' into 'identifier.__call__(...)'
            return self.visit_MemberFunction(custom_nodes.MemberFunction(ast.Name(node.id), "__call__", node.args))

        if node.id in self.whole_table:

            table_entry = self.whole_table[node.id]

            if isinstance(table_entry, list):
                if len(table_entry) == 0:
                    raise "MyCall is not a function, object or constructor call"
                else:
                    # Get an ordered list of the argument types for the function call
                    arg_types = self.traverse(node.args)
                    # Get the function table entry for the function being called
                    function_table = self.match_function(arg_types, table_entry)

                    tt = TypeTree(node.id, arg_types, function_table.ast_node, self.working_tree_node, None)
                    self.working_tree_node.child_trees.append(tt)
                    self.working_tree_node = tt

                    # Traverse the FunctionDef
                    self.traverse(function_table.ast_node)

                    ret_type = self.working_tree_node.ret_type
                    parent = self.working_tree_node.parent
                    self.working_tree_node = parent

                    return ret_type
            elif isinstance(self.whole_table[node.id], symbol_table.Class):
                # Get an ordered list of the argument types for the function call
                arg_types = self.traverse(node.args)
                # Get the function table entry for the __init__ function of the class being constructed
                function_table = self.match_function(arg_types, self.whole_table[node.id]["__init__"])

                tt = TypeTree("__init__", arg_types, function_table.ast_node, self.working_tree_node, None)
                self.working_tree_node.child_trees.append(tt)
                self.working_tree_node = tt

                # Traverse the FunctionDef
                self.traverse(function_table.ast_node)

                m = self.working_tree_node.symbol_map
                parent = self.working_tree_node.parent
                self.working_tree_node = parent

                member_var_types = OrderedDict()

                for mem in self.whole_table[node.id].member_variables:
                    member_var_types["self." + mem.name] = m["self." + mem.name]

                return m_types.UserClass(node.id, member_var_types)


    def visit_FormattedValue(self, node):
        raise NotImplemented()
        return m_types.String()

    def visit_SelfMemberVariable(self, node):
        return self.working_tree_node.symbol_map["self." + node.id]

    def visit_SelfMemberFunction(self, node):
        # Get an ordered list of the argument types for the function call
        arg_types = self.traverse(node.args)

        user_class = self.working_tree_node.parent_class

        class_table = self.whole_table[user_class.identifier]
        function_table = self.match_function(arg_types, class_table[node.id])

        tt = TypeTree("__init__", arg_types, function_table.ast_node, self.working_tree_node, user_class)
        self.working_tree_node.child_trees.append(tt)
        self.working_tree_node = tt

        # Traverse the FunctionDef
        self.traverse(function_table.ast_node)

        ret_type = self.working_tree_node.ret_type
        parent = self.working_tree_node.parent
        self.working_tree_node = parent

        return ret_type


    def visit_MemberFunction(self, node):
        ex_type = self.traverse(node.exp)
        # Get an ordered list of the argument types for the function call
        arg_types = self.traverse(node.args)

        if type(ex_type) is m_types.UserClass:

            class_name = ex_type.identifier
            class_table = self.whole_table[class_name]
            function_table = self.match_function(arg_types, class_table[node.id])

            tt = TypeTree(node.id, arg_types, function_table.ast_node, self.working_tree_node, ex_type)
            self.working_tree_node.child_trees.append(tt)
            self.working_tree_node = tt

            # Traverse the FunctionDef
            self.traverse(function_table.ast_node)

            ret_type = self.working_tree_node.ret_type
            parent = self.working_tree_node.parent
            self.working_tree_node = parent


            return ret_type


        else:
            # Expression is a built-in type, so to get the return type we look to the built_in_returns map
            return self.built_in_returns[ex_type][node.id][self.HashableList(arg_types)]


    def visit_SolitarySelf(self, node):
        return self.working_tree_node.parent_class

    def visit_MonoAssign(self, node):

        r_value_type = self.traverse(node.value)

        if isinstance(node.target, ast.Name):

            if node.target.id in self.working_tree_node.symbol_map:

                if self.working_tree_node.symbol_map[node.target.id] != r_value_type:
                    raise "Reassignment (to a different type) is not supported right now. The TypeTree structure only holds one type per variable name and is not able to support reassignment"
                else:
                    #node.assign_type = custom_nodes.Reassign()
                    pass
            else:
                #node.assign_type = custom_nodes.FirstAssign()
                self.working_tree_node.symbol_map[node.target.id] = r_value_type

        elif isinstance(node.target, custom_nodes.SelfMemberVariable):
            self.working_tree_node.symbol_map["self." + node.target.id] = r_value_type
        else:
            raise NotImplemented()



    def visit_Return(self, node):
        ret_type = self.traverse(node.value)
        self.working_tree_node.ret_type = ret_type




    def visit_FunctionDef(self, node):
        self.traverse(node.body)

