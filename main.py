import symtable
import ast
import utils
import sugar

source = """



"""

table = symtable.symtable(source, "", "exec")

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
                raise f"Class {class_node.name} contains a non-function node {node.name}. Classes can only contain functions"
            if node.name == "__init__":
                init = node
                break
        # If the class has no init function this is an error
        if init == None:
            raise f"Class {class_node.name} MUST implement __init__"
        else:

            # Get any assignments (a = b) in the initialiser
            for assignment in filter(lambda node : type(node) is ast.Assign, node.body):
                # Get any assignment target that is an attribute
                for attribute in filter(lambda node : type(node) is ast.Attribute, assignment.targets):
                    innermost = utils.get_inntermost_attribute(attribute)

                    # if the attribute is of the form self.SOMETHING then the SOMETHING is a member variable
                    if innermost.value.id == 'self' and type(innermost.value.ctx) is ast.Load:
                        members.add(innermost.attr)

        member_mapping[class_node.name] = members

    return member_mapping



my_ast = ast.parse(source, mode='exec')

print(ast.dump(my_ast, indent=4))

selves = resolve_member_variables(my_ast)

print(selves)

print(ast.dump(my_ast, indent=4))

sugar.resolve_special_functions(my_ast)
print(ast.dump(my_ast, indent=4))

print(ast.unparse(my_ast))