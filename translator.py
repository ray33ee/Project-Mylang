import ast
import errors
import symbol_table


def translate(table: symbol_table.Table):
    return Translator(table).visit(table.get_main().ast_node)


class Translator(ast.NodeVisitor):
    def __init__(self, table: symbol_table.Table):


        print(ast.dump(table.get_main().ast_node))

        print(table)
