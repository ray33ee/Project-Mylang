
import logging

logger = logging.getLogger(__name__)

test_sources = [

"""


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
""",

"""

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

""",

"""

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


""",

"""

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

""",

"""

def f(x):
    return x

def main():
    a = f(1)
    b = f(2)
    c = f(True)

""",

"""


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



""",

"""

class Range:
    def __init__(length):
        self.index = zero(int(length))

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


""",

"""

class Test:
    def __init__(x):
        self.x = float(x)

def f(x):
    return x

def main():
    t = Test(88)
    l = Test(44.0)

    f(t)

""",

"""

def main():
    a = b = c = 1
    x = y = 2
    f = 4.0
    g = True

""",

"""

class Test:
    def __init__():
        self.x = 0

    def __get_x__():
        return self.x

def main():
    t = Test()
    a = t.x

""",

"""

def f(x):
    return x

def main():
    l = []
    v = []
    x = l[0]
    l.append(v)
    v.append(3)

    f(x)
    f(l)
    f(v)



""",

"""

def f(x):
    return x

def main():
    l = []
    x = l[0]

    f(x)

    x.append(4)


    l.append([])

""",

"""

def f(x):
    return x

def main():
    l2 = []
    l1 = []
    
    
    a = l1[0]
    b = l2[0]
    
    f(a)
    f(b)
    
    c = a + b
    
    f(c)
    
    l2.append(12.0)
    l1.append(12.0)
    

""",

"""


def main():
    print("Hello world!")

""",

"""

class Float:

    def __init__(x):
        self.x = float(x)
    
    def __get_x__():
        return self.x
        
    def __float__():
        return self.x
        
    def __add__(other):
        return Float(self.x + float(other))
        
    def me():
        return self
        
def main():
    a = Float(100)
    c = a + 12
    d = a + c
    f = d + 13.0

""",

"""

class Test():
    def __init__():
        self.x = f()

    def __get_x__():
        return self.x

    def __call__():
        return True

def f():
    return g((True, 3.4))

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

""",

"""


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
		return Complex(self.real + real(rhs), self.imag + imag(rhs))


def main():
	c1 = Complex(1, 2)
	c2 = Complex(1.0, 2.0)

	c3 = c2 + c1

	c4 = c1 + 5
	
	a = 1
	b = 1.0
	
	c = str(a)
	d = str(b)
	
	print(c)
	print(d)


""",

"""

def main():
    x = 1
    y = True
    a = f"hello {x+1} and {y}" 

"""

]

def run_tests():
    import utils

    for source in test_sources:
        utils.analysis(source, False)

    logger.debug(f"All {len(test_sources)} test passed")
