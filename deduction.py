import ast
from contextlib import contextmanager

import custom_nodes
import errors
import m_types
import parse_template
import symbol_table
import ir
import logging

logger = logging.getLogger(__name__)

def deduce(table: symbol_table.Table):
    t = _Deduction(table)
    t.visit_FunctionDef(table.get_main().ast_node)
    return t.manager.working_tree_node

class TreeManager:

    def __init__(self, table):
        self.table = table
        self.working_tree_node = TypeTree("main", [], table.get_main().ast_node, None, None, None)


    @contextmanager
    def new_child_tree(self, arg_types, ast_node, parent_class_type, parent_class_node):

        tt = TypeTree(ast_node.name, arg_types, ast_node, self.working_tree_node, parent_class_type, parent_class_node)
        self.working_tree_node.child_trees.append(tt)
        self.working_tree_node = tt
        yield
        self.working_tree_node = self.working_tree_node.parent

    def substitute_node(self, node, sub):
        self.working_tree_node.subs[node] = sub

    def is_node_in_symbolmap(self, node):
        return node in self.working_tree_node.symbol_map

    def get_map(self):
        return self.working_tree_node.symbol_map

    def get_symbol(self, node):
        return self.working_tree_node.symbol_map[node]

    def insert_symbol(self, node, symbol):
        self.working_tree_node.symbol_map[node] = symbol

    def get_ret_type(self):
        return self.working_tree_node.ret_type

    def set_ret_type(self, ret_type):
        self.working_tree_node.ret_type = ret_type

    def get_parent_class_type(self):
        return self.working_tree_node.parent_class_type

    def set_parent_class_type(self, class_type):
        self.working_tree_node.parent_class_type = class_type



class TypeTree(ast.AST):

    _fields = ["function_name", "arg_map", "ret_type", "ast_node", "child_trees"]

    def __init__(self, name, arg_types, ast_node, parent, parent_class_type, parent_class_node):
        # Todo: We don't need to pass 'name' as we can deduce this from ast_node.name
        self.function_name = ast_node.name
        self.arg_types = arg_types

        self.arg_map = []

        if parent_class_type and self.function_name != "__init__":
            member_types = parent_class_type.member_types
        else:
            member_types = []

        # Combine the argument map and the class member variable map into one
        self.symbol_map = {}

        # Combine the arg name and type into an ir.Arg
        # also add the arg into the symbol map
        for key, value in zip(ast_node.args.args, arg_types):
            self.arg_map.append(ir.Arg(key.arg, value))
            self.symbol_map[key.arg] = value

        for member in member_types:
            self.symbol_map[member.id] = member.annotation

        self.ast_node = ast_node
        self.parent = parent

        self.child_trees = []
        self.ret_type = m_types.Ntuple([])
        self.parent_class_type = parent_class_type # None if the function is a global function, UserClass node if the function is a member function
        self.parent_class_node = parent_class_node
        # A set of node substitutions. These can be used to allow modification of function code for each function not for the entire template
        # Maps nodes to substitute to nodes to substitute with
        self.subs = {}

    def get_member_map(self):
        pass

    def __repr__(self):
        return ast.dump(self, indent=4)



# Translator walks the nodes and a) resolves types and b) converts code into IR
class _Deduction(ast.NodeVisitor):


    built_in_functions = {
        "print_string": m_types.Ntuple([]),
        "panic_string": m_types.Ntuple([]),
    }

    def __init__(self, table: symbol_table.Table):
        self.whole_table = table

        self.biumap = {}

        self.manager = TreeManager(table)


    # Assert that all the expressions in args are the same type, then return this type. Otherwise raise an exception
    def assert_same_type(self, *args):
        pass

    def traverse(self, node):
        if isinstance(node, list):
            return [self.visit(n) for n in node]
        else:
            return self.visit(node)


    def recursive_compare(self, arg, annotation):

        # Here we have a simple system to score an argument,annotation pair on how compatible they are.
        # If they are completely different types (For example int and float) then they have a score of -inf (which is propagated through recursive calls)
        # If they are the same type and not containers, this is a score of 1
        # If they are the same type and containers, this is a score of 1 plus the scores of the inner types
        # If they are different types but the annotation is a wildcard, this is a score of 0

        if type(arg) is type(annotation):
            if type(annotation) is m_types.Vector:
                return self.recursive_compare(arg.element_type, annotation.element_type) + 1
            elif type(annotation) is m_types.DynamicSet:
                return self.recursive_compare(arg.element_type, annotation.element_type) + 1
            elif type(annotation) is m_types.Option:
                return self.recursive_compare(arg.contained_type, annotation.contained_type) + 1
            elif type(annotation) is m_types.Result:
                return self.recursive_compare(arg.ok_type, annotation.ok_type) + self.recursive_compare(arg.err_type, annotation.err_type) + 1
            elif type(annotation) is m_types.Dictionary:
                return self.recursive_compare(arg.key_type, annotation.key_type) + self.recursive_compare(arg.value_type, annotation.value_type) + 1
            elif type(annotation) is m_types.Ntuple:
                raise NotImplemented()
            else:
                return 1
        else:
            if type(annotation) is m_types.WildCard:
                return 0
            else:
                return float("-inf")

    def get_score(self, arg_list, candidate):

        # If the number of args doesn't match, the candidate cannot be a match
        if len(arg_list) != len(candidate.args.args):
            return None

        total_score = 0

        for arg, annotate in zip(arg_list, candidate.args.args):
            logger.debug("        **********")
            logger.debug("        Arg")
            logger.debug("        **********")
            score = self.recursive_compare(arg, annotate.annotation)
            logger.debug("        Argument Score: " + str(score))
            total_score += score

        if total_score == float("-inf"):
            return None
        else:
            return total_score





    # Given a list of potential functions and a list of agruments, choose the most appropriate function template
    def match_function(self, arg_list, candidates):

        logger.debug("**********")
        logger.debug("Matcher")
        logger.debug("**********")

        logger.debug(arg_list)

        best_score, best_choice = float("-inf"), None

        if len(candidates) == 0:
            raise "There should always be at least one candidate"

        for candidate in candidates:
            logger.debug("    **********")
            logger.debug("    Candidate")
            logger.debug("    **********")
            logger.debug("    " + ast.dump(candidate.ast_node))
            score = self.get_score(arg_list, candidate.ast_node)
            logger.debug("    Candidate Score: " + str(score))
            if score is not None:
                if score > best_score:
                    best_score, best_choice = score, candidate
                elif score == best_score:
                    # 'candidate' and 'best_choice' have the same score
                    raise "Two candidates cannot have the same score"

        if best_choice is None:
            raise "A suitable candidate could not be found"

        logger.debug("Best score: " + str(best_score))
        logger.debug("Best Candidate: " + str(ast.dump(best_choice.ast_node)))

        return best_choice


    def visit_Constant(self, node):
        if isinstance(node.value, bool):
            return m_types.Boolean()
        elif isinstance(node.value, int):
            return m_types.Integer()
        elif isinstance(node.value, float):
            return m_types.Floating()
        elif isinstance(node.value, str):
            return m_types.String()
        elif node.value is None:
            return m_types.Option(m_types.Unknown(self))
        else:
            raise NotImplemented()

    def visit_Name(self, node):
        return self.manager.get_symbol(node.id)


    def visit_List(self, node):
        if len(node.elts) == 0:
            return m_types.Vector(m_types.Unknown(self))
        elif len(node.elts) > 0:
            return m_types.Vector(self.traverse(node.elts[0]))
        else:
            raise NotImplemented()


    def visit_Tuple(self, node):
        return m_types.Ntuple(self.traverse(node.elts))

    def visit_MyCall(self, node):
        # First we need to find out whether this node represents:
        # a) a function call
        # b) a callable object call
        # c) a constructor call

        # first we check for any local variables with the name
        if self.manager.is_node_in_symbolmap(node.id):
            # Add an entry to the substitution map
            self.manager.substitute_node(node, custom_nodes.MemberFunction(ast.Name(node.id), "__call__", node.args, self.traverse(node.args), self.manager.get_symbol(node.id)))
            # Treat the mycall 'identifier(...)' as a 'identifier.__call__(...)'
            return self.visit_MemberFunction(custom_nodes.MemberFunction(ast.Name(node.id), "__call__", node.args))

        if node.id == "some":
            arg_types = self.traverse(node.args)

            if node.id == "some":

                # some(expr) does not evaluate to a function, but it converts to rusts std::option::Option::Some(expe)

                if len(arg_types) != 1:
                    raise "some function takes exactly one argument"

                a = arg_types[0]

                self.manager.substitute_node(node, custom_nodes.SomeCall(node.args[0]))

                return m_types.Option(a)

        if node.id == "byte_array":

            if len(node.args) != 0:
                raise "Bytes function takes no arguments"

            self.manager.substitute_node(node, custom_nodes.BytesCall())

            return m_types.Bytes()


        if node.id in self.whole_table:

            table_entry = self.whole_table[node.id]

            if isinstance(table_entry, list):
                if len(table_entry) == 0:
                    raise "MyCall is not a function, object or constructor call"
                else:
                    # Global function call

                    # Get an ordered list of the argument types for the function call
                    arg_types = self.traverse(node.args)

                    # Get the function table entry for the function being called
                    function_table = self.match_function(arg_types, table_entry)

                    with self.manager.new_child_tree(arg_types, function_table.ast_node, None, None):

                        # Traverse the FunctionDef
                        self.traverse(function_table.ast_node)

                        ret_type = self.manager.get_ret_type()

                    self.manager.substitute_node(node, custom_nodes.MyCall(node.id, node.args, arg_types))

                    return ret_type
            elif isinstance(self.whole_table[node.id], symbol_table.Class):
                # Constructor call

                # Get an ordered list of the argument types for the function call
                arg_types = self.traverse(node.args)

                class_entry = self.whole_table[node.id]

                # Get the function table entry for the __init__ function of the class being constructed
                function_table = self.match_function(arg_types, class_entry["__init__"])

                with self.manager.new_child_tree(arg_types, function_table.ast_node, None, class_entry.node):

                    # Traverse the FunctionDef
                    self.traverse(function_table.ast_node)

                    m = self.manager.get_map()

                    member_var_types = []

                    for mem in self.whole_table[node.id].member_variables:
                        member_var_types.append(ir.Member("self." + mem.name, m["self." + mem.name]))

                    usr_class = m_types.UserClass(node.id, member_var_types)

                    logger.debug("Arg types")
                    logger.debug(arg_types)

                    self.manager.set_parent_class_type(usr_class)

                self.manager.substitute_node(node, custom_nodes.ConstructorCall(usr_class, node.args, arg_types))


                # If the class has a __del__ implementation, we need to implement this
                if "__del__" in class_entry:


                    function_table_del = self.match_function([], class_entry["__del__"])

                    print(function_table_del)

                    with self.manager.new_child_tree([], function_table_del.ast_node, usr_class, class_entry.node):
                        # Traverse the FunctionDef
                        self.traverse(function_table_del.ast_node)


                return usr_class

        else:

            # For any call not in the symbol table, we assume is a global function call to an external functions (print, panic, etc.)

            # Get an ordered list of the argument types for the function call
            arg_types = self.traverse(node.args)

            self.manager.substitute_node(node, custom_nodes.MyCall(node.id, node.args, arg_types))


        if node.id in self.built_in_functions:
            return self.built_in_functions[node.id]

        print(node.id)

        if m_types.BuiltInClass(node.id) in parse_template.built_in_classes:
            arg_types = self.traverse(node.args)

            self.manager.substitute_node(node, custom_nodes.BuiltInClassConstructor(node.id, node.args, arg_types))

            return m_types.BuiltInClass(node.id)

        logger.error(f"Could not resolve function call '{node.id}', Node: {ast.dump(node)}")
        raise "See log"


    def visit_JoinedStr(self, node):
        self.traverse(node.values)
        return m_types.String()

    def visit_SelfMemberVariable(self, node):
        return self.manager.get_symbol("self." + node.id)

    def visit_SelfMemberFunction(self, node):
        # Get an ordered list of the argument types for the function call
        arg_types = self.traverse(node.args)

        user_class = self.manager.get_parent_class_type()

        class_table = self.whole_table[user_class.identifier]
        function_table = self.match_function(arg_types, class_table[node.id])

        with self.manager.new_child_tree(arg_types, function_table.ast_node, user_class, class_table.node):
            # Traverse the FunctionDef
            self.traverse(function_table.ast_node)

            ret_type = self.manager.get_ret_type()

        self.manager.substitute_node(node, custom_nodes.SelfMemberFunction(node.id, node.args, arg_types))

        return ret_type


    def handle_builtin(self, node, ex_type, arg_types):

        # If any arg_types are unknowns, we need to add these ass dependents to ex_type
        found_unknown = False
        u = m_types.Unknown(self)

        for t in arg_types:
            if type(t) is m_types.Unknown:
                if not t.has_inner():
                    found_unknown = True
                    t.add_dependent(u, node, arg_types)

        if found_unknown:
            return u

        if type(ex_type) is m_types.Vector and node.id == "append":
            t = arg_types[0]
            ex_type.element_type.fill(t)
            self.manager.substitute_node(node, custom_nodes.MemberFunction(node.exp, node.id, node.args,
                                                                            arg_types, ex_type))
            return m_types.Ntuple([])

        elif type(ex_type) is m_types.Unknown:
            if ex_type.has_inner():
                ex_type = ex_type.get_type()
            else:
                # Replace with a node containing type info

                self.manager.substitute_node(node, custom_nodes.MemberFunction(node.exp, node.id, node.args,
                                                                                arg_types, ex_type))

                # Create a new unknown for the return type of the built in call and tie this unknown to ex_type.
                # This means that when ex_type's unknown is resolved, this new unknown will be resolved too
                u = m_types.Unknown(self)
                ex_type.add_dependent(u, node, arg_types)
                return u


        # Expression is a built-in type, so to get the return type we look to the built_in_returns map

        b = parse_template.bim.get_item(type(ex_type), node.id, arg_types)

        # If the lookup returns a string, this represents an associated type. We access this type via getattr on the extype:
        if type(b) is str:
            b = getattr(ex_type, b)

        self.manager.substitute_node(node, custom_nodes.MemberFunction(node.exp, node.id, node.args,
                                                                        arg_types, ex_type))

        # If the lookup fails, we might be able to use the right functions instead. For example
        # if __add__ fails try __radd__ instead. If radd works, replace it with `self.working_tree_node.subs`.

        # Lets use an example, say we have a function call
        # a.__add__(b)
        # which is not implemented for 'a'. We then try
        # b.__radd__(a)
        # if this is implemented, we swap it out via the substitution map. if it is not, this is a compiler error

        # Note: We must perform this test on user defined types, as well as built-ins

        return b


    def visit_MemberFunction(self, node):



        ex_type = self.traverse(node.exp)
        # Get an ordered list of the argument types for the function call
        arg_types = self.traverse(node.args)

        if type(ex_type) is m_types.UserClass:

            if node.id == "__id__":

                self.manager.substitute_node(node, custom_nodes.MemberFunction(node.exp, node.id, node.args,
                                                                                       arg_types, ex_type))

                return m_types.ID()

            class_name = ex_type.identifier
            class_table = self.whole_table[class_name]
            function_table = self.match_function(arg_types, class_table[node.id])

            with self.manager.new_child_tree(arg_types, function_table.ast_node, ex_type, class_table.node):
                # Traverse the FunctionDef
                self.traverse(function_table.ast_node)

                ret_type = self.manager.get_ret_type()

            self.manager.substitute_node(node, custom_nodes.MemberFunction(node.exp, node.id, node.args, arg_types, ex_type))

            return ret_type
        elif type(ex_type) is m_types.BuiltInClass:

            b = parse_template.built_in_classes.get_item(ex_type, node.id, arg_types)

            self.manager.substitute_node(node, custom_nodes.MemberFunction(node.exp, node.id, node.args,
                                                                            arg_types, ex_type))

            return b
        else:

            return self.handle_builtin(node, ex_type, arg_types)



    def visit_SolitarySelf(self, node):
        return self.manager.get_parent_class_type()

    def visit_MonoAssign(self, node):

        r_value_type = self.traverse(node.value)

        if isinstance(node.target, ast.Name):

            if self.manager.is_node_in_symbolmap(node.target.id):

                if self.manager.get_symbol(node.target.id) != r_value_type:
                    self.manager.insert_symbol(node.target.id, r_value_type)
                else:
                    # If the variable has been assigned to before and this new assignment is of the same value, we have a reassignment (such as a = a + x)
                    self.manager.substitute_node(node, custom_nodes.Reassign(node.target, node.value))
            else:

                self.manager.insert_symbol(node.target.id, r_value_type)

        elif isinstance(node.target, custom_nodes.SelfMemberVariable):
            self.manager.insert_symbol("self." + node.target.id, r_value_type)
        else:
            raise NotImplemented()


    def visit_InitAssign(self, node):
        self.manager.insert_symbol("self." + node.id, self.traverse(node.value))





    def visit_Return(self, node):
        self.manager.set_ret_type(self.traverse(node.value))


    def visit_If(self, node):
        self.traverse(node.test)
        self.traverse(node.body)


    def visit_While(self, node):
        self.traverse(node.test)
        self.traverse(node.body)

    def visit_For(self, node):

        if type(node.target) is ast.Name:
            ex_type = self.traverse(node.iter)
            logger.warning("Must add expr_type to MemberFunction")
            self.manager.insert_symbol(node.target.id, self.traverse(custom_nodes.MemberFunction(node.iter, "__next__", [])).contained_type)
        else:
            raise "For target must be a name"

        self.traverse(node.body)


    def visit_FunctionDef(self, node):
        self.traverse(node.body)

