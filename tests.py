
import logging

logger = logging.getLogger(__name__)

test_sources = [

    ("""
    
def main():
    print("Hello world!")
    
    """, b'Hello world!\n'),

    ("""

def main():
    print(1+1)
    
    """, b'2\n'),

    ("""
    
def main():
    a = b = 2.5
    c = 7
    print(a + b + c)
    
    """, b'12\n'),

    ("""
    
class Float:
    def __init__(x):
        self.x = float(x)
    
    def __init__():
        self.x = 0.0
        
    def __get_x__():
        return self.x
        
    def __float__():
        return self.x
        
    def __add__(other):
        return Float(self.x + float(other))
    
    def __push_fmt__(s, conversion):
        self.x.__push_fmt__(s, conversion)
        
        
        
def main():

    four = Float(4)
    zero = Float(0.0)
    one = Float(True)
    
    print(four)
    print(zero)
    print(one)
    
    nine = four + four + one
    
    print(nine)
    
    still_four = four + zero
    
    print(still_four)
    
    """, b'4\n0\n1\n9\n4\n'),

    ("""
    
def main():
    l = [4.1]
    print(l[0])
    
    """, b'4.1\n'),

    ("""
    
class Me:
    def __init__():
        self.x = 0
        
    def __get_x__():
        return self.x
        
    def me():
        return self
    
def main():
    m = Me()
    
    print(m.x)
    
    n = m.me()
    
    print(n.x)
    
    """, b'0\n0\n'),

    ("""

def main():
    a = b = 100
    c = "yes"
    x = f"a: {a}, b+1: {b+1}, c: {c}, nested_format: {f"is this even legal? {b}"}"
    
    print(x)
    
    """, b'a: 100, b+1: 101, c: yes, nested_format: is this even legal? 100\n'),

    ("""
    
def f(x):
    return some(x)

def main():
    y = f(5).unwrap()
    
    print(y)
    
    """, b'5\n'),

    ("""
    
class Range:
        
    def __init__(end):
        self.i = 0
        self.end = end
        self.step = 1
        
    def __init__(start, end):
        self.i = start
        self.end = end
        self.step = 1
        
    def __init__(start, end, step):
        self.i = start
        self.end = end
        self.step = step
        
    
    def __get_i__():
        return self.i
    
    def __get_end__():
        return self.end
    
    def __get_step__():
        return self.step
        
    def __set_i__(i):
        self.i = i
        
    def __iter__():
        return self
    
    def __next__():
        if self.i >= self.end:
            return None
        
        i = self.i
        tmp = self.i + self.step
        self.i = tmp
        return some(i)

def main():
    
    for i in Range(3):
        print(i)
    
    for i in Range(3, 6):
        print(i)
    
    for i in Range(7, 14, 2):
        print(i)

    """, b'0\n1\n2\n3\n4\n5\n7\n9\n11\n13\n'),

    ("""
    
class Integer:
    def __init__(x):
        self.x = int(x)
    
    def __init__():
        self.x = 0
    
    def __get_x__():
        return self.x    
    
    def __int__():
        return self.x
        
    def __zero__():
        return Integer()
        
    def __one__():
        return Integer(1)
    
    def __add__(other):
        return Integer(self.x + int(other))
    
    def __ge__(other):
        return self.x >= int(other)
    
    def __push_fmt__(s, c):
        self.x.__push_fmt__(s, c)
    
class Range:
        
    def __init__(end):
        self.i = zero(end)
        self.end = end
        self.step = one(end)
        
    def __init__(start, end):
        self.i = start
        self.end = end
        self.step = one(start)
        
    def __init__(start, end, step):
        self.i = start
        self.end = end
        self.step = step
    
    def __get_i__():
        return self.i
    
    def __get_end__():
        return self.end
    
    def __get_step__():
        return self.step
        
    def __set_i__(i):
        self.i = i
        
    def __iter__():
        return self
    
    def __next__():
        if self.i >= self.end:
            return None
        
        i = self.i
        tmp = self.i + self.step
        self.i = tmp
        return some(i)

def main():
    
    for i in Range(Integer(3)):
        print(i)
    
    for i in Range(Integer(3), Integer(6)):
        print(i)
    
    for i in Range(Integer(7), Integer(14), Integer(2)):
        print(i)

    """, b'0\n1\n2\n3\n4\n5\n7\n9\n11\n13\n'),

    ("""
    
def main():
    l = []
    l.append(3)
    print(l[0])
    
    """, b'3\n'),

    ("""
    
class SimpleRange:
    def __init__(max):
        self.x = 0
        self.max = max
    
    def __get_x__():
        return self.x
    
    def __get_max__():
        return self.max
        
    def __set_x__(x):
        self.x = x
        
    def __iter__():
        return self
    
    def __next__():
        if self.x >= self.max:
            return None
        
        x = self.x
        tmp = self.x + 1
        self.x = tmp
        return some(x)

def main():
    it = SimpleRange(10)
    
    for i in SimpleRange(10):
        print(i)

    """, b'0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n'),

    ("""


def main():
    l = [1, 2, 3, 4, 5, 6, 7]
    
    s = ContainerSlice(l, 2, 5, 1)
    
    s_1 = ContainerSlice(s, 1, 2, 1)
    
    for a in ContainerIterator(l):
        print(a)
    
    for a in ContainerIterator(s):
        print(a)
    
    for a in ContainerIterator(s_1):
        print(a)
    

    """, b'1\n2\n3\n4\n5\n6\n7\n3\n4\n5\n4\n'),

    ("""
    
class ListWrapper:
    def __init__(l):
        self.l = l
    
    def __get_l__():
        return self.l
    
    def __hash__(hasher):
        for item in ContainerIterator(self.l):
            hash(item, hasher)
        
    
    
def main():
    h = Hasher()
    
    h.write(100)
    h.write(4.5)
    h.write("hello world!")
    h.write(byte_array())
    
    print(h.finalise())
    
    t = Hasher()
    
    l = ListWrapper([1, 2, 3, 4])
    
    hash(l, t)
    
    print(t.finalise())
    
    """, None)



]

