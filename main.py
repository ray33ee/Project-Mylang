import symtable
import ast

import ir
import members
import sugar
import utils
import errors
import symbol_table
import custom_unparser
import mangler
import m_types

source = """


class Test:
    def __init__():
        self.a = 0
        
    def __get_a__():
        return self.a
        
    def __set_a__(a):
        self.a = a
    
    def get():
        return self.a
        
    def set(a):
        self.a = a
        
    def me():
        return self
    
    def test():
        return -a

def main():
    c = Test()
    d = c.me()
"""

source = """


class Complex:
	def __init__(realz, imagz):
		self.real = realz
		self.imag = imagz
		
	def __get_real__():
	    return self.real
		
	def __get_imag__():
	    return self.imag
	
	def __real__():
	    return self.real
	
	def __imag__():
	    return self.imag

	def __add__(rhs):
		return Complex(real(self) + real(rhs), imag(self) + imag(rhs))


def main():
	c1 = Complex(1, 2)
	c2 = Complex(1.0, 2.0)

	c3 = c2 + c1

	c4 = c1 + 5

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
    n_1 = next(r)
    

"""

source = """

class Test():
    def __init__():
        self.x = f()
        
    def __get_x__():
        return self.x
        
    def __call__():
        return True

def f():
    return g(("hello", 3.4))

def g(i):
    return i

def main():
    a = Test()
    x = a.x
    y = a()
    a = Test()
    a = 55
    b = 4
    
    b = b + 4
    
    u = g(1)
    v = g(2)
    l = g(3.4)

"""

source = """

def f(x):
    return x
    
def main():
    a = f(1)
    b = f(2)
    c = f(True)

"""

source = """

class Test():
    def __init__():
        self.x = f()
        
    def __get_x__():
        return self.x
    
def f():
    return 4

def main():
    a = Test()
    b = Test()
    c = a.x

"""

utils.analysis(source)
