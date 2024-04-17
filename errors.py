

# Exception raised when the child of a ClassDef ast node is not a FunctionDef node
class NestedClassException(Exception):
    def __init__(self, offending_class, non_function_node):
        self.offending_class = offending_class
        self.non_function_node = non_function_node

    def __str__(self):
        return f"Class '{self.offending_class.name}' contains a non-function node of type {type(self.non_function_node)}. Classes can only contain functions"


class ClassMissingInitException(Exception):
    def __init__(self, offending_class):
        self.offending_class = offending_class

    def __str__(self):
        return f"Class '{self.offending_class.name}' has no __init__ method. Every class MUST contain a constructor"


class WrongNumberOfComparisons(Exception):
    def __str__(self):
        return f"The number of comparisons in an ast.Compare must be exactly one. Chained comparison is not allowed"


class ASTExpressionNotSupported(Exception):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f"Python expression ({type(self.expression)}) not supported"


class ChainedAssignmentNotImplemented(Exception):
    def __str__(self):
        return "Chained assignment has not been implemented"


class InvalidTopLevelNodeException(Exception):
    def __str__(self):
        return "Invalid top level node. Only functions or classes are allowed as top level nodes"
