import symtable
import ast
import utils
import sugar
import errors
import symbol_table
import custom_unparser

source = """

class Complex:
    def __init__(real, imag):
        self.real = real
        self.imag = imag
        
    def __init__(real):
        return Complex(real, 0)
        
    def __get_real__(self):
        return self.real
    
    def __set_imag__(self, imag):
        self.imag = imag
    
    def __get_imag__(self):
        return self.imag
    
    def __set_real__(self, real):
        self.real = real
        
    def __imag__(self):
        return self.imag
        
    def __real__(self):
        return self.real
 
"""

table = symtable.symtable(source, "", "exec")


utils.analysis(source)

