import ast

import deduction
import ir


def translate(tree):
    t = Translator(tree)
    t.climb_tree()
    m = t.module

    m.classes = [x for x in t.class_map.values()]

    return t.module

# Class which takes a TypeTree and returns a Rust IR
class Translator(ast.NodeVisitor):
    def __init__(self, tree: deduction.TypeTree):
        self.working_tree = tree

        # Keep track of all function, class pairs to avoid conflicts
        self.function_set = set()

        self.module = ir.Module()
        self.working_function = None
        self.working_class = None

        self.class_map = {}

    def climb_tree(self, depth=0):

        if self.working_tree.parent_class_type:
            c = self.working_tree.parent_class_type
        else:
            if self.working_tree.function_name == "__init__":
                c = self.working_tree.parent_class_node.name
            else:
                c = None

        # The following triple can be used to uniquely represent a function. We use this to avoid repeats
        triple = self.working_tree.function_name, deduction.Deduction.HashableList(self.working_tree.arg_types), c

        if triple in self.function_set:
            return

        print(" " * depth * 4 + self.working_tree.function_name)

        self.function_set.add(triple)

        # Visit the node
        self.traverse(self.working_tree.ast_node)

        children = self.working_tree.child_trees

        p = self.working_tree.parent

        for child in children:
            self.working_tree = child
            self.climb_tree(depth+1)

        self.working_tree = p


    def traverse(self, node):
        if type(node) is list:
            for n in node:
                self.visit(n)
        else:
            self.visit(node)


    def visit_ClassDef(self, node):
        pass

    def visit_FunctionDef(self, node):

        # Create a new IR entry
        self.working_function = ir.FunctionDef(self.working_tree.function_name, self.working_tree.arg_map)
        self.working_function.ret_type = self.working_tree.ret_type

        # Traverse the function body
        self.traverse(node.body)

        if self.working_tree.function_name == "__init__" and self.working_tree.parent_class_type and self.working_tree.parent_class_node:
            usr = self.working_tree.parent_class_type

            if usr in self.class_map:
                raise NotImplemented()
            else:
                ir_class = ir.ClassDef(usr.identifier, usr.member_types)


                self.class_map[usr] = ir_class

            ir_class.add_function(self.working_function)


        elif self.working_tree.parent_class_type and self.working_tree.parent_class_node:
            # Member function
            usr = self.working_tree.parent_class_type

            self.class_map[usr].add_function(self.working_function)
        else:
            # Global function
            self.module.add_function(self.working_function)

        self.working_function = None
