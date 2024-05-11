
# Introduction

To allow templated functions and classes, and to prevent naming conflicts, fuctions and class names are all mangled.

# Mangling

Mangling is the process of taking a templated function or templated class (i.e. functions and classes where the types are all filled out) and creating a string identifier. The grammar of mangled names is as follows:

mangled = \_Z\[scope\]\[body\]

scope = N\[pair\]+E

-- A single pair represents a length of an identifier then the identifier itself
pair = \[length\]\[identifier\]

body = \[function\] | \[class\]

function = F\[type\]*(R\[type\])?

-- used to describe classes in nested types
class = C\[total_length\]\[type\]*

-- Used to describe a mangled class
Class = C\[total_length\]\[scope\]\[type\]*

type = v 
| b 
| i 
| f 
| a 
| l\[type\] 
| u 
| m 
| d\[type\]\[type\] 
| s\[type\] 
| o\[type\] 
| r\[type\]\[type\] 
| \[Class\]

# Length

Length is a positive number as a string which represents the length (in characters) of the following string.

# Pair

A pair is a length, identifier_string tuple

# Body

The body of a mangled name can either be a function or a class and contains information about arguments and return value for functions, and fields for classes.

# Function

Function contains the function identifier `F`, a list of zero or more arguments, and an optional return value which is identified by `R` and the return value type

# Class

Class contains the class identifier `C` and a list of types for its fields.

# Types

- unit (v)
- bool (b)
- int (i)
- float (f)
- Id (a)
- List (l)
- String (u)
- Bytes (m)
- Dictionary (d)
- Set (s)
- Option (o)
- Result (r)
- User defined class (c)

# Examples

1. `def add(x: int, y: int) -> int` mangles to `_ZN3addEFiiRi`
1. `class Complex(x: float, y: float)` mangles to `_ZN7ComplexECff`
1. `class Complex(x: float, y: float)` mangles to `_ZN7ComplexECff`

