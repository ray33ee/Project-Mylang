
import utils
import logging
import sys

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
        self.i = i
        
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


class Wrapper:
    def __init__():
        self.l = []
        
    def __get_l__():
        return self.l
    
    def app(x):
        self.l.append(x)
        
def f(x):
    return x

def main():
    
    a = Wrapper()
    
    b = a.l
    
    f(b)
    
    a.app(4)
    
    

"""

source = """

class Range:
    def __init__(length):
        self.index = zero(length)
        
    def __get_index__():
        return self.index
    
    def __set_index__(value):
        self.index = value
        
    def __iter__():
        return self
        
    def __next__():
        r = self.index
        self.index = self.index + one(self.index)
        return r


def f(x):
    return x

def main():
    r = Range(44)
    
    l = iter(r)
    
    for n in l:
        f(n)
    

"""

source = """

class Test:
    def __init__(x):
        self.x = float(x)

def f(x):
    return x

def main():
    t = Test(88)
    l = Test(44.0)
    
    f(t)

"""

source1 = """

def f(x):
    return x

def main():
    l = []
    l.append(3)
    x = l[0]
    f(l)
    
    y = float(x)

"""

source1 = """

def main():
    a = b = c = 1
    x = y = 2

"""

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

utils.analysis(source)

