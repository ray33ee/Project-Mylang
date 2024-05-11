import symtable
import ast
import utils
import sugar
import errors
import symbol_table
import custom_unparser
import mangler
import demangler
import m_types

source = """

def thing(x, y):
    x.something(y.something_else())

"""

table = symtable.symtable(source, "", "exec")

utils.analysis(source)

bodies = [mangler.Function([m_types.Integer(), mangler.Class([m_types.Boolean()], mangler.Name("s"))], m_types.Integer()),

mangler.Class([mangler.Class([m_types.Boolean()], mangler.Name("s")), mangler.Class([m_types.Integer()], mangler.Name("t") )]),

mangler.Function([m_types.Vector(m_types.Integer()), m_types.String(), mangler.Class([m_types.Floating()], mangler.Name("complex")), m_types.Floating()]),

mangler.Function([m_types.Dictionary(m_types.String(), m_types.Integer())]),


          ]

for body in bodies:
    mangler.mangler_demanger_test(body, True)

print("All tests passed")