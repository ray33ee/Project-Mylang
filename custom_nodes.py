import ast

# A Self on its own, without accessing any attributes (for example return self, or x = self)
class SolitarySelf(ast.Name):
    def __init__(self, name: ast.Name):
        self._fields = name._fields
        super().__init__("self", name.ctx)


# A Self.SOMETHING, a special type of attribute
class SelfMemberVariable(ast.Attribute):
    def __init__(self, attribute: ast.Attribute):
        self._fields = attribute._fields
        super().__init__(ast.Name("self", attribute.value.ctx), attribute.attr, attribute.ctx)
