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


class Test:
    def __init__():
        self.a = 0
        
    def __get_a__(self):
        return self.a
    
    def get(self):
        return self.a
        
    def set(self, a):
        self.a = a
        
    def test(self):
        thing(3, 5.0, "Yes", a.b.c)
        
    def me(self):
        return self
    
    def test(self):
        return -a

def main():
    c = (a+3).b()[5]
"""

source = """


class Complex:
	def __init__(realz, imagz):
		self.real = realz
		self.imag = imagz
		
	def __get_real__(self):
	    return self.real
	
	def __real__(self):
	    return self.real

	def __add__(self, rhs):
		return Complex(real(self) + real(rhs), imag(self) + imag(rhs))


def main():
	c1 = Complex(1, 2)
	c2 = Complex(1.0, 2.0)

	c3 = c2 + c1

	c1 = c1 + 5

	print(c1)
	print(c2)
	print(c3)

"""

source = """

class Empty:
    def __init__():
        self.y = True
        self.x = 0
        
    def thing():
        return self.y
        
    def __get_y__():
        return self.y
    

def main():
    a = True
    a = float(a)
    b = Empty()
    c = b.y
    d = b.thing()

"""

table = symtable.symtable(source, "", "exec")

utils.analysis(source)


m = mangler.Mangler()

print(m(mangler.Name("f"), mangler.Function([m_types.String()])))