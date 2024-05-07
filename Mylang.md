
# Mylang 

Mylang is a language that looks like Python, but generates code more like Rust or Go. Statically typed, Strongly typed, duck typed with infered typing.

# Hello world!

```Python
def main():
	print("Hello world!")

```

Above is a hello world application that computes the roughly the following in rust (Note that def main is the program entry point and is required):

```Rust

fn main() {
	println!("Hello world!");
}

```

# Static typing

Mylang is statically typed but we use infered typing, see the following example:

```Python

def add(x, y):
	return x + y

def main():
	sum = add(2, 5)
	print(sum)
```

In the example the arguments passed to add are two integers, so `add` is implemented as such:

```Rust


fn add(x: i64, y: i64) -> i64 {
	return x + y
}

fn main() {
	let mut sum = add(2, 5);
	println!("{}", sum);
}


```

The function paramater types are deduced from usage. All variables are automatically set to mutable. Note how the return type of the `add` function is also deduced from the return call.

# Duck typing

Consider a custom class that implements the '\_\_str\_\_' function. This function, similar to the Python version, will convert the type to a string. We can create a function to take a value and convert it to a string. So we can use it as follows:

```Python

class Custom1:
	def __str__(self):
		return "Custom Class!"

class Custom2:
	def __str__(self):
		return "Custom Class 2!"

def convert_to_string(x):
	return str(x)

def main():
	c1 = Custom1()
	c2 = Custom2()

	print(convert_to_string(c1))
	print(convert_to_string(c2))

```

The ducktyping focuses on the `conver_to_string` method in the following way:

1. First we obtain a list of all calls to this function.
2. For each call, we identify the argument types for each paramater. In this example we have `Custom1` and `Custom2`.
3. Then we check the body of `convert_to_string` for any functions used on these paramaters. In this example we just have the `str` function which is syntactic sugar for  `x.__str__()` function.
4. If any of the functions called are not defined for the paramater, an error is thrown. This does not happen in this case as `__str__` is defined for `Custom1` and `Custom2`
5. Otherwise, one Rust function for each combination of different paramaters is made. In this example just two functions, one to take a `Custom1` and another for the `Custom2`

The output looks a little something like

```Rust

struct Custom1;

impl Custom1 {

	pub fn __init__() -> Self {
		return Custom1;
	}

	pub fn __str__(& mut self) -> & 'static str {
		return "Custom Class!";
	}
}

struct Custom2;

impl Custom2 {

	pub fn __init__() -> Self {
		return Custom2;
	}

	pub fn __str__(& mut self) -> & 'static str {
		return "Custom Class 2!";
	}
}

fn convert_to_string_Custom1(mut x: Custom1) -> & 'static str {
	return x.__str__();
}

fn convert_to_string_Custom2(mut x: Custom2) -> & 'static str {
	return x.__str__();
}

fn main() {
    let mut c1 = Custom1::__init__();
    let mut c2 = Custom2::__init__();
    
    println!("{}", convert_to_string_Custom1(c1));
    println!("{}", convert_to_string_Custom2(c2));
}

```

Some important side notes on the above example:

- Even though `__str__` doesn't use self and is a member function and NOT static because it is invoked as a member function (i.e. it is called as x.y not CLASS.y). To solve this we add the `& mut self` variable to the rust function to force Rust to treat it as a member function.
- Class constructors use `__init__` which is implemented as a static function in rust.
- Because `Custom1` and `Custom2` have no member variables, they must be implemented in rust as `struct Custom1;` and `struct Custom2;`
- When using static strings, we use `& 'static str`
- `__str__` must return a string to work correctly. However generally the return type is deduced.
- All the member variables used are declared in the constructor. If a mamber variable that was not instantiated in the constructor is used elsewhere, this is an error.
- Also everything is mutable by default. Sorry Rust :(

Finally, the `convert_to_string` function is only to demonstrate duck typing and is not actually needed. The `print` function automatically calls `__str__` on all built in types anyway, so 

```Python

class Custom1:
	def __str__(self):
		return "Custom Class!"

class Custom2:
	def __str__(self):
		return "Custom Class 2!"

def main():
	c1 = Custom1()
	c2 = Custom2()

	print(c1)
	print(c2)

```

would evaluate to

```Rust

struct Custom1;

impl Custom1 {

	pub fn __init__() -> Self {
		return Custom1;
	}

	pub fn __str__(& mut self) -> & 'static str {
		return "Custom Class!";
	}
}

struct Custom2;

impl Custom2 {

	pub fn __init__() -> Self {
		return Custom2;
	}

	pub fn __str__(& mut self) -> & 'static str {
		return "Custom Class 2!";
	}
}

fn main() {
    let mut c1 = Custom1::__init__();
    let mut c2 = Custom2::__init__();
    
    println!("{}", c1.__str__());
    println!("{}", c2.__str__());
}

```

# Function overloading

Functions can be overloaded provided there is no ambiguity between overloads:

```Python

class Custom3:
	def custom_function(self):
		print("Custom Class!")

	def custom_function(self, x):
		print(x)


def main():
	c3 = Custom3()

	c3.custom_function()
	c3.custom_function(200)

```

```Rust
struct Custom3;

impl Custom3 {
    pub fn __init__() -> Self {
        return Custom3;
    }
    
    pub fn custom_function(& mut self) {
        println!("Custom Class!");
    }
    
    pub fn custom_function_int(& mut self, x: i64) {
        println!("{}", x);
    }
}

fn main() {
    let mut c3 = Custom3::__init__();
    
    c3.custom_function();
    c3.custom_function_int(200);
}

```

# Rust Enums

We use rust enums because they are king:

```Python

enum Collection:
	None
	One(x)
	Many(y)

```

# By reference

While primitive built in and user defined types are instantiated on the stack and coopied when moved by value, built in containers and most user defined classes are instantiated on the heap and passed by reference:

```Python

def subtract_2(l):

	for i in range(len(l)):
		l[i] = l[i] - 2

	return l.copy()

def main():

	lst = [2, 5, 7, 2, 5]

	print(subtract_2(lst))
	print(lst)

```

```Rust

fn subtract_2(l: & mut Vec<i64>) -> Vec<i64> {
	for i in 0..l.len() { 
		l[i] = l[i] - 2;
	}

	return l.clone()
}

fn main() {
	let mut lst = vec![2, 5, 7, 2, 5];

	println!("{:?}", subtract_2(& mut lst));
	println!("{:?}", & mut lst);
}

```

# Rust Result

We use Rust error handling because exception based error handling is less than ideal. Instead we use Rust's error handling which is based on `Result` which is a special value that can either be `Ok` and have a sucess/return value associated with it, or `Err` indicating failure and have an error value. To return `Ok` we simply return a value as normal. To return an error we use the `error` function. The `error` function can take any value that implements the `__error__` function. By default, when a function returns a `Result` this result `unwraps`, returning the success value if succeeded, and panicing if there is an error. Take the following example:

```Python

def divide(a, b):
	if b != 0:
		return a/b
	else:
		return error("Divide by zero!")

def main():
	print(divide(3.0, 2.0))
	# print(divide(4.0, 0.0)) # Calling this function will cause a panic

```

```Rust

fn divide(a: f64, b: f64) -> Result<f64, & 'static str> {
	if b != 0.0 {
		return Ok(a / b);
	} else {
		return Err("Divide by zero!");
	}
}

fn main() {
	println!("{}", divide(3.0, 2.0).unwrap());
}


```

Mylang's static type inferance works by tracing all code paths in a function. If any one path returns a `error` then the return value is designated as `Result` and all other non-error values are wrapped in an `Ok`. As mentioned, by default, when a function that returns an `error` is called, unwrap is called on that function return value immediately. This on its own is not enough, as all `Results` will just panic. To allow actual error handling, we introduce a new statement shown below:

```Python

def divide(a, b):
	if b != 0:
		return a/b
	else:
		return error("Divide by zero!")

def divide_handler(a, b):
	ok divide(a, b) as dividend:
		print("{a} / {b} = {dividend}")
	err as e:
		print("divide error - {e}")

def main():
	divide_handler(2.0, 7.0)
	divide_handler(3.0, 0.0)

```

The line `ok divide(a, b) as dividend` can be interpreteed as 'if the divide call returns an ok, execute the following block with dividend as the result from the divide function'. The second block `err as e` can be interpreted as 'if the divide call returns err, execute the following block with e as the returned error'. The ok/err block is the only time where a function returning a result is not unwrapped straight away. See the following code for clarification:

```Rust

fn divide(a: f64, b: f64) -> Result<f64, & 'static str> {
	if b != 0.0 {
		return Ok(a / b);
	} else {
		return Err("Divide by zero!");
	}
}

fn divide_handler(a: f64, b: f64) {
	match divide(a, b) {
		Ok(dividend) => {
			println!("{} / {} = {}", a, b, dividend);
		}
		Err(e) => {
			println!("divide error - {}", e);
		}
	}
}

fn main() {
	divide_handler(2.0, 7.0);
	divide_handler(3.0, 0.0);
}

```

NOTE: I'm not really a fan of the ok/err syntax. I prefer something more generic like match that can be used for some/none.

# Variadic arguments?

Variadic arguments are allowed and are implemented the same(ish) way as they are in C. Argumments are implemented as a static list on the stack. Variadic argumments can be overloaded to specify different or more optimised behaviour for a set number of arguments. All variadic arguments must be the same type. Variadic arguments must be at the end of the list. Variadic arguments are accessed with the `__variadic__` list

```Python

def min(a):
	return a

def min(a, b):
	if a < b:
		return a
	else
		return b

def min(..):
	m = +inf
	for arg in __variadic__:
		if arg < m:
			m = arg

	return m

def main():
	print(min(2))
	print(min(3, 9))
	print(min(2, 6, 5, 9, 4))

```

```Rust

//Created from the single and double argument min calls
fn min___variadic___int(a: i64) -> i64 {
	return a;
}

fn min___variadic___int_int(a: i64, b: i64) -> i64 {
	if a < b {
		return a;
	} else {
		return b;
	}
}

//Generic function created by min(..)
fn min___variadic___ints(__variadic__: & [i64]) -> i64 {
	let mut m = i64::MAX;

	for arg in __variadic__ {
		if *arg < m {
			m = *arg;
		}
	}

	return m;
}

// Specific implementatio of min(2, 6, 5, 9, 4)
fn min___variadic___int_5() -> i64 {
	let __variadic__ = [2, 6, 1, 9, 4];
	return min___variadic___ints(&__variadic__);
}

fn main() {
	println!("{}", min___variadic___int(2));
	println!("{}", min___variadic___int_int(3, 9));
	println!("{}", min___variadic___int_5());
}

```

# String formatting

Think of a Rust-like way to format strings that isn't too bulky but is still powerful and efficient. Maybe something using `format` and `__format__`. Think of a way that doesn't keep concatenating or assigning new strings.

# Type table

Tabulate all types against trait functions and show which Rust functions they invoke, like so:

| Function | int (i64) | float (f64) | string (String) | bool (bool) | list (vec) | tuple | range (x..y) | set (HashSet) | dict (HashMap) |
|----------|-----------|-------------|-----------------|-------------|------------|-------|--------------|-----|------|
|\_\_str\_\_   | i64.to_string() | f64.to_sting() | String | bool.to_string() | dunno lol | dunno lol | "range(x, y)" | dunno | also dunno
|\_\_len\_\_   |    	   |             |  String.len     |             | vec.len    | compile time resolved | dunno lol | HashSet.len | HashMap.len|
|\_\_float\_\_ | i64 as f64 | return f64 | String.parse | bool.parse | | | | | |


When a function listed is called on a built in type, it is converted to Rust code via the table above.

# Classes

Note: While member variables can be infered, they must only have one type as this will be the types used by the Rust class. To show this, we show the following code which is valid:

```Python


class Point:

	def __init__(x, y):
		self.x = x
		self.y = y


def main():
	p = Point(7.5, 5.4)

```

because type inference shows that both `Point.x` and `Point.y` are floats (based on the call to `__init__`) but the following is not:

```Python
# THIS MYLANG CODE WILL NOT COMPILE

class Point:

	def __init__(x, y):
		self.x = x
		self.y = y


def main():
	p = Point(7.5, 5.4)
	q = Point(7, 5)

```

Because in the first call to the contructor both arguments are floats, however in the second constructor both are integers and there is no conversion, implicit or otherwise. We can solve this by modifying the contructor to convert the inputs to a float during assignment. This means that anything can be used to construct the `Point` as long as it has a `__float__` function. This gives the best of both worlds, it is clear that `Point` stores two floats, and yet we can supply non-float types as arguments at the small cost of having to explicitly call `float` on the arguments

```Python

class Point:

	def __init__(x, y):
		self.x = float(x)
		self.y = float(y)

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __str__(self):
		return "{self.x}i + {self.y}j"


def main():
	a = Point(1.7, 4.1)
	b = Point(3, 9)

	c = a + b

	print(a)
	print(b)
	print(c)

```

```Rust

struct Point {
	pub _x: f64, // Note the prefixed underscore to all member variables to avoid confusing Rust
	pub _y: f64,
}

impl Point {
	//Two constructors are called, on two floates and the other on two ints so we provide functions for both
	pub fn __init__float_float(x: f64, y: f64) -> Self {
		return Point {
			_x: x, //float(x) requires no conversion
			_y: y,
		}
	}

	pub fn __init__int_int(x: i64, y: i64) -> Self {
		return Point {
			_x: x as f64, //calling float(x) on an integer evaluates to 'x as f64'
			_y: y as f64,
		}
	}

	pub fn __add__(& mut self, other: & mut Self) -> Self {
		return Point::__init__float_float(self._x + other._x, self._y + other._y) // Here we use `__init__float_float` as this is deduced from the contructor call
	}

	pub fn __str__(& mut self) -> String {
		return format!("{}i + {}j", self._x, self._y);
	}
}

fn main() {
	let mut a = Point::__init__float_float(1.7, 4.1);
	let mut b = Point::__init__int_int(3, 9);

	let mut c = a.__add__(& mut b);

	println!("{}", a.__str__());
	println!("{}", b.__str__());
	println!("{}", c.__str__());
}


```

# Getters and Setters

Getters can be implemented by adding `__get_NAME__` and setters can be implemented by adding `__set_NAME__` to the class, where 'NAME' is the name of the variable. For example:

```Python

class PropertyTest:

	def __init__(a, b):
		self.a = str(a)
		self.b = str(b)

	def __set_a__(self, a):
		self.a = str(a)
		print("Setter - {self.a}")

	def __get_a__(self):
		print("Getter - {self.a}")
		return self.a

	def __repr__():
		return print("PropertyTest({self.a}, {self.b})")

def main():
	pt = PropertyTest("Hello", "world!")

	print(pt)

	pt.a = "Goodbye"

	print(a)

	print(pt)

	pt.b = "everyone"

	print(b)

	print(pt)




```

Because `__set_a__` and `__get_a__` are implemented for `PropertyTest`, whenever `a` is assigned or fetched, these functions are used instead. More generally, `object.name = value` is evaluated to `object.__set_name__(value)` if `__set_name__` is implemented for object. Similarly, `value = object.name` is evaluated to `value = object.__get_name__()` if `__get_name__` is implemented for object. If getters or setters are not implemented default implementatons are used instead. See the Rust output below:

```Rust

struct PropertyTest {
	pub _a: String,
	pub _b: String,
}

impl PropertyTest {
	pub fn __init__str_str(a: & 'static str, b: & 'static str) -> Self {
		return PropertyTest {
			_a: String::from(a), // We must convert static str to heap string
			_b: String::from(b),
		}
	}

	pub fn __set_a__str(& mut self, a: & 'static str) {
		self._a = String::from(a);
		println!("Setter - {}", self._a);
	}

	pub fn __get_a__(& self) -> & String {
		println!("Getter - {}", self._a);
		return &(self._a); 
	}

	pub fn __repr__(& self) -> String {
		return format!("PropertyTest({}, {})", self._a, self._b);
	}

}

fn main() {
	let mut pt = PropertyTest::__init__str_str("Hello", "world!");

	println!("{}", pt.__repr__());

	pt.__set_a__str("Goodbye");

	println!("{}", pt.__get_a__());

	println!("{}", pt.__repr__());

	pt._b = String::from("everyone");

	println!("{}", pt._b);

	println!("{}", pt.__repr__());

}

```

Getters and setters do not need to be implemented on member variables. For example

```Python

class Currency:
	def __init__(value):
		self.pennies = value

	def __get_pennies__():
		return self.pennies

	def __get_pounds__():
		return self.pennies / 100

def main():

	c = Currency(34)

	print("pennies: {c.pennies}, pounds: {c.pounds}")

```

is completely valid even though there is no member variable `self.pounds`, so 

# Some/None

Mylang contains the `None` keyword as a pairing with the `some` function. This works as it does in python. We can use `some(5)` or `None` to represent a present value of 5, or an absent value, respectively. The some/none statement can be used to extract the inner value if there is one, similar to using `match` in rust:

```Python

def first(x):
	if len(x) == 0:
		return None
	else:
		return some(x[0])

def test_first(x):
	some(val) as first(x):
		print("x contains a some({val})")
	none:
		print("x does not contain a value")


def main():
	test_first([10, 3, 14])
	test_first([])

```

```Rust

fn first(x: Vec<i64>) -> Option<i64> {
	if x.len() == 0 {
		return None;
	} else {
		return Some(x[0])
	}
}

fn test_first(x: Vec<i64>) {
	match first(x) {
		Some(val) => {
			println!("x contains some ({})", val);
		}
		None => {
			println!("x does not contain a value");
		}
	}
}

fn main() {
	test_first(vec![10, 3, 14]);
	test_first(vec![]);
}

```

# Privacy

By default, member variables are all public. However, prefixing the name with the double underscore ("\_\_") and making sure there are no trailing underscores, marks the variable as private. This means that it can only be accessed from within the class. Getters and setters can still be provided, but they can only be accessed from within the class too.

# Deduction problems?

Take the following example

```Python

def f():
	return 1

def f():
	return "hello"

def main():
	v = str(f())

```

It is impossible to determine which version of `f` is called since `str` is defined for integers and strings. Maybe the solution to this is NOT to allow function overloading by the user. Overloading should only be performed by the compiler for generating functions that take and return different types.

# Heap Vs Stack {#stackorheap}

Yes, I know, you hate the stack vs heap debate as much as I do. Here we follow a similar strategy to Python: Built-in primitives on the stack, everything else on the heap. The one exception to this is any user created types that behave like built-in primitives. That is, any user created types that are:

a) Simple - Types that do not contain any references (or any child objects) as this would be incompatible with copying and passing by value
b) Small - Types that are only a handful of machine words long. Larger types incur a larger overhead to copy when passing by value
c) Immutable - Immutable types cannot be modified so can be passed around by value and treated the same way as other types.

Stack types are passed by value and copied around, whereas heap types are passed by reference.

An example of a custom type that would be implemened on the stack is the `Point` class from the previous example, because:

a) it contains no references
b) it is only 2 floats long
c) It is immutable as none of the member functions alter the member variables. 

# Reference counting, cycles and the heap

As mentioned above, stack objects are passed by value and heap values are passed by reference. Heap values are reference counter to automatically free when no longer root accessible. This of course does not clean up cycles, so we have a special reference counted type that scans for and frees inacessible cycles. This more complex form of reference counting can free cycles, but comes with extra overhead that normal non-cycle types don't need. 

To solve this issue, the compiler scans all variables and class variables to determine if any of them have the capacity to form cycles. For types and variables that are definitely not part of cycles, regular reference counting is used. For any types and variables that MIGHT produce cycles, the special reference counting is used.

# Non-cyclic references

Take the following example and its translation to see how we handle simple references and heap objects:

```Python

def minus_2(l):
	for i in range(len(l)):
		l[i] = l[i] - 2

	return l

def main():
	test = [13, 5, 21, 8, 4]

	print(minus_2(l))
	print(l)

```

In the example, note that the only heap object is a list, and it is a list of integers, so is not cyclic.

```Rust 

use std::cell::{UnsafeCell, RefCell, Ref};
use dumpster::{Collectable, unsync::Gc};
use std::borrow::Borrow;
use std::rc::Rc;


// Reference counted cell type aliases for improved readability
type CellGc<T> = Gc<UnsafeCell<T>>;
type CellRc<T> = Rc<UnsafeCell<T>>;

// Functions used to obtain a mutable reference from an unsafe cell for improved readability
fn mut_ref_gc<T: Collectable>(t: & CellGc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

fn mut_ref_rc<T>(t: & CellRc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

// Functions to create new CellGc and CellRc objects for improved readability
fn new_gc<T: Collectable>(t: T) -> CellGc<T> {
    Gc::new(UnsafeCell::new(t))
}

fn new_rc<T>(t: T) -> CellRc<T> {
    Rc::new(UnsafeCell::new(t))
}

fn minus_2(l: CellRc<Vec<u64>>) -> CellRc<Vec<u64>> {
    for i in 0..(*mut_ref_rc(&l)).len() {
        mut_ref_rc(&l)[i] = mut_ref_rc(&l)[i] - 2;
    }
    return l.clone();
}

fn main() {

    let test = new_rc(vec![13, 5, 21, 8, 4]);

    println!("{:?}", mut_ref_rc(&minus_2(test.clone())));
    println!("{:?}", mut_ref_rc(&test));

}

```

See how `test` is implemented as a reference counted heap object.

# Cycles

In this example, we give a simple cyclic reference that uses the advanced reference counter to clean up:

```Python

class A:
	def __init__(b):
		self.a = b

class B:
	def __init__():
		self.b = None

	def set_b(self, a):
		self.b = some(a)

def link():
	b = B()

	a = A(b)

	b.set_b(a)

	# At this point a and b form a cyclic reference

def main():
	link()

```

```Rust


use std::cell::{UnsafeCell, RefCell, Ref};
use dumpster::{Collectable, unsync::Gc};
use std::borrow::Borrow;
use std::rc::Rc;


// Reference counted cell type aliases for improved readability
type CellGc<T> = Gc<UnsafeCell<T>>;
type CellRc<T> = Rc<UnsafeCell<T>>;

// Functions used to obtain a mutable reference from an unsafe cell for improved readability
fn mut_ref_gc<T: Collectable>(t: & CellGc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

fn mut_ref_rc<T>(t: & CellRc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

// Functions to create new CellGc and CellRc objects for improved readability
fn new_gc<T: Collectable>(t: T) -> CellGc<T> {
    Gc::new(UnsafeCell::new(t))
}

fn new_rc<T>(t: T) -> CellRc<T> {
    Rc::new(UnsafeCell::new(t))
}

#[derive(Collectable)]
struct A {
    a: CellGc<B>,
}

impl A {
    fn new(a: CellGc<B>) -> Self {
        return A {
            a,
        };
    }
}

#[derive(Collectable)]
struct B {
    b: Option<CellGc<A>>,
}

impl B {
    fn new() -> Self {
        return B {
            b: None,
        };
    }

    fn set_b(& mut self, b: CellGc<A>) {
        self.b = Some(b);
    }
}

fn link() {
    let mut b = new_gc(B::new());

    let mut a = new_gc(A::new(b.clone()));

    mut_ref_gc(&b).set_b(a.clone());
}

fn main() {

    link();

}

```

The compiler recognises that `A` and `B` are at risk of forming cyclic references, so we use `Gc` to reference count and check cycles.

# Mixed approach

Objects that point into a cycle can be normal reference counted. And objects in a cycle can point to normal reference counted objects. This means that we can maximise the use of normal, fast reference counting. See the following example:



# Realistic example

The examples above are useful, but a bit abstract. Here we create a parent/child system with a manager class that holds the parent:

```Python

class Child:
	def __init__(parent, id):
		self.parent = parent
		self.id = id

	def __str__(self):
		return str(self.id)

class Parent:
	def __init__():
		self.children = []

	def add_child(self, child):
		self.children.append(child)

class Manager:
	def __init__(head):
		self.head = head

	def kids(self):
		return self.head.children

def main():
	p = Parent()

	m = Manager(p)

	c_1 = Child(p, 1)
	c_2 = Child(p, 2)
	c_3 = Child(p, 3)

	p.add_child(c_1)
	p.add_child(c_2)
	p.add_child(c_3)

	for child in m.kids():
		print(child)

```

```Rust 

use std::cell::{UnsafeCell, RefCell, Ref};
use dumpster::{Collectable, unsync::Gc};
use std::borrow::Borrow;
use std::rc::Rc;

// Reference counted cell type aliases for improved readability
type CellGc<T> = Gc<UnsafeCell<T>>;
type CellRc<T> = Rc<UnsafeCell<T>>;

// Functions used to obtain a mutable reference from an unsafe cell for improved readability
fn mut_ref_gc<T: Collectable>(t: & CellGc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

fn mut_ref_rc<T>(t: & CellRc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

// Functions to create new CellGc and CellRc objects for improved readability
fn new_gc<T: Collectable>(t: T) -> CellGc<T> {
    Gc::new(UnsafeCell::new(t))
}

fn new_rc<T>(t: T) -> CellRc<T> {
    Rc::new(UnsafeCell::new(t))
}


#[derive(Collectable)]
struct Child {
    parent: CellGc<Parent>,
    id: u64,
}

impl Child {
    fn __init__(parent: CellGc<Parent>, id: u64) -> Self {
        return Child {
            parent,
            id,
        };
    }

    fn __str__(& mut self) -> String {
        return format!("{}", self.id);
    }
}

#[derive(Collectable)]
struct Parent {
    children: CellGc<Vec<CellGc<Child>>>, // Vecs must be wrapped in a rc, and it is a vector of rc children. got it?
}

impl Parent {
    fn __init__() -> Self {
        return Parent {
            children: new_gc(Vec::new()),
        };
    }

    fn add_child(& mut self, child: CellGc<Child>) {
        mut_ref_gc(&self.children).push(child);
    }
}

struct Manager {
    head: CellGc<Parent>,
}

impl Manager {
    fn __init__(head: CellGc<Parent>) -> Self {
        return Manager {
            head,
        }
    }

    fn kids(& mut self) -> CellGc<Vec<CellGc<Child>>> {
        mut_ref_gc(&self.head).children.clone()
    }
}

fn main() {

    let mut parent = new_gc(Parent::__init__());

    let mut manager = new_rc(Manager::__init__(parent.clone()));

    let mut c_1 = new_gc(Child::__init__(parent.clone(), 1));
    let mut c_2 = new_gc(Child::__init__(parent.clone(), 2));
    let mut c_3 = new_gc(Child::__init__(parent.clone(), 3));

    mut_ref_gc(&parent).add_child(c_1.clone());
    mut_ref_gc(&parent).add_child(c_2.clone());
    mut_ref_gc(&parent).add_child(c_3.clone());

    let thing = mut_ref_gc(&parent);
    let thing2 = mut_ref_gc(&parent);


    for child in mut_ref_gc(&mut_ref_rc(&manager).kids()).iter() {
        println!("{}", mut_ref_gc(child).__str__());
    }
}

```


# Fallbacks

Dynamic ducktyping allows for fallbacks by testing if an object implements a function then making decisions on these tests. For example, in python the `__str__` provides a function that is used to represent an object as a string. However, if this function is not defined, `__repr__` is used as a fallback. To fascilitate this, we allow multiple functions with the same signature and return value to be defined. For a given call, the compiler will try each of these functions until it finds one that works for the arguments:

```Python

def to_string(x):
	return str(x)

def to_string(x):
	return repr(x)

```

In the above example, when `to_string` is called on a parameter, say named `y`, the compiler will first try the first implementation. It will test any functions called on `y` to make sure they hold. The only function is `str` and this is implemented as calling the object's `__str__`, so if it is defined, `str` is defined and therefore so is `to_string`, so a `to_string` is created to accept `y` as an argument. If however this first implementation is not compatible with `y` it tries the next. If all functions are not compatible a compile time error is produced. 

In the example above the compiler tries the functions in the order they are written. A different order can be specified with `@fallback n`:

```Python

@fallback 2
def to_string(x):
	return str(x)

@fallback 1
def to_string(x):
	return repr(x)

```

in the above example the order is reversed. 

# Special functions

Special functions work similarly to how they work in Python, and some of them have arguments or return values with explicit types. If these explicit types are not respected when implementing special functions on custom classes, this is an error.

# Dictionaries

Dictionaries with mutable keys is a logic error. To avoid this, we take a similar approach to python. There are three cases:

- Stack objects: Stack objects are copied into the map and their hashes are computed over all fields.
- Built in heap objects:
	- mutable: Cannot be used in hash maps. A compile time error will be produced
	- immutable: These are a special variant of the usual list, string, etc. that are immutable and specifically created for use in hash keys. Objects are copied by reference and hashes are computed for each item in the collection.
- User defined heap objects: Objects are copied by reference and the hash is computed on the reference itself.

Another note for dictionaries is that any map that is a) known at compile time and b) immutable can be implemented as a phf via the `Rust-PHF` crate.

# Serde

Serialisation and deserialisation similar to Rust Serde crate. Special functions `__se__` and `__de__` can be used to convert an object to bytes, and use a stream of bytes to instantiate objects, respectively. 

# Read/Write

Functions similar to how they work in Rust, `__read__` and `__write__`

# Id

Every object has the `id` function that returns the address of the object as a special type `Id` (which is implemented as `usize`). We have special functions for RC and GC that obtain unique references pointing to the heap. For stack variables we can do something like transmute.

# Paths

Use a `__path__` function in calls like `open()` to convert objects to path objects of type `Path` which is the same as Rust's `std::path::Path`. By default, `__path__` calls `__str__` and converts it into a path object.

# Drop

Use `__del__` to call the objects destructor via Rust's drop interface.

# Complex numbers

Complex numbers are implemented with the `complex` class which exposes two special functions, `__real__` and `__imag__` that return the real and imaginary parts of the complex number, respectively. Floats, ints and other real number values expose `__real__` (which returns the number) and `__imag__` (which returns 0), since these numbers are complex numbers with imaginary part 0. Note: Complex numbers do not implement `__float__`, `__int__` or `__index__`

# Profiling, testing and benchmarking

Yes, yes and yes, all built in.

# Compiler checks

- Inferring types from literal values and return types
- Constructing overloaded functions for each call
- Checking that types have the functions that we call via duck typing
- Checking for classes that are at risk of producing cycles
- Checking for variables that are at risk of producing cycles
- Check for any mutable call to a built in collection inside iteration (avoiding iterator invalidation)
- Make sure the mutable built in collections are never used as keys in dictionaries
- Figure out whether custom types are mutable or immutable. If class fields are never changed (eitehr by internal functions or externally accessing fields) the class is immutable. Otherwise it is mutable.

# Returning object references

Take the following

```Python

class A:
	def __init__(self):
		self.list = []

	def append(self, value):
		self.list.append(value)

	def __str__(self):
		str(self.list)

def make():
	a = A()

	a.append(55)

	return a

def main():
	print(make())

```

instead of returning a clone of `a` (if we returned a clone then the reference count would be incremented when we clone, and decremented when `a` falls out of scope) we just return `a` itself:

```Rust


// Reference counted cell type aliases for improved readability
type CellGc<T> = Gc<UnsafeCell<T>>;
type CellRc<T> = Rc<UnsafeCell<T>>;

// Functions used to obtain a mutable reference from an unsafe cell for improved readability
fn mut_ref_gc<T: Collectable>(t: & CellGc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

fn mut_ref_rc<T>(t: & CellRc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}

// Functions to create new CellGc and CellRc objects for improved readability
fn new_gc<T: Collectable>(t: T) -> CellGc<T> {
    Gc::new(UnsafeCell::new(t))
}

fn new_rc<T>(t: T) -> CellRc<T> {
    Rc::new(UnsafeCell::new(t))
}

//Get the IDs of gc and rc objects
fn gc_id<T: Collectable>(t: & CellGc<T>) -> usize {
    return Gc::<_>::as_id(t);
}

fn rc_id<T: Collectable>(t: & CellRc<T>) -> usize {
    return Rc::<_>::as_ptr(t) as usize;
}

struct A {
    list: CellRc<Vec<i64>>,
}

impl A {
    fn __init__() -> Self {
        return A {
            list: new_rc(vec![]),
        };
    }

    fn append(& self, value: i64) {
        mut_ref_rc(&self.list).push(value);
    }

    fn __str__(& self) -> String {
        format!("{:?}", mut_ref_rc(&self.list))
    }
}

fn make() -> CellRc<A> {
    let mut a = new_rc(A::__init__());

    mut_ref_rc(&a).append(55);

    return a;
}

fn main() {
    println!("{}", mut_ref_rc(&make()).__str__())
}

```

# Python's AST

## Type inferance

Whenever we assign to a value we look to the expression to determine the type. Assignments can come in many forms:

- `x = 2`: Here we can deduce the type of the LHS by seeing the type of the RHS. 
- `for a in b`: This example is slightly more complex. Here we need to determine the type of `a` based on `b`. `b` must have `__iter__` defined, and this iter must have a `__next__` function. `__next__` returns `Option<T>` for some type `T`, and its this type that belongs to our variable `a`.
- some/none and ok/err matching statements: Based on the return value from the values passed to the match statements.

For each assignment, we look to the targets (LHS of assignment) and we identify them by scope (this allows two variables of the same name to be treated separately if they are in separate scopes), then we look at the expression (RHS of assignment) and treat the targets type as the same as the assignment.

## Stack or Heap

For every user defined class, we must decide at compile time whether class instances will exist on the stack or heap. To do this we test for the conditions outlined [here](#stackorheap). Here we outline more rigorous requirements:

a) No references - The user defined class must not contain references to other user defined class, or built in containers that exist on the heap. 
b) Small - The size, in bytes, of the user defined class must be less than some threshold.
c) Immutable - To be immutable, assignment of member variables must ONLY happen within the `__init__` call. Assignments in member functions, or on public fields outside the class will result in the class being marked as a mutable type.

If all three of these requirements are met, the class is marked as a stack object and is moved around by value. In Rust we implement the copy trait for these objects.

## RC or GC

After type inferrance has been completed, the compiler can walk over all types that can contain references (built in containers and user defined types) and follows any fields or elements that contain references. If cycles are found, all variables involved are allocated using GC. Otherwise RC is used.

## Mylang AST

The Mylanf AST is similar to the Python AST, but it excludes things like with statements, match statements and error handling statements and incudes extra statically obtained information (type, heap or stack, RC or GC) and other statements like the some/none and the ok/err.

For all variables, the AST contains extra information on top of the information in the Python AST including:

- Stack or Heap: Indicator stating whether the type is declared on the stack or heap, as defined by the rules above
- RC or GC: Does the variable use normal reference counting (via Rust's std) or does it use RC with cycle detection (using dumpster)

We also include extra statements:

- some/none: some_none(expr value, expr target, stmt* some_body, stmt* none_body) where value is the expression contained the `Option`, target is the some inner value, some_body is the body of the some arm, and none_body is the body of the none arm.
- ok/err: ok_err(Call value, expr ok_target, expr err_target, stmt* ok_body, stmt* err_body) where value is a function call returning a `Result`, ok_target is the `Ok` inner value, err_target is the `Err` value, ok_body is the body of the ok arm, and err_body is the body of the err arm.

# Mylang Grammar

Mylang grammar is as follows:



<pre><span></span><span class="c c-Singleline">-- ASDL's 4 builtin types are:</span>
<span class="c c-Singleline">-- identifier, int, string, constant</span>

<span class="k">module</span> <span class="nt">Mylang</span>
<span class="p">{</span>
    <span class="n">stmt</span> <span class="o">=</span> <span class="nc">FunctionDef</span><span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">name</span>, <span class="bp">arguments</span><span class="o"> </span><span class="n">args</span>,
                       <span class="bp">stmt</span><span class="o">* </span><span class="n">body</span>, <span class="bp">expr</span><span class="o">* </span><span class="n">decorator_list</span>, <span class="bp">expr</span><span class="o">? </span><span class="n">returns</span>,
                       <span class="bp">string</span><span class="o">? </span><span class="n">type_comment</span>, <span class="bp">type_param</span><span class="o">* </span><span class="n">type_params</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">ClassDef</span><span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">name</span>,
             <span class="bp">keyword</span><span class="o">* </span><span class="n">keywords</span>,
             <span class="bp">stmt</span><span class="o">* </span><span class="n">body</span>,
             <span class="bp">expr</span><span class="o">* </span><span class="n">decorator_list</span>,
             <span class="bp">type_param</span><span class="o">* </span><span class="n">type_params</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">Return</span><span class="p">(</span><span class="bp">expr</span><span class="o">? </span><span class="n">value</span><span class="p">)</span>

          <span class="o">|</span> <span class="nc">Assign</span><span class="p">(</span><span class="bp">expr</span><span class="o">* </span><span class="n">targets</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">value</span>, <span class="bp">string</span><span class="o">? </span><span class="n">type_comment</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">AugAssign</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">target</span>, <span class="bp">operator</span><span class="o"> </span><span class="n">op</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">value</span><span class="p">)</span>
          <span class="c c-Singleline">-- 'simple' indicates that we annotate simple name without parens</span>
          <span class="o">|</span> <span class="nc">AnnAssign</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">target</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">annotation</span>, <span class="bp">expr</span><span class="o">? </span><span class="n">value</span>, <span class="bp">int</span><span class="o"> </span><span class="n">simple</span><span class="p">)</span>

          <span class="c c-Singleline">-- use 'orelse' because else is a keyword in target languages</span>
          <span class="o">|</span> <span class="nc">For</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">target</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">iter</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">body</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">orelse</span>, <span class="bp">string</span><span class="o">? </span><span class="n">type_comment</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">While</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">test</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">body</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">orelse</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">If</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">test</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">body</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">orelse</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">SomeNone</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">value</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">target</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">some_body</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">none_body</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">OkErr</span><span class="p">(</span><span class="bp">Call</span><span class="o"> </span><span class="n">value</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">ok_target</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">err_target</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">ok_body</span>, <span class="bp">stmt</span><span class="o">* </span><span class="n">err_body</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">Assert</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">test</span>, <span class="bp">expr</span><span class="o">? </span><span class="n">msg</span><span class="p">)</span>

          <span class="o">|</span> <span class="nc">Expr</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">value</span><span class="p">)</span>
          <span class="o">|</span> <span class="nc">Pass</span> <span class="o">|</span> <span class="nc">Break</span> <span class="o">|</span> <span class="nc">Continue</span>

          <span class="c c-Singleline">-- col_offset is the byte offset in the utf8 string the parser uses</span>
          <span class="nb">attributes</span> <span class="p">(</span><span class="bp">int</span><span class="o"> </span><span class="n">lineno</span>, <span class="bp">int</span><span class="o"> </span><span class="n">col_offset</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_lineno</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_col_offset</span><span class="p">)</span>

          <span class="c c-Singleline">-- BoolOp() can use left &amp; right?</span>
    <span class="n">expr</span> <span class="o">=</span> <span class="nc">BoolOp</span><span class="p">(</span><span class="bp">boolop</span><span class="o"> </span><span class="n">op</span>, <span class="bp">expr</span><span class="o">* </span><span class="n">values</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">BinOp</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">left</span>, <span class="bp">operator</span><span class="o"> </span><span class="n">op</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">right</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">UnaryOp</span><span class="p">(</span><span class="bp">unaryop</span><span class="o"> </span><span class="n">op</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">operand</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Lambda</span><span class="p">(</span><span class="bp">arguments</span><span class="o"> </span><span class="n">args</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">body</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">IfExp</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">test</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">body</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">orelse</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Dict</span><span class="p">(</span><span class="bp">expr</span><span class="o">* </span><span class="n">keys</span>, <span class="bp">expr</span><span class="o">* </span><span class="n">values</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Set</span><span class="p">(</span><span class="bp">expr</span><span class="o">* </span><span class="n">elts</span><span class="p">)</span>
         <span class="c c-Singleline">-- need sequences for compare to distinguish between</span>
         <span class="c c-Singleline">-- x &lt; 4 &lt; 3 and (x &lt; 4) &lt; 3</span>
         <span class="o">|</span> <span class="nc">Compare</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">left</span>, <span class="bp">cmpop</span><span class="o">* </span><span class="n">ops</span>, <span class="bp">expr</span><span class="o">* </span><span class="n">comparators</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Call</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">func</span>, <span class="bp">expr</span><span class="o">* </span><span class="n">args</span>, <span class="bp">keyword</span><span class="o">* </span><span class="n">keywords</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">FormattedValue</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">value</span>, <span class="bp">int</span><span class="o"> </span><span class="n">conversion</span>, <span class="bp">expr</span><span class="o">? </span><span class="n">format_spec</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">JoinedStr</span><span class="p">(</span><span class="bp">expr</span><span class="o">* </span><span class="n">values</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Constant</span><span class="p">(</span><span class="bp">constant</span><span class="o"> </span><span class="n">value</span>, <span class="bp">string</span><span class="o">? </span><span class="n">kind</span><span class="p">)</span>

         <span class="c c-Singleline">-- the following expression can appear in assignment context</span>
         <span class="o">|</span> <span class="nc">Attribute</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">value</span>, <span class="bp">identifier</span><span class="o"> </span><span class="n">attr</span>, <span class="bp">expr_context</span><span class="o"> </span><span class="n">ctx</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Subscript</span><span class="p">(</span><span class="bp">expr</span><span class="o"> </span><span class="n">value</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">slice</span>, <span class="bp">expr_context</span><span class="o"> </span><span class="n">ctx</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Name</span><span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">id</span>, <span class="bp">expr_context</span><span class="o"> </span><span class="n">ctx</span>, <span class="bp">topology</span><span class="o"> </span><span class="n">t</span>, <span class="bp">location</span><span class="o"> </span><span class="n">l</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">List</span><span class="p">(</span><span class="bp">expr</span><span class="o">* </span><span class="n">elts</span>, <span class="bp">expr_context</span><span class="o"> </span><span class="n">ctx</span><span class="p">)</span>
         <span class="o">|</span> <span class="nc">Tuple</span><span class="p">(</span><span class="bp">expr</span><span class="o">* </span><span class="n">elts</span>, <span class="bp">expr_context</span><span class="o"> </span><span class="n">ctx</span><span class="p">)</span>

         <span class="c c-Singleline">-- can appear only in Subscript</span>
         <span class="o">|</span> <span class="nc">Slice</span><span class="p">(</span><span class="bp">expr</span><span class="o">? </span><span class="n">lower</span>, <span class="bp">expr</span><span class="o">? </span><span class="n">upper</span><span class="p">)</span>

          <span class="c c-Singleline">-- col_offset is the byte offset in the utf8 string the parser uses</span>
          <span class="nb">attributes</span> <span class="p">(</span><span class="bp">int</span><span class="o"> </span><span class="n">lineno</span>, <span class="bp">int</span><span class="o"> </span><span class="n">col_offset</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_lineno</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_col_offset</span><span class="p">)</span>

    <span class="n">expr_context</span> <span class="o">=</span> <span class="nc">Load</span> <span class="o">|</span> <span class="nc">Store</span> <span class="o">|</span> <span class="nc">Del</span>

    <span class="n">boolop</span> <span class="o">=</span> <span class="nc">And</span> <span class="o">|</span> <span class="nc">Or</span>
    
    <span class="n">location</span> <span class="o">=</span> <span class="nc">Heap</span> <span class="o">|</span> <span class="nc">Stack</span>

    <span class="n">topology</span> <span class="o">=</span> <span class="nc">Cyclic</span> <span class="o">|</span> <span class="nc">Acyclic</span>

    <span class="n">operator</span> <span class="o">=</span> <span class="nc">Add</span> <span class="o">|</span> <span class="nc">Sub</span> <span class="o">|</span> <span class="nc">Mult</span> <span class="o">|</span> <span class="nc">MatMult</span> <span class="o">|</span> <span class="nc">Div</span> <span class="o">|</span> <span class="nc">Mod</span> <span class="o">|</span> <span class="nc">Pow</span> <span class="o">|</span> <span class="nc">LShift</span>
                 <span class="o">|</span> <span class="nc">RShift</span> <span class="o">|</span> <span class="nc">BitOr</span> <span class="o">|</span> <span class="nc">BitXor</span> <span class="o">|</span> <span class="nc">BitAnd</span> <span class="o">|</span> <span class="nc">FloorDiv</span>

    <span class="n">unaryop</span> <span class="o">=</span> <span class="nc">Invert</span> <span class="o">|</span> <span class="nc">Not</span> <span class="o">|</span> <span class="nc">UAdd</span> <span class="o">|</span> <span class="nc">USub</span>

    <span class="n">cmpop</span> <span class="o">=</span> <span class="nc">Eq</span> <span class="o">|</span> <span class="nc">NotEq</span> <span class="o">|</span> <span class="nc">Lt</span> <span class="o">|</span> <span class="nc">LtE</span> <span class="o">|</span> <span class="nc">Gt</span> <span class="o">|</span> <span class="nc">GtE</span> <span class="o">|</span> <span class="nc">Is</span> <span class="o">|</span> <span class="nc">IsNot</span> <span class="o">|</span> <span class="nc">In</span> <span class="o">|</span> <span class="nc">NotIn</span>

    <span class="n">arguments</span> <span class="o">=</span> <span class="p">(</span><span class="bp">arg</span><span class="o">* </span><span class="n">posonlyargs</span>, <span class="bp">arg</span><span class="o">* </span><span class="n">args</span>, <span class="bp">arg</span><span class="o">? </span><span class="n">vararg</span>, <span class="bp">arg</span><span class="o">* </span><span class="n">kwonlyargs</span>,
                 <span class="bp">expr</span><span class="o">* </span><span class="n">kw_defaults</span>, <span class="bp">arg</span><span class="o">? </span><span class="n">kwarg</span>, <span class="bp">expr</span><span class="o">* </span><span class="n">defaults</span><span class="p">)</span>

    <span class="n">arg</span> <span class="o">=</span> <span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">arg</span>, <span class="bp">expr</span><span class="o">? </span><span class="n">annotation</span>, <span class="bp">string</span><span class="o">? </span><span class="n">type_comment</span><span class="p">)</span>
           <span class="nb">attributes</span> <span class="p">(</span><span class="bp">int</span><span class="o"> </span><span class="n">lineno</span>, <span class="bp">int</span><span class="o"> </span><span class="n">col_offset</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_lineno</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_col_offset</span><span class="p">)</span>

    <span class="c c-Singleline">-- keyword arguments supplied to call (NULL identifier for **kwargs)</span>
    <span class="n">keyword</span> <span class="o">=</span> <span class="p">(</span><span class="bp">identifier</span><span class="o">? </span><span class="n">arg</span>, <span class="bp">expr</span><span class="o"> </span><span class="n">value</span><span class="p">)</span>
               <span class="nb">attributes</span> <span class="p">(</span><span class="bp">int</span><span class="o"> </span><span class="n">lineno</span>, <span class="bp">int</span><span class="o"> </span><span class="n">col_offset</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_lineno</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_col_offset</span><span class="p">)</span>

    <span class="c c-Singleline">-- import name with optional 'as' alias.</span>
    <span class="n">alias</span> <span class="o">=</span> <span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">name</span>, <span class="bp">identifier</span><span class="o">? </span><span class="n">asname</span><span class="p">)</span>
             <span class="nb">attributes</span> <span class="p">(</span><span class="bp">int</span><span class="o"> </span><span class="n">lineno</span>, <span class="bp">int</span><span class="o"> </span><span class="n">col_offset</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_lineno</span>, <span class="bp">int</span><span class="o">? </span><span class="n">end_col_offset</span><span class="p">)</span>

    <span class="n">type_ignore</span> <span class="o">=</span> <span class="nc">TypeIgnore</span><span class="p">(</span><span class="bp">int</span><span class="o"> </span><span class="n">lineno</span>, <span class="bp">string</span><span class="o"> </span><span class="n">tag</span><span class="p">)</span>

    <span class="n">type_param</span> <span class="o">=</span> <span class="nc">TypeVar</span><span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">name</span>, <span class="bp">expr</span><span class="o">? </span><span class="n">bound</span><span class="p">)</span>
               <span class="o">|</span> <span class="nc">ParamSpec</span><span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">name</span><span class="p">)</span>
               <span class="o">|</span> <span class="nc">TypeVarTuple</span><span class="p">(</span><span class="bp">identifier</span><span class="o"> </span><span class="n">name</span><span class="p">)</span>
               <span class="nb">attributes</span> <span class="p">(</span><span class="bp">int</span><span class="o"> </span><span class="n">lineno</span>, <span class="bp">int</span><span class="o"> </span><span class="n">col_offset</span>, <span class="bp">int</span><span class="o"> </span><span class="n">end_lineno</span>, <span class="bp">int</span><span class="o"> </span><span class="n">end_col_offset</span><span class="p">)</span>
<span class="p">}</span>
</pre>

# Compiler pipeline

Mylang source --> Preprocessor --> Python AST parse --> Static analysis --> Mylang AST --> ????? --> Rust source code

# Type deduction algorithm

When deducing types, it is not always immediately obvious what the types are. Take the following example

```Python

def add_2(x):
	return x + 2


def main():
	a = add_2(5)
	b = add_2(6.7)

```

when we look to the function `add_2` on its own, there is nothing indicating the type of `x` or the return value. The parameter `x` could be many different types, so instead of defining it by type we define by requrement. There is only the requirement that `x` implement `__add__(int)`. To show this we annotate variables we don't know the type of with a '%', so when we analyse the function on its own we have

```Python

def add_2(x: %1) -> %2:
	return x + 2

```

where the requirement for %1 is that it implements `__add__(int)`, and there is no requirement for %2. For variables that can only be one type, we use '$' notation. For example

```Python

def return_1():
	return 1

def main():
	x = return_1()

```

there is only one implementation of `return_1`, so the return value type is known:

```Python

def return_1() -> $1:
	return 1

def main():
	x: $2 = return_1()

```

Here is an example with both type variables and requirement variables:

```Python

def add_2(x):
	return x + 2


def main():
	a = add_2(5)
	b = add_2(6.7)

```

It is not clear from the function what type `x` is, so we must deduce it from calls:

```Python

def add_2(x: %1) -> %2:
	return x + 2


def main():
	a: $1 = add_2(5)
	b: $2 = add_2(6.7)

```

when we try the call to `add_2` we don't have any types for the argument or return value. So we must create a copy of `add_2` that takes `5` as its argument. We first test to make sure that the paramter passed, `5` satisfies the requrement of `%1` (in this case `5` must implement `__add__(int)`). It does, so we create a copy of `add_2` taking an integer as an argument. We can also use the full implementation of `__add__(int)` to know the return type of this new function, also int. We do this again with `6.7` as the argument and the result is similar except the argument and return value are both `float`. This results in an intermediate form looking like:

```Python

def add_2_int_int(x: int) -> int:
	return x + 2

def add_2_float_float(x: float) -> float:
	return x + 2


def main():
	a: $1 = add_2_int_int(5)
	b: $2 = add_2_float_float(6.7)

```

Note that for the add functions we have a) mangled the names and b) filled in the type variables with explicit types. We know these types because they were created from the previous step. Finally we can deduce the types `$1` and `$2` to give

```Python

def add_2_int_int(x: int) -> int:
	return x + 2

def add_2_float_float(x: float) -> float:
	return x + 2


def main():
	a: int = add_2_int_int(5)
	b: float = add_2_float_float(6.7)

```

The big question is, 'Can we deduce a functions argument and return types based on the body alone?'

## Mixed 

```Python

def minus_2(x):
	for i in range(len(x)):
		x[i] = x[i] - 2

```

we do not know the type of `x` from this, however because `range.__next__` returns an int, we can say that `i` is an int:

```Python

def minus_2(x: %1):
	for i: int in range(len(x)):
		x[i] = x[i] - 2

``` 

and we can say that `%1` must implement `__len__`, `__getitem__(int) -> %2` and `__setitem__(int, %2)` where `%2` implements `__sub__(int)`.

## Explicit annotations

The user can explicitly annotate types as such:

```Python

def add_2(x: float):
	return x+2

```

in the above example there is exactly one implementaion of `add_2`. If the user tries something like `add_2(4)` this will fail as there is no implementation for `int`. Also note how no return value is provided as this can be deduced from the return type. The converse is not true, it is not possible to deduce from return value. The following example

```Python

def add_2(x) -> float:
	return float(x+2)

```

means that `x` can be any value as long as `__add__(int)` is defined and `__float__` is defined on its return value. The `float` function is needed to ensure whatever `x` we use we return a float. Multiple implementations of a function can be defined for arguments as long as they are not explicitly annotated. The following example can accept any type for `x` as long as it implements `__add__(float)`. However only `float` can be accepted for `y`.

```Python
def add(x, y: float):
	return x + y
```

## Deduction for init

Consider two statements:

- Statement 1: The type of class fields must be deductable with just ONE possible type. So this is fine:

```Python

class A:
	def __init__(self):
		self.x = 3

```

because there is only one possible type for `self.x`, `int`. However this is not:

```Python

class A:
	def __init__(self, x):
		self.x = x

def main():
	a_1 = A(4) # Here self.x is deduced as int
	a_2 = A(43.0) # But here it is deduced as float. Error!


```

- Statement 2: When init is used to create a class, duck typing can be used

These may seem mutually exclusive, however we can have our cake and eat it. Lets say we want to store a value in a class as a float, but take any argument that can be converted to float. We can use the following:

```Python

class A:
	def __init__(self, x):
		self.x = float(x)

def main():
	a_1 = A(4)
	a_2 = A(43.0)


```

Since `__float__` always returns `float`, we always know that the type of `self.x` is also float. Two difference copies of `init` are made one accepting `float` and one `int` but both result in `self.x` being a float.

## Nesting

Take the following

```Python

def f(x):
	g(x)

```

In this simple example the requirements of `f` are the requirements of `g`. To generalise, the requirements of a variable are the sum of the requirements of a) all member functions and b) all functions that use it as parameters.


# Inference algorithm

## Definitions

- All functions with at least one argument that is not explicitly typed is treated as polymorphic so

```Python

def f(x):
	return 1

def g(g: int, y):
	return y(g)

```

are polymorphic but

```Python

def h(a: int, b: float):
	return a + b

def i(c: List)
	return len(c)

```

are not.

- Variables labelled with the `%` symbol indicate that they can be any type so long as they fulfill a set of requrements. 

- A requirement represents a function that a type must contain. The variables on requirement function can contain requirements.

- Variables laballed with the `$` symbol indicate that they can be exactly one type

## Labelling

First we iterate over all local variables, function arguments and return statements and label each with a unique type variable. We assume all variables are `%` variables until proven otherwise. So with

```Python

def sub_2(container):

	for i in range(len(container)):
		container[i] = container[i] - 2

	return container

def main():
	x = [3, 6, 7, 9]
	y = [2.5, 7.2, 4.9, 5.1]

	print(sub_2(x))
	print(sub_2(y))



```

we get something like 

```Python

def sub_2(container: %1) -> %2:

	for i: %3 in range(len(container)):
		container[i] = container[i] - 2

	return container

def main():
	x: %4 = [3, 6, 7, 9]
	y: %5 = [2.5, 7.2, 4.9, 5.1]

	print(sub_2(x))
	print(sub_2(y))



```

and we expand into special functions to give

```Python

def sub_2(container: %1) -> %2:

	for i: %3 in range(container.__len__()):
		container.__setitem__(i, container.__getitem__(i).__sub__(2))

	return container

def main():
	x: %4 = [3, 6, 7, 9]
	y: %5 = [2.5, 7.2, 4.9, 5.1]

	print(sub_2(x))
	print(sub_2(y))



```

## Rules

Next we iterate over the code to learn as much about our type variables as possible. In this case we have:

- %1
	- $1 must implement the function `__getitem__(int) -> %6`, where $6 implements `__subtract__(int) -> %7`
	- $1 must implement the function `__setitem__(int, %8)`
- %2
	- %2 = %1, because the return value is `container` which has type `%1`
- %3
	- We have to do a little digging for this one. Given `for a in b`, the type of `a` is deduced by first finding the type `b.__iter__()`, then in that type we find `__next__()`, and `a` is the same type as the return value for `__next__()` (without the some). In this case, `range.__iter__()` is type `IterRange`, and its `__next__()` function always returns int. So
	%3 = int.
- %4
	- RHS of assignment is `List<int>` so %4 = `List<int>`
- %5
	- RHS of assignment is `List<float>` so %5 = `List<int>`
- %6
	- As mentioned, %6 must implement `__subtract__(int)`
- %7
	- There are no restrictions on %7
- %8
	- %8 = %7 because the return value of the substraction is fed into the `__setitem__` function, and these have type variables %7 and %8, respectively.

## Function calls

For each function call we make sure that the parameters 'fit'. That is, if the function is not polymorphic, we check that the parameters fit the explicit types. If it is, we make sure that the parameters fulfill any requirements discovered in the Rules phase. In the above example we have two calls:

	- sub_2(x): We know that `x` has type `List<int>` so we test the two implementation requirements:
		- x does implement the function `__getitem__(int) -> $6`
		- in this case, $6 = int
		- $6 implements `__subtract__(int) -> $7`
		- $7 = int
	
	- sub_2(y): We know that `x` has type `List<float>` so we test the two implementation requirements:
		- x does implement the function `__getitem__(float) -> $6`
		- in this case, $6 = float
		- $6 implements `__subtract__(float) -> $7`
		- $7 = float

we now create two mangled versions of `sub_2` copying the code and creating new type variables with the same rules:

```Python

def sub_2_a(container: List<int>) -> List<int>:

	for i: int in range(container.__len__()):
		container.__setitem__(i, container.__getitem__(i).__sub__(2))

	return container

def sub_2_b(container: List<float>) -> List<float>:

	for i: int in range(container.__len__()):
		container.__setitem__(i, container.__getitem__(i).__sub__(2))

	return container

def main():
	x: List<int> = [3, 6, 7, 9]
	y: List<float> = [2.5, 7.2, 4.9, 5.1]

	print(sub_2_a(x))
	print(sub_2_b(y))

```

## Unification

Follow the steps outlined in the unification algorithm outlined [here](https://www.cmi.ac.in/~madhavan/courses/pl2009/lecturenotes/lecture-notes/node113.html)

## Algorithm 

We keep performing the steps in the function calls and unification steps until we either have an error or a substitution mapping type variables to types.

# Structure

## Types

Here we have a list of all types that a variable can be

- bool
- int
- float
- string
- bytes
- list<T>
- map<K, V>
- set<K>
- option<T>
- result<T, E>
- function pointer<List of types for each parameter, One or none types for the return value>
- user defined type<String value with the name of the type>

```Rust

enum Type {
	Bool,
	Int,
	Float,
	Complex,
	String,
	Path,
	Bytes,
	List{ item: Type },
	Map{ key: Type, value: Type },
	Set{ element: Type },
	Option{ t: Type },
	Result{ t: Type, e: Type }
	FunctionPointer{ args: Vec<Type>, ret: Option<Type> },
	Class{ name: String },

	//Identifier used to represent type variables in the unification algorithm
	TypeIdentifier(u64),

	//Used to resolve requirements. This allows the values of containers to be expressed as requirements rather than explicit types
	Requirement(Requirement),
}

```

## Requirement

Requirements could be as simple as 'Implement the `__xyz__()` function', or as complicated as 'Implement the `__iter()__ -> $1` function where $1 implements `__next__() -> $2` where $2 implements `some_function($3, int) -> $4` where $3 implements `__float__()` and $4 has no requirements'.

Requirements can be a type. This is how we implement explicit types.

Requirements can be one of the following

```Rust

struct FunctionRequirement {
	name: String,
	args: Option<Vec<Requirement>>,
	ret: Option<Requirement>,
}

enum Requirement {
	//To match, the matchee must have type given
	ExplicitType(Type),
	//To match, the matchee must implement each of the functions in the list
	ImplementsFunctions(Vec<FunctionRequirement>),
	//Matches any matchee
	NoRequirements,
	//Placeholder - Used where we don't have an explicit type just yet
	Placeholder,
}

```

### Examples

'Implement the `__xyz__()` function' would evaluate to

```Rust

Requirement::ImplementsFunctions(
	vec![FunctionRequirement{ 
		name: "__xyz__",
		args: None,
		ret: None,
	}]
)

```

and 'Implement the `__iter()__ -> $1` function where $1 implements `__next__() -> $2` where $2 implements `some_function($3, int) -> $4` where $3 implements `__float__() -> float`, $4 has no requirements and $2 also implements `some_other_function()` would evaluate to

```Rust 

Requirement::ImplementsFunctions(vec![FunctionRequirement {

        name:"__iter__",
        args: None,
        ret: Requirement::ImplementsFunctions(vec![FunctionRequirement {

            name:"__next__",
            args: None,
            ret: Some(Requirement::ImplementsFunctions(vec![FunctionRequirement {

                name:"some_function",
                args: Some(vec![ Requirement::ImplementsFunctions(vec![FunctionRequirement {
                            name: "__float__",
                            args: None,
                            ret: Requirement::ExplicitType(Type::Float),
                        }

                        ]),
                    Requirement::ExplicitType(Type::Int)]),
                ret: Some(Requirement::NoRequirements),
            }

            ,
            FunctionRequirement {
                name:"some_other_function",
                args: None,
                ret: None,
            }

            ,
            ]))
        }

        ])
    }

    ])

```

finally we have

```Python

def f(x, y):
	return x(y)

```

which evaluates to 

```Python

def f(x: %1, y: %2) -> %3:
	return x.__call__(y)

```

and from this we have the requirement 'x implements `__call__(%2)` where %2 has no requirements' this can be formalised as

```Rust

Requirement::ImplementsFunctions(
	vec![FunctionRequirement{ 
		name: "__call__",
		args: Some(vec![Requirement::NoRequirements]),
		ret: Some(vec![Requirement::NoRequirements]),
	}]
)

```

when we make a call to `f`, we check the requirement on `x`. If it is satisfied, we create a copy of `f` filling out all the types.

### Fallbackss

As mentioned, for each function call, we test each parameter make sure they match the requirements of the function. In fact, the algorithm is more general than this because poly functions can have multiple definitions indicating fallback functions. So we keep testing requirements on each of the fallback definitions until we find a function that matches, or if we run out of fallbacks and none of them match, we have a type error. Take the following example:

```Python

class A:
	def __str__():
		return "str"

class B:
	def __repr__():
		return "repr"

def to_string(x):
	return x.__str__()

def to_string(x):
	return x.__repr__()

def main():

	print(to_string(A()))

	print(to_string(B()))


```

The first implementation of `to_string` has the 'x implements `__str__()` function' and the second implementation has the 'x implements `__repr__()` function'. So in our first call to `to_string`, we check the criteria for `A`. Since it does fulfill the requirements we have found a match and create a copy of `to_string` that takes `A` as an argument. Next we take the second call. We test `B` for the requrement, which fails since it does not implement `__str__`, so we fallback to the next implementation. Since `B` meets these requirements, we create a copy of the second `to_string` implementation which takes `B` as an argument.

## Equation list

A list of equations of the form `a = b` where a and be can be types or type variables. Equations can look like

- $1 = int
- $2 = $3
- bool = $4
- $4 = $4
- bool = bool
- bool = int

The set of equations is implemented as a list of pairs. A pair is made of two terms, the LHS and the RHS of the equality. Terms are defined as followed:

```Rust

enum Term {
	ExplicitType(Type),
	TypeVariable(u64),
}

```

so the set is defined as `Vec<(Term, Term)>`. For each pair there are 4 cases:

- TypeVariable, TypeVariable: in this case we have $n = $m, so we replace all occurences of $n with $m, or vise versa
- ExplicitType, TypeVariable: in this case we swap the two, so TYPE = $n becomes $n = TYPE.
- TypeVariable, ExplicitType: in this case we have $n = TYPE so we do nothing
- ExplicitType, ExplicitType: In this case we have TYPE_a = TYPE_b. If the types are the same and simple types, remove it from the set as it is redundant. If they are different, this represents a type error. If they are poly types and the same, (list, option, etc.) then equate the internal types. So V<$2, int> = V<bool, int> becomes $2 = bool and int = int. If they are poly types and different, this is a type error.

### Overloading

We can use the requirement and fallback systems together to allow function overloading. Take the following

```Python

def f(x: int):
	...

def f(x: string):
	...

def f(x: float):
	...

def f(x):
	...

def f():
	...

def f(x, y)
	...

```

Since requirements can include explicit types, any number of arguments and nested requirements, we can use this with the fallback system to deduce function overloads. Just as before, we can check the arguments of function calls against the definitions one at a time until we find a match.

# Init polymorphism

We can create templates for classes based on the requirements of the member variables. Take the following

```Python

class Complex:
	
	def __init__(real, imag):
		self.real = real
		self.imag = imag

	def __add__(self, other):
		return Complex(self.real + other.real, self.imag + other.imag)	

```

converting the syntactic sugar we have

```Python

class Complex:

	def __init__(real, imag):
		self.real = real
		self.imag = imag

	# Since no getters or setters were explicitly implemented, Mylang provides these defaults
	def __set_real__(self, real):
		self.real = real

	def __get_real_(self):
		return self.real

	def __set_imag__(self, imag):
		self.imag = imag

	def __get_imag_(self):
		return self.imag

	def __add__(self, other):
		return Complex(self.__get_real__().__add__(other.__get_real__()), self.__get_imag_().__add__(other.__get_imag_()))

```

In the above example, we see that `__init__` has no requirements itself, however the `__add__` function does. From this we see that the requirements on emmber variables are a sum of all the requirements on all the member variables in all the member functions. In this case we just have the requirment that `real` implements `__add__($1)` where $1 implements `__get_real__`. Note that `other` in `__add__` has requirements itself, and are separate from `real`'s requiremnts. From this we have two important results:

- Requirements on non-member function variables resuts in the individual function being templated
- Requirements on member variables (anything on `self`) results in the class being templated.

So in the above example, if we use `Complex(int, int)` and `Complex(float, float)`, this creates two templates of `Complex`. Next we use our implementation of zip to demonstrate class templating:

```Python

class Zip:
	def __init__(iter_a, iter_b):
		self.a = iter_a.__iter__()
		self.b = iter_b.__iter__()

	def __next__():
		a = self.a.__next__()
		b = self.b.__next__()

		# Stop the iterator as soon as either zip is finished
		if a.is_none() or b.is_none():
			return None

		return some((a, b))

```

in the above example we see that the type of `self.a` is decided by `iter_a.__iter__()`. And `__iter__` is a special function, but it doesn't have a set return type. So we must go to `iter_a` for answers, but again this variable's type is not explicit, so we cannot tell from the definition. We cannot tell from the definiton. To make things more general, we treat class generics the way we treat function generics. We treat monomorphic and polymorphic classes the same. 

First we create a set of requirements for each member variable. In this case, we have 'self.a must implement `__next__`'. Next we create requirements for `iter_a`, namely 'iter_a must implement `__iter__() -> $1` where $1 implements `__next__`.

Now that we have a set of requirements, every time we construct a new `Zip` we check the requirements on the constructor then from this call we deduce the type of `self.a`.

## Exceptions

There are times when the type cannot be deduced by the constructor alone.

```Python

class Container:
	def __init__():
		self.a = []

	def extend(item):
		self.a.append(item)

```

This can only happen with container type. Namely

- List types (Lists)
- Map types (Dictionaries, sets, etc.)
- Option

this can be resolved by deducing the type from certain functions that each type has. For example

- `append`, `insert` for list types
- `insert` for map types
- `some` for option

also sometimes we can look at the initialisation to deduce type, for example `[2, 5, 4]` and `{ "fred": 2.3, "mike": 6.5 }`.

## Misleading

Some classes look like they will be templated, but it might only be the `__init__` function that is templated:

```Python

class Int:
	def __int__(value):
		self.value = int(value)

def main():
	a = Int(9)
	b = Int(4.5)

```

it might look as though `Int` would be templated for integers and floats. However the constructor converts every value into a float in its implementation, which means that the `__init__` function is templated. The `float` function always returns a Mylang float, so only one version of `Int` will ever be made, that is where `self.value` is a float. However in the next example, two class templates are made as the values are stored directly and not converted:

```Python

class Int:
	def __int__(value):
		self.value = value

def main():
	a = Int(9)
	b = Int(4.5)

```

## Summary

The rules for class vs function templating are very simple:

- Class templating is performed based on the member variables
- Function templating is performed based on the function parameters.

and the way we test for compatibility (via requirements) and deduce type works the same way for both systems. In fact the algorithm is exactly the same, the only difference is instead of looking at function arguments, we look at member variables.

# Self problem

When we call the `self` variable as is in Rust, this gives a reference to the instantiated object. In Mylang this should be the same, except with stack types it should make a copy of the object, but with heap objects this must return a reference counted RC or GC type. 

The problem is that if we have a Rust class `A`, then `self` within `A` returns an `A`, whereas it should return a `Rc<UnsafeCell<A>>`.

We could secretly include a reference to the object in each custom heap structure, however this will mean that every object becomes a cycle and will invalidate reference counting. This could be fixed with a weak reference but this would still add memory overhead to each structure.

What we must do instead is for each `self` object we must convert it to a `Rc<UnsafeCell<A>>` then clone it to respect the reference counting rules. We can do this with roughly the following:

- Obtain a pointer to `self`
- Since this pointer points to an `A` that exists within a `Rc<UnsafeCell<A>>`, we must decrement N bytes where N is the size in bytes of all the data before `A`
- We now have a pointer at the beginning of `Rc<UnsafeCell<A>>`, so we cast this back to a `Rc<UnsafeCell<A>>` object.
- Finally we clone this object to obtain a new reference to `A` that respects the reference counting rules.

NOTE: These rules only apply when we are obtaining `self` on its own. This does not apply to members variable access like `self.a` as tha `a` is stored as a reference counted object anyway or is stack allocated and moved by value. I propose a functions something like

```Rust

fn filthy_cast_to_rc<T>(t: & T) -> Rc<UnsafeCell<T>> {
    filthy_cast_to_rgc::<T, Rc<UnsafeCell<T>>>(t, 2)
}

fn filthy_cast_to_gc<T>(t: & T) -> Gc<UnsafeCell<T>> {
    filthy_cast_to_rgc::<T, Gc<UnsafeCell<T>>>(t, 1)
}

fn filthy_cast_to_rgc<T, R: Clone>(t: & T, number_of_counts: isize) -> R {
    unsafe {
        // Convert the reference to t into a pointer to t
        let t_pointer = t as * const T;
        
        // convert this pointer to t into a pointer to bytes (used for offset function)
        let bytes_pointer = t_pointer as * const u8;
        
        // The RcBox type contains two usize counts (strong and weak counts) then the data.
        // So to go from the data to the beginning of the RcBox struct, we subtract two usizes worth of bytes from the pointer.
        // For the GcBox, we only have one usize (a single strong count) and so we subtract one usize.
        // We supply the number of usizes to subtract as the argument `number_of_counts`
        let box_begin = bytes_pointer.offset(std::mem::size_of::<usize>() as isize * -number_of_counts);
        
        //Magical jiggery pokery to convert pointer to u8 into a pointer to Rc<...>
        let rc_ref = &box_begin as *const * const u8;
        
        let rc_pointer = rc_ref as * const R;
        
        //Get a regular reference to the Rc<...> object
        let rc_ref = &*rc_pointer;
        
        //Clone the Rc object. This provides a reference to T that respects the reference counting rules
        rc_ref.clone()
    }
}

```

This unholy abomination above is safe if and only if the function is called on an object `t` that is itself wrapped in an [RG]c<UnsafeCell<T>> type, if not this is undefined behaviour.

# Rough roadmap for inference

1. Obtain a dict mapping class names to sets of class member variables
2. Reconstruct the ast replacing all BinOps, BoolOps, UnartOps, IfExps, Compares, getters/setters, Subscripts and built in functions (float(), int(), etc.) to their respective functions. I.e. BinOp(a, 'add', b) becomes something like Call(Attribute(a, '__add__'), [b]). All member variable assignments that are NOT in `__init__` or in a getter/setter, replace it with `__set_NAME__` or `__get_NAME__`
3. Obtain a dict for each function (global and class) that maps parameters (including member variables for class functions) to a list of requirements. Note: be sure to add requirements for variables recursively, looking at all the member functions for the variables, and functions that are called on the variable.
4. For each class, decide whether it is stack or heap allocated
5. Add type variables for each variable

# The Mutable and Immutable

Mutability is important as it is used to decide whether a type should be created on the stack or class, so we only extend out definition of immutability to this end. For example, there are other cases where a class can be considered mutable other than the cases below, but these cases break the other conditions of stack and so we do not consider them.

## Overview

Determining whether a class is mutable or immutable is not as simple as it seems, as there are many operations that can alter mutability. Take the following situations

### Reassigning member variables

Perhaps the simplest example is a class that reassigns its member variables. That is, if a class contains a non-__init__ function that assigns a member variable, the class is no longer immutable. Take the following

```Python

class A:
	def __init__():
		self.x = 0

	def change(value):
		self.x = value

```

### Mutable calls

Next we have mutable calls. If we call a mutable function on a member variable, the class is no longer immutable. For example

```Python

class A:
	def __init__():
		self.list = []

	def append(value):
		self.list.append(value)

```

Even though there is no reassignment of `self.list`, we are mutating `self.list` with the call to append.

### External mutation

If we access mutable members outside a class, this can make any class mutable. So we have to treat a class as mutable if it contains public mutable variables. To avoid this, we must make the member variables private. This will prevent external mutation via reassignment or mutable function calling. So there are two possibilities:

- If a class contains all private member variables, it may be immutable (if it satisfies other conditions)
- If a class contains at least one public member variable, it is definitely considered mutable

# Augmented assign

For this section we use the `+=` example, but this can be extended to any augmented assignment operator. 

Augmented assignment such as `a += b` can be treated in two ways:

- As syntactic sugar for `a = a + b`
- As a call on a mutable function on a for example `a.__iadd__(b)`

At first it might seem like all augmented assignments should be treated as syntactic sugar. However, for heap types the temporary value `a+b` will result in an extra allocation. For heap values, mutable functions acting on variables in place is preferable. This approach should not be used on all types, as this will add a mutable function to the class preventing a class from existing on the stack. For classes that the user wishes to keep on the stack, NO overload should be provided, and the compiler should treat this as `a = a + b`. If the user decides to use an augmented assign overload function on a variable they wish to exist on the stack, this will almost certainly be a mutable function which will break the stack rules, and turn the class into a heap variable instead.

To summarise, if an augmented assignment overload function is provided, it is used. If it is not provided, it is replaced with `a = a + b` and the usual requirement/fallback rules are followed. 

When deciding whether or not to implement an overload function, the general rule is as follows: If the class is intended to exist on the stack (i.e. following the three rules, see stack vs heap for more info) an overload should not be used. If the class is a heap value and augmented assignment is desired, the user should provide an overload.

# Right operators

Say we have a type `A` which implements `__add__` for integers. If we have a variable `a` of type `A` then `a + 5` is valid, but `5 + a` is not as adding a type `A` is not defined for integers. To fix this, we use Python's approach which is to add a bunch of `r` functions, `__radd__`, `__rsub__` etc. Given `a+b`, the compiler first tries `a.__add__(b)` and if this function is not defined for `a` we try `b.__radd__(a)` instead (if this fails then th requirement is not met). 

# Multiplicity

Because a polymorphic class can have `n` different implementations and each one `m` different polymorphic member functions, we might expect `mn` combinations. However we can rule out certain combinations. Take

```Python

class A:
	def __init__(x):
		self.x = x

	def func_a(self, y):
		print("Called function a with {y}")

def main():

	a_1 = A(3)
	a_2 = A(3.4)

	a_1.func_a("hello")
	a_2.func_a(True)


```

In the above example, `A` has two types, one where `self.x` is an `int` (a_1) and another where it is a `float`. We call `func_a` twice with two different arguments, but the string version is only used for a_1 and the boolean version is only used for a_2. So we have one implementation of `A` where `self.x` is an integer and `func_a` takes a string, and another implementation where `self.x` is a float and `func_a` takes a boolean. So instead of every class getting every function, we only implement on where they are needed.

# Filling

When we try and fill out classes and functions, we must have a special symbol table like structure that holds all the polymorphs. 

- For each class we define, we keep a list of polymorphs
- For each polymorph, we have a set of functions that are called on that particular polymorph. 

So in the example above, this would look like

- Polymorph on `A` where `self.x` is a `float`
	- Polymorph on `A.func_a` where `y` is a boolean
- Polymorph on `A` where `self.x` is a `int`
	- Polymorph on `A.func_a` where `y` is a string

# Questions

Here we provide a list of things that the static analysis needs to figure out:

- Class polymorphs (i.e. when member variables can be different types)
- Function polymorphs (i.e. when function parameters can be different types)
- Class immutability (i.e. if a class can be considered immutable)
- Class location (i.e. if a class is on the stack or heap)
- Function parameter requirements

# Todo

1. Obtain a dict mapping class names to sets of class member variables
2. Reconstruct the ast replacing all BinOps, BoolOps, UnartOps, IfExps, Compares, getters/setters, Subscripts and built in functions (float(), int(), etc.) to their respective functions. I.e. BinOp(a, 'add', b) becomes something like Call(Attribute(a, '__add__'), [b]). All member variable assignments that are NOT in `__init__` or in a getter/setter, replace it with `__set_NAME__` or `__get_NAME__`. Replacements:
	- Function calls
		- float(x) -> x.\_\_float\_\_
		- int(x) -> x.\_\_int\_\_
		- complex(x) -> x.\_\_complex\_\_
		- id(x) -> x.\_\_id\_\_
		- char(x) -> x.\_\_char\_\_
		- str(x) -> x.\_\_str\_\_
		- repr(x) -> x.\_\_repr\_\_
		- bool(x) -> x.\_\_bool\_\_
		- abs(x) -> x.\_\_abs\_\_
		- len(x) -> x.\_\_len\_\_
		- iter(x) -> x.\_\_iter\_\_
		- next(x) -> x.\_\_next\_\_
		- path(x) -> x.\_\_path\_\_
		- real(x) -> x.\_\_real\_\_
		- imag(x) -> x.\_\_imag\_\_
		- bytes(x) -> x.\_\_bytes\_\_
	- Binary Ops
		- a + b -> a.\_\_add\_\_(b)
		- a - b -> a.\_\_sub\_\_(b)
		- a * b -> a.\_\_mul\_\_(b)
		- a / b -> a.\_\_truediv\_\_(b)
		- a % b -> a.\_\_mod\_\_(b)
		- a ** b -> a.\_\_pow\_\_(b)
		- a << b -> a.\_\_lshift\_\_(b)
		- a >> b -> a.\_\_rshift\_\_(b)
		- a | b -> a.\_\_or\_\_(b)
		- a ^ b -> a.\_\_xor\_\_(b)
		- a & b -> a.\_\_and\_\_(b)
		- a // b -> a.\_\_floordiv\_\_(b)
	- Comparators
		- a < b -> a.\_\_lt\_\_(b)
		- a <= b -> a.\_\_le\_\_(b)
		- a == b -> a.\_\_eq\_\_(b)
		- a != b -> a.\_\_ne\_\_(b)
		- a > b -> a.\_\_gt\_\_(b)
		- a <= b -> a.\_\_ge\_\_(b)
	- Getters and setters
		- a.VARIABLE = c -> a.\_\_set\_VARIABLE\_\_(c) (Provided the assignment isn't in an init or its own setter function)
		- a.VARIABLE -> a.\_\_get\_VARIABLE\_\_() (Provided the access isn't in an init or its own getter function)
	- Unary ops
		- -a -> a.\_\_neg\_\_()
		- +a -> a.\_\_pos\_\_()
		- ~a -> a.\_\_invert\_\_()
3. Create an algorithm that takes a function and a parameter, and creates a requirement for that paramater
	- a.b(), where the requirement is that `a` implements `b`
	- b(a) where the requirements of `a` become the requirements of the function `b`. These we must solve recursively.
	- Should requirements contain fallbacks, used for augmented assignment and right vs left special functions?
4. Create the requriements classes (as defined in inference algorithm above) Requirements come from two sources

# Function calls

Say a function `f` contains a call to another function `g` on a parameter like

```Python

def f(x)
	g(x)

```
 
There are two possibilities, a) that g is some global function or b that g is a function pointer passed to f, like so

```Python

def f(x, g)
	g(x)

```

Our requirement scheme must be able to handle this case.

# Chaining comparisons?

Maybe dont chain operations and test if a value is between two values with `x in interval(1, 3)`

# Unused requirements

As if the requirement system isn't already complicated enough, just because a class has a function that acts on mamber variables, doesn't meman these should be added to the requirements. If this function is not called on a particular instance, it doesn't make sense to impose those requirements:

```Python

class A:
	def __init__(x):
		self.x = x

	def __float__(self):
		return self.x.__float__()

	def __str__(self):
		return self.x.__str__()

def main():
	a_1 = A(Complex(1, 1))
	a_2 = A(2.3)

	print(a_1)
	print(float(a_2))


```

Since the `__float__` function is never called on `a_1` it should not form a requirement. It would be unfair to exclude a particular type based on a requirement that the compiler can verify is never used. To solve this, we can break down requirements by the member function they come from, or we can create optional requirements

# Slices

Slices can be either Rust-like or Pythonic. We can have the best of both with something like a wrapper around a container that uses the slice for indexing and iterating:

```Python

class ContainerSlice:
	def __init__(container, slice):
		self.container = container
		self.slice = slice

	def __getitem__(self, index: int):
		return self.container[self.slice.start + index * self.slice.step]

	# Ideally we would return a ContainerSlice with the original container (i.e. ContainerSlice(self.container, ...)), and compose the two start/stop/step strategies into one for efficiency but this is just a demonstration and I cba to do the maths atm even though its not that hard lol
	def __getitem__(self, slice: Slice):
		return ContainerSlice(self, slice.start, slice.stop, slice.step)

	def __setitem__(self, index: int, value):
		self.container[self.start + index * self.step] = value

	# This abomination obtains the number of elements in the slice
	def __len__(self):
		return max((self.slice.stop - self.slice.start + (self.slice.stop - self.slice.start) % self.slice.step) // self.slice.step, 0)

	def __iter__(self):
		return ContainerSliceIterator(self)

# The following iterator will work on normal 'unsliced' containers too. Any container with __getitem__(int) and __len__() should work
class ContainerIterator:
	def __init__(container):
		self.container = container
		self.ind = 0

	def __next__(self):
		if self.ind >= len(self.container):
			return None

		return some(self.container[self.ind])

		self.ind += 1


```

Note: The above example doesn't take into account optional agruments in slices (for example slice(0, None, 2), etc.) and is not a complete listing for ContainerSlices or ContainerIterators.

# Requirements and fallbacks

```Python

def f(x):
	return str(x)

def f(x):
	return repr(x)

def g(x):
	return f(x)

```

The requirements of `x` in `g` should include the two versions of `f`, the first as a function and the second as a falback. And indeed all function based requirements should have fallbacks. Any time we have a requirment function with fallbacks, the requirements should reflect all the fallbacks. In the above example, `x` contains the requirements of the first implementation of `f` (that is, `x` must implement `__str__`) but it also has a fallback requirement that `x` impement `__repr__`.

Also think of how it works with complex functions

```Python

def f(x):
	return str(x)

def f(x):
	return repr(x)

def g(x):
	return "{f(x)} {float(x)}"



```

the requirements on `x` in `g` should look something like: 'x should implement `__float__` and x should implement `__str__`, then `__repr__` as a fallback'. So when we apply member functions to a parameter, we propagate these requirements, one set for each fallback.

# Rust's traits

We might be able to leverage Rust's powerful trait and generics system to make life easier. For example:

```Python

class A:
	def __init__(a):
		self.a = a

	def __float__(self):
		return self.a.__float__()

```

can be made easier with


```Rust


trait Float<F> {
    fn __float__(&self) -> F;
}

struct A<T> {
    a: T,
}

impl<T> A<T> {
    fn new(a: T) -> Self {
        A {
            a,
        }
    }
}

impl<F, T: Float<F>> Float<F> for A<T> {
    fn __float__(&self) -> F {
        return self.a.__float__();
    }
}

//Not required in the transformation, only required here to complete the example.
impl Float<f64> for f64 {
    fn __float__(&self) -> f64 {
        return *self;
    }
}

fn main() {

    let a = A::new(4.5);
    
    println!("{}", a.__float__());
    
    println!("hello world");
}


```

As shown above, each member function in a class can be given its own trait which will replicate static ducktyping.

# Nested functions

When we have a function like 

```Python

def f(x):
	g(x)

```

previously we mentioned that the requirements of g on x are passed to f and become the requirements of f on x. This is no longer the case. In this case, x has no requirments and it is down to g to check its own requirements. In general, functions are responsible for their own reuqirements and these requirements are not passed to calling functions.

# Stack or heap new

Creating a new instance via `__init__` should return a `Rc` if the variable is on the heap, or `Self` if it is a stack variable. We pass instances with `clone` which will clone the `Rc` or copy the varible, for heap and stack values respectively.

Create a special marker trait for stack or heap variables?

# Mylang lite

A prototype for Mylang which differs from mylang in the following ways:

- Does not implement fallback methods
- All variables exist on the heap
- All heap variables are std::rc::Rc 
- Can only overload functions by number of parameters

# Stack, Access and This traits

We want to be able to treat stack and heap variables in the same way, to make the code translation easier, however there are fundamental differences between the two:

## Function access

To call a function on a heap variable, the helper function

```Rust
fn mut_ref_rc<T>(t: & CellRc<T>) -> & mut T {
    unsafe { UnsafeCell::<_>::get(t).as_mut().unwrap() }
}
```

is needed, but for stack variables `Variable.Function()` is enough.

To solve this, we have a trait `Access` which exposes one function `access` that for heap variables stored as `CellRc<T>` returns `&T` and for stack variables of type `T` returns `&T`. 

```Rust

trait Access {
	
}

```


We can implement a blanket implementaion for all `CellRc<T>` with

```Rust




```

## Access to Self

If a function needs to move a whole `self`, maybe it needs to return self, this also happens differently for heap and stack variables. For stack variables, we return `*self` but for heap variables we must use the dirty cast from `T` to `CellRc<T>`

# Requirement algorithm

Resolving requirements is the core of the mylang static analysis. We start with a function `resolve_requirement` which takes a function and an argument in that function and returns a requirement for that function.

1. If the argument has a type annotation. If it does, then the requirement becomes an explicit type with the name given in the annotation.
2. We look over all calls to methods of the argument (and any calls on any aliases of the argument) and any calls to stand alone functions that take the argument or any alias as a parameter, and build a tree of member functions and function requirements.
3. If this tree is not empty, then we have a function list requirement. If this list is empty, then there are no requirements

Since step one is trivial once a Python AST has been generated, we focus on step 2. To take an example, sets say we have a function `f` and a variable we wish to track requirements for called `x`. Assume we have already checked for a type annotation on `x` and none were found. This means we must start step 2. First we create a list of variables to track, starting with `\[x\]`.

Than for each variable in the list we look for:

- Any aliases of the variable (i.e. `y = x`)
	- If we find an alias, we add this to the list of variables to track
- Any method calls on the variable (i.e. `x.some_function()`)
	- If we find a method call we add this to the requirement list then we perform a search on all parameters passed and the return value.
- Any global function calls taking the variable as a parameter (i.e. `some_function(x)`)
	- We compute the requirements for the function then add these to the variable

For each method call on the variable, we recursively complete the same steps to resolve the requirements on any arguments and the return value. When all ends are exhausted (i.e. with concrete types, no return/paramaters, or no requirements) then the search is complete.


# Revised strategy

we have a function called `resolve_requirements` which takes an ast functiondef object as a paramater.

In this function, we define a dictionary called `symbols` which maps argument names to a list of aliases and a set of requirements.

When we come accross an expression which acts on any of the alias variables, we recursively add the requirements to the requirement stored in the dict.

When an alias of a paramater is created, this is added to the dict

When a return value for a member function is assigned to a variable, that variable is added to the list, its alias tracked and its requirements added too.

Take the following abomination:

```Python

def func(x, y):
	#1
	alias_x = x
	#2
	float_x = x.__float__()
	#3
	sums = float_x.__add__(y.__float__())
	#4
	alias_alias_x = alias_x
	#5
	return (alias_alias_x.__str__(), sums.__float__())
	#6

```

Here we outline the states of `resolve_requirements` at each statement in `func`:

1. `symbols = { "x": ([], None), "y": ([], None) }`
2. `symbols = { "x": (["alias_x"], None), "y": ([], None) }`
3. `symbols = { "x": (["alias_x"], ImplementsFloat), "y": ([], None), "float_x": ([], None) }`
4. `symbols = { "x": (["alias_x"], ImplementsFloat), "y": ([], ImplementsFloat), "float_x": ([], ImplementsAddToYDotFloat), "sums": ([], None) }`
5. `symbols = { "x": (["alias_x", "alias_alias_x"], ImplementsFloat), "y": ([], ImplementsFloat), "float_x": ([], ImplementsAddToYDotFloat), "sums": ([], None) }`
6. `symbols = { "x": (["alias_x", "alias_alias_x"], ImplementsFloatAndImplementsStr), "y": ([], ImplementsFloat), "float_x": ([], ImplementsAddToYDotFloat), "sums": ([], ImplementsFloat) }`

the last step is to resolve all temporary variables into the argument variables. Idk how to do this yet so this is tomorrow's problem lol gl tomorrow Will.

`symbols = { "x": (["alias_x", "alias_alias_x"], ImplementsFloatWhichImplementsAddToYDotFloatWhereTheSumImplementsFloatAndAlsoImplementsStr), "y": ([], ImplementsFloat)}`

Resolving temporary variables can be done by replacing a requirement with a special placeholder indicating the variable. In the above example, the return value for `x.__float__()` has no requirements when it is formed, but it does have a return value. So in place of a requirement on the return value, we store the name of the variable we assign to, `float_x`. At the end of parsing, we can replace all of these special placeholders with their requirements.

Optimisation: We make a slight adjustment to the above strategy. Instead of mapping argument names to a list-requirement pair, we map argument names to requirements. When we add an alias, we map that to the requirement of the aliased variable. Modifying one requirement will modify the requirements for all aliases, since the requirements are passed by reference.

# Things and stuff:

Any method call chain can be represented as

a.b(...).c(...). ... z(...)

each function can have args that are either another method call chain or None.

First we start with a variable `x`.

`x` has n member functions `mem_1_1` to `mem_1_n`.