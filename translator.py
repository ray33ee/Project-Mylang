import ast

import custom_nodes
import deduction
import errors
import m_types
import symbol_table
from collections import OrderedDict


def translate(table: symbol_table.Table):
    t = Translator(table)
    t.function_stack.push(FunctionFrame({}))
    t.visit_FunctionDef(table.get_main().ast_node)
    print(t.function_stack.peek().symbol_map)


class ClassFrame:
    def __init__(self, cls):
        self.cls = cls

class FunctionFrame:
    def __init__(self, arg_types_map, function=None, cls=None):
        self.working_function = function
        self.working_class = cls
        self.symbol_map = arg_types_map

        self.return_type = None

    def __setitem__(self, key, value):
        print(self.symbol_map)
        self.symbol_map[key] = value

    def __getitem__(self, item):
        try:
            return self.symbol_map[item]
        except KeyError:
            raise errors.VariableUsedBeforeAssignment(item)

    def __contains__(self, item):
        return item in self.symbol_map


class Stack:
    def __init__(self):
        self.x = []

    def push(self, value):
        self.x.append(value)

    def peek(self):
        return self.x[-1]

    def pop(self):
        return self.x.pop()


class Translator(ast.NodeVisitor):

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


    # The following dictionary maps types to another dictionary which itself maps mangled names to their return values
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
            "__add__": { HashableList([m_types.Floating()]): m_types.Floating() },
        },

        m_types.Integer(): {
            "__add__": { HashableList([m_types.Integer()]): m_types.Integer() },
        },
    }

    def __init__(self, table: symbol_table.Table):
        self.function_stack = Stack()
        self.class_stack = Stack()
        self.whole_table = table

    # Assert that all the expressions in args are the same type, then return this type. Otherwise raise an exception
    def assert_same_type(self, *args):
        pass

    def traverse(self, node):
        if isinstance(node, list):
            return [self.visit(n) for n in node]
        else:
            return self.visit(node)

    def visit_FunctionDef(self, node):
        self.traverse(node.body)

    def visit_MonoAssign(self, node):

        r_value_type = self.traverse(node.value)

        if isinstance(node.target, ast.Name):

            if node.target.id in self.function_stack.peek():
                if self.function_stack.peek()[node.target.id] != r_value_type:
                    node.assign_type = custom_nodes.FirstAssign()
                    self.function_stack.peek()[node.target.id] = r_value_type
                else:
                    node.assign_type = custom_nodes.Reassign()
            else:
                node.assign_type = custom_nodes.FirstAssign()
                self.function_stack.peek()[node.target.id] = r_value_type

        elif isinstance(node.target, custom_nodes.SelfMemberVariable):
            self.function_stack.peek()["self." + node.target.id] = r_value_type
        else:
            raise NotImplemented()



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
        return self.function_stack.peek()[node.id]


    def visit_Tuple(self, node):
        return m_types.Tuple(self.traverse(node.elts))

    def visit_MyCall(self, node):
        # First we need to find out whether this node represents:
        # a) a function call
        # b) a callable object call
        # c) a constructor call

        # first we check for any local variables with the name
        if node.id in self.function_stack.peek():
            raise NotImplemented()
            return

        if node.id in self.whole_table:
            if isinstance(self.whole_table[node.id], symbol_table.Function):
                # Get an ordered list of the argument types for the function call
                arg_types = self.traverse(node.args)
                # Get the function table entry for the function being called
                function_table = self.whole_table[node.id]
                # Combine the arg names and arg types into a map from name to type
                arg_map = {key.arg: value for key, value in zip(function_table.ast_node.args.args, arg_types)}
                # Add a stack frame for the function
                self.function_stack.push(FunctionFrame(arg_map))
                # Traverse the FunctionDef
                self.traverse(function_table.ast_node)
                # Pop the stack frame off and get the return type of the function
                frame = self.function_stack.pop()
                return frame.return_type
            elif isinstance(self.whole_table[node.id], symbol_table.Class):
                # Get an ordered list of the argument types for the function call
                arg_types = self.traverse(node.args)
                # Get the function table entry for the __init__ function of the class being constructed
                function_table = self.whole_table[node.id]["__init__"]
                # Combine the arg names and arg types into a map from name to type
                arg_map = {key.arg: value for key, value in zip(function_table.ast_node.args.args, arg_types)}
                # Add a stack frame for the function
                self.function_stack.push(FunctionFrame(arg_map))
                # Traverse the FunctionDef
                self.traverse(function_table.ast_node)
                # Pop the stack frame off and get the return type of the function
                frame = self.function_stack.pop()


                member_var_types = OrderedDict()

                for mem in self.whole_table[node.id].member_variables:
                    member_var_types["self." + mem.name] = frame["self." + mem.name]

                print(member_var_types)

                return deduction.UserClass(node.id, member_var_types)

            else:
                raise "MyCall is not a function, object or constructor call"

    def visit_FormattedValue(self, node):
        return m_types.String()

    def visit_Return(self, node):
        print(node.value)
        self.function_stack.peek().return_type = self.traverse(node.value)

    def visit_SelfMemberVariable(self, node):
        print(ast.dump(node))
        return self.class_stack.peek().cls.member_types["self." + node.id]

    def visit_SelfMemberFunction(self, node):
        user_class = self.class_stack.peek().cls
        class_table = self.whole_table[user_class.identifier]
        function_table = class_table[node.id]
        # Get an ordered list of the argument types for the function call
        arg_types = self.traverse(node.args)
        # Combine the arg names and arg types into a map from name to type
        arg_map = {key.arg: value for key, value in zip(function_table.ast_node.args.args, arg_types)}
        # Combine this with the member map
        arg_map = {**arg_map, **dict(user_class.member_types)}
        # Add a stack frame for the function
        self.function_stack.push(FunctionFrame(arg_map))
        # Traverse the FunctionDef
        self.traverse(function_table.ast_node)
        # Pop the stack frame off and get the return type of the function
        frame = self.function_stack.pop()
        return frame.return_type


    def visit_MemberFunction(self, node):
        ex_type = self.traverse(node.exp)

        if type(ex_type) is deduction.UserClass:
            class_name = ex_type.identifier
            class_table = self.whole_table[class_name]
            function_table = class_table[node.id]

            # Get an ordered list of the argument types for the function call
            arg_types = self.traverse(node.args)
            # Combine the arg names and arg types into a map from name to type
            arg_map = {key.arg: value for key, value in zip(function_table.ast_node.args.args, arg_types)}

            # Combine this with the member map
            arg_map = {**arg_map, **dict(ex_type.member_types)}
            # Add a stack frame for the function
            self.function_stack.push(FunctionFrame(arg_map))
            self.class_stack.push(ClassFrame(ex_type))
            # Traverse the FunctionDef
            self.traverse(function_table.ast_node)
            self.class_stack.pop()
            # Pop the stack frame off and get the return type of the function
            frame = self.function_stack.pop()
            return frame.return_type


        else:

            return self.built_in_returns[ex_type][node.id][self.HashableList(self.traverse(node.args))]

        print(ex_type)
        print("Member")



