import symtable
import ast

import members
import sugar_v
import utils
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

class Complex:
    def __init__(r, i):
        self.real = r
        self.imag = i
        
    def __get_real__():
        return self.real
        
    def __get_imag__():
        return self.imag
        
    def __real__():
        return self.real
        
    def __imag__():
        return self.imag
    
    def __add__(other):
        return Complex(real(self) + real(other), imag(self) + imag(other))
    

def main():
    a = Complex(1.0, 2.0)
    b = Complex(0.5, 3.0)
    c = Complex(1, 2.0)
    d = a + b

"""

source = """

class Range:
    def __init__(start, finish, step):
        self.i = start
        self.finish = finish
        self.step = step
        
    def __set_i__(i):
        self.i = a = i
        
    def __get_i__():
        return self.i
        
    def __get_step__():
        return self.step
        
    def __next__():
        r = self.i
        self.i = self.i + self.step
        return r

def main():
    r = Range(0, 10, 1)
    
    n = next(r)
    

"""


def flatten(l):
    r = []
    if type(l) is list:
        for item in l:
            r.extend(flatten(item))
        return r
    else:
        return [l]

print(mangler.Mangle("__add__", mangler.Function([m_types.Floating()])))

utils.analysis(source)

