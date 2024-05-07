import symtable
import ast
import utils
import sugar
import errors
import symbol_table
import custom_unparser

source = """

def thing(x, y):
    x.something(y.something_else())

"""

table = symtable.symtable(source, "", "exec")


utils.analysis(source)

