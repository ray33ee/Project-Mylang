
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

""", b'4\n0\n1\n9\n4\n')

]

def run_tests():
    import utils

    for source, expected_output in test_sources:
        #source, expected_output = test_sources[-1]
        utils.analysis(source, True, expected_output)

    logger.debug(f"All {len(test_sources)} test passed")
