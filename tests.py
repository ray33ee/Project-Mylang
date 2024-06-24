
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
    l = []
    l.append(3)
    print(l[0])
    
    """, b'3\n'),

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

]

def run_tests():
    import utils

    for source, expected_output in test_sources:
        #source, expected_output = test_sources[-1]
        utils.analysis(source, True, expected_output)

    logger.debug(f"All {len(test_sources)} test passed")
