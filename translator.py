import ast
import logging
import deduction
import ir
import mangle

logger = logging.getLogger(__name__)

def translate(tree):
    t = _Translator(tree)
    logger.debug("**************")
    logger.debug("Mini Tree")
    logger.debug("**************")
    t.climb_tree()
    m = t.module

    m.classes = [x for x in t.class_map.values()]

    return t.module

# Class which takes a TypeTree and returns a Rust IR
class _Translator(ast.NodeVisitor):
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
        triple = self.working_tree.function_name, deduction._Deduction.HashableList(self.working_tree.arg_types), c

        if triple in self.function_set:
            return

        logger.debug("    " * depth + self.working_tree.function_name)

        self.function_set.add(triple)

        # Visit the node
        self.traverse(self.working_tree.ast_node)

        children = self.working_tree.child_trees

        p = self.working_tree.parent

        for child in children:
            self.working_tree = child
            self.climb_tree(depth+1)

        self.working_tree = p


    def visit(self, node):

        if node in self.working_tree.subs:
            return super().visit(self.working_tree.subs[node])
        else:
            return super().visit(node)

    def traverse(self, node):

        if type(node) is list:
            # Convert an array of nodes into an array of self.visit(node) values removing any Nones
            return list(filter(lambda x : x != None, map(self.visit, node)))
        else:
            return self.visit(node)


    def visit_ClassDef(self, node):
        pass

    def visit_FunctionDef(self, node):



        # Create a new IR entry
        ir_function = ir.FunctionDef(self.working_tree.function_name, [ir.Arg(ir.Identifier(id), ann.get_type()) for id, ann in self.working_tree.arg_map.items()])
        ir_function.set_return_type(self.working_tree.ret_type.get_type())

        # Traverse the function body
        ir_function.body = self.traverse(node.body)

        if self.working_tree.parent_class_type and self.working_tree.parent_class_node:
            # Member function
            usr = self.working_tree.parent_class_type

            self.class_map[usr].add_function(ir.MemberFunctionDef(ir_function))
        else:
            # Global function
            if ir_function.name == "main":
                self.module.add_function(ir.MainFunctionDef(ir_function))
            else:
                self.module.add_function(ir_function)

    def visit_InitFunctionDef(self, node):


        # Create a new IR entry
        ir_function = ir.InitFunctionDef(self.working_tree.function_name, [ir.Arg(ir.Identifier(id), ann.get_type()) for id, ann in self.working_tree.arg_map.items()], node.member_list)
        ir_function.set_return_type(self.working_tree.ret_type.get_type())

        # Traverse the function body
        ir_function.body = self.traverse(node.body)


        # Constructor
        usr = self.working_tree.parent_class_type



        l = [ir.Member(field[5:], ann.get_type()) for field, ann in usr.member_types.items()]


        if usr not in self.class_map:
            ir_class = ir.ClassDef(usr.identifier, l)
            self.class_map[usr] = ir_class
        else:
            ir_class = self.class_map[usr]

        ir_class.add_function(ir_function)

    def visit_MonoAssign(self, node):
        return ir.LetAssign(self.traverse(node.target), self.traverse(node.value))

    def visit_GetterAssign(self, node):
        return ir.Reassign(ir.SelfVariable(node.self_id), self.traverse(node.value))

    def visit_Return(self, node):
        return ir.Return(self.traverse(node.value))

    def visit_Expr(self, node):
        return ir.Expr(self.traverse(node.value))

    def visit_If(self, node):
        return ir.IfElse(self.traverse(node.test), self.traverse(node.body), self.traverse(node.orelse))

    def visit_While(self, node):
        return ir.While(self.traverse(node.test), self.traverse(node.body))

    def visit_For(self, node):
        return ir.For(self.traverse(node.target), self.traverse(node.iter), self.traverse(node.body))

    def visit_Break(self, node):
        return ir.Break()

    def visit_Continue(self, node):
        return ir.Continue()

    def visit_Pass(self, node):
        return None

    def visit_Name(self, node):
        return ir.Identifier(node.id)

    def visit_Constant(self, node):
        return ir.Constant(node.value)

    def visit_List(self, node):
        return ir.List(self.traverse(node.elts))

    def visit_Tuple(self, node):
        return ir.Tuple(self.traverse(node.elts))

    def visit_SolitarySelf(self, node):
        return ir.SolitarySelf()

    def visit_SelfMemberVariable(self, node):
        return ir.SelfVariable(node.id)

    def visit_SelfMemberFunction(self, node):
        return ir.SelfFunction(node.id, self.traverse(node.args), node.types)

    def visit_MemberFunction(self, node):
        return ir.MemberFunction(self.traverse(node.exp), node.id, self.traverse(node.args), node.types)

    def visit_ConstructorCall(self, node):
        return ir.ClassConstructor(node.class_id, self.traverse(node.args), node.types)

    def visit_MyCall(self, node):
        return ir.GlobalFunctionCall(node.id, self.traverse(node.args), node.types)

    def visit_InitAssign(self, node):
        return ir.LetAssign(ir.Identifier(mangle.mangle(node)), self.traverse(node.value))
