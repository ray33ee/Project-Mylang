# Contents

- 1 [Introduction](#introduction)
- 2 [Structural Typing](#structural_typing)
	- 2.1 [Special Methods](#special_methods)
		- 2.1.1 [Specials](#specials)
			- 2.1.1.0 [Initialisation](#init)
				- 2.1.1.0.1 [\_\_init\_\_](#__init__)
			- 2.1.1.1 [Conversions and casts](#conversions_casts)
				- 2.1.1.1.1 [\_\_float\_\_](#__float__)
				- 2.1.1.1.2 [\_\_int\_\_](#__int__)
				- 2.1.1.1.3 [\_\_index\_\_](#__index__)
				- 2.1.1.1.4 [\_\_bool\_\_](#__bool__)
				- 2.1.1.1.5 [\_\_str\_\_](#__str__)
				- 2.1.1.1.6 [\_\_fmt\_\_](#__fmt__)
				- 2.1.1.1.7 [\_\_bytes\_\_](#__bytes__)
			- 2.1.1.2 [Containers](#containers)
				- 2.1.1.2.1 [\_\_len\_\_](#__len__)
				- 2.1.1.2.2 [\_\_contains\_\_](#__contains__)
			- 2.1.1.3 [Sequences](#sequences)
				- 2.1.1.3.1 [\_\_getitem\_\_](#__getitem__)
				- 2.1.1.3.2 [\_\_setitem\_\_](#__setitem__)
			- 2.1.1.4 [Maps](#maps)
				- 2.1.1.4.1 [\_\_hash\_\_](#__hash__)
			- 2.1.1.5 [Properties](#special_properties)
				- 2.1.1.5.1 [\_\_get_IDENTIFIER\_\_](#__get_IDENTIFIER__)
				- 2.1.1.5.2 [\_\_set_IDENTIFIER\_\_](#__set_IDENTIFIER__)
			- 2.1.1.6 [Binary Operators](#binop)
			- 2.1.1.7 [Unary Operators](#unop)
			- 2.1.1.8 [Compares](#cmpop)
				- 2.1.1.8.1 [\_\_lt\_\_](#__lt__)
				- 2.1.1.8.2 [\_\_le\_\_](#__le__)
				- 2.1.1.8.3 [\_\_eq\_\_](#__eq__)
				- 2.1.1.8.4 [\_\_ne\_\_](#__ne__)
				- 2.1.1.8.5 [\_\_gt\_\_](#__gt__)
				- 2.1.1.8.6 [\_\_ge\_\_](#__ge__)
			- 2.1.1.9 [Augmented Assign](#augop)
			- 2.1.1.10 [Iterable](#iterable)
				- 2.1.1.10.1 [\_\_next\_\_](#__next__)
				- 2.1.1.10.2 [\_\_iter\_\_](#__iter__)
			- 2.1.1.11 [Callable](#callable)
				- 2.1.1.11.1 [\_\_call\_\_](#__call__)
			- 2.1.1.12 [Complex](#complex)
				- 2.1.1.12.1 [\_\_real\_\_](#__real__)
				- 2.1.1.12.2 [\_\_imag\_\_](#__imag__)
			- 2.1.1.13 [Identities](#identities)
				- 2.1.1.13.1 [\_\_zero\_\_](#__zero__)
				- 2.1.1.13.2 [\_\_one\_\_](#__one__)
			- 2.1.1.14 [Fallable](#fallable)
				- 2.1.1.14.1 [\_\_unwrap\_\_](#__unwrap__)
			- 2.1.1.15 [identity](#identity)
				- 2.1.1.15.1 [\_\_id\_\_](#__id__)
			- 2.1.1.16 [Paths](#paths)
				- 2.1.1.16.1 [\_\_path\_\_](#__path__)
			- 2.1.1.17 [Heap Values](#heap_values)
				- 2.1.1.17.1 [\_\_drop\_\_](#drop)
		- 2.1.2 [Operator Overloading](#operator_overloading)
		- 2.1.3 [Built-in functions](#bi_functions)
			- [abs](#bf_abs)
			- [all](#bf_all)
			- [any](#bf_any)
			- [assert](#bf_assert)
			- [chr](#bf_chr)
			- [enumerate](#bf_enumerate)
			- [err](#bf_err)
			- [filter](#bf_filter)
			- [format](#bf_format)
			- [hash](#bf_hash)
			- [id](#bf_id)
			- [input](#bf_input)
			- [iter](#bf_iter)
			- [len](#bf_len)
			- [map](#bf_map)
			- [max](#bf_max)
			- [min](#bf_min)
			- [next](#bf_next)
			- [ok](#bf_ok)
			- [open](#bf_open)
			- [path](#bf_path)
			- [pow](#bf_pow)
			- [print](#bf_print)
			- [round](#bf_round)
			- [sorted](#bf_sorted)
			- [some](#bf_some)
			- [sum](#bf_sum)
	- 2.2 [Properties](#properties)
		- 2.2.1 [Getter](#getter)
		- 2.2.2 [Setter](#setter)
- 3 [Built-in Types](#bi_types)
	- 3.1 [`bool`](#bi_bool)
	- 3.2 [`int`](#bi_integer)
	- 3.3 [`char`](#bi_char)
	- 3.4 [`float`](#bi_float)
	- 3.5 [Id](#bi_id)
	- 3.6 [`List`](#bi_list)
	- 3.7 [`String`](#bi_string)
	- 3.8 [`Bytes`](#bi_bytes)
	- 3.9 [Dictionary](#bi_dict)
	- 3.10 [`Set`](#bi_set)
	- 3.11 [Option](#bi_option)
	- 3.12 [Result](#bi_result)
- 4 [Exceptionless](#exceptionless)
- 5 [Stack, Heap and the Rule of Three](#stack_heap_rot)
	- 5.1 [Stack](#stack)
	- 5.2 [Heap](#heap)
	- 5.3 [Rule of Three Explanation](#rule_of_three_e)
	- 5.4 [Rule of Three](#rule_of_three)
	- 5.5 [Drop](#drop)
- 6 [Garbage collection](#garbage_collection)
	- 6.1 [Standard Reference Counting](#reference_counting)
	- 6.2 [Collecting Cycles](#collecting_cycles)
- 7 [Function overloading](#function_overloading)
	- 7.1 [By paramater count](#by_count)
	- 7.2 [By explicit type](#by_specificity)
- 8 [Control Flow](#control_flow)
	- 8.1 [If](#if_statement)
	- 8.2 [For](#for_statement)
	- 8.3 [While](#while_statement)
	- 8.4 [Loop](#loop_statement)
	- 8.5 [OkError](#okerr_statement)
	- 8.6 [SomeNone](#somenone_statement)
- 9 [Grammar](#grammar)
	- [Formatted String](#g_formatted_string)

# 1 Introduction <a name="introduction"></a>

- Structurially typed
- Strongly typed
- Statically typed
- Python like syntax, Rust like performance (hopefully lol)

# 2 Structural Typing <a name="structural_typing"></a>

Mylang is structurally typed (think duck typing for static langauges, see [this](https://en.wikipedia.org/wiki/Structural_type_system) for more information) so instead of function arguments taking variables by type, we take variables by what functions they implement.

## 2.1 Special methods <a name="special_methods"></a>

While any member function can be used for structural typing, there are certain functions that classes can implement which convery special meaning. Like in Python, these functions start and and in a double underscore `__`. Here we outline all special functions, their meaning, their behaviour, their return value, what types they should be implemented on and any arguments they take.

### 2.1.1 Specials <a name="specials"></a>

#### 2.1.1.0 Initialisation <a name="init"></a>

##### 2.1.1.0.1 `__init__` <a name="__init__"></a>

Called to construct objects. Can contain any number and any type of parameters. Must not return a value. All fields of a class must be set in `__init__` and no new fields may be initialised elsewhere.

#### 2.1.1.1 Conversions and Casts <a name="conversions_casts"></a>

##### 2.1.1.1.1 `__float__` <a name="__float__"></a>

This function should convert a type into a float-like object. For primitive types that implement it, this returns [float](#bi_float). It takes no arguments, and the return type has no type restrictions.

##### 2.1.1.1.2 `__int__` <a name="__int__"></a>

Used to convert an object into an integer-like object. For primitives that implement it, this returns [int](#bi_integer). Takes no arguments and the return type has no restrictions.

##### 2.1.1.1.3 `__index__` <a name="__index__"></a>

Converts an object into a value that can be used to index arrays. Takes no arguments and the return type must be [id](#bi_id)

##### 2.1.1.1.4 `__bool__` <a name="__bool__"></a>

Converts an object into a boolean value. Takes no arguments and the return type must be [bool](#bi_bool). This function is automatically called by any expression in statements that require boolean expressions (`if`, `while`, etc.)

##### 2.1.1.1.5 `__str__` <a name="__str__"></a>

Converts an object into a string. Takes no arguments and must return [String](#bi_string). This function is automatically called by expressions (without explicit formats) in formatted [`print`](bf_print) statements.

##### 2.1.1.1.6 `__fmt__` <a name="__fmt__"></a>

Converts an object into a formatted string. Takes any number of arguments representing the format of the string and must return [String](#bi_string). This function is called by expressions (with explicit formats) in formatted [`print`](#bf_print) statements.

##### 2.1.1.1.7 `__bytes__` <a name="__bytes__"></a>

Converts an object into a list of bytes. Takes no arguments and should return a bytes-like object.

#### 2.1.1.2 Containers <a name="containers"></a>

Containers must expose a [`__len__`](#__len__) function that returns the number of items in the container, and should implement a [`__contains__`](#__contains__) function to determine if an item exists in the container. If a container has elements stored sequentially then it should expose [`__getitem__`](#__getitem__) and [`__setitem__`](#__setitem__) (see [2.1.1.3](#containers)) on integer types, and if it is map-like it should implement those functions on keys. All containers should implement an [`__iter__`](#__iter__) (see [2.1.1.10](#iterable)) type for traversal regardless of container type.

##### 2.1.1.2.1 `__len__` <a name="__len__"></a>

Used mostly for containers but can be extended to any types with some notion of size, this function will return the number of elements in a type.

##### 2.1.1.2.2 `__contains__` <a name="__contains__"></a>

Containers should this function to users to test whether an alement exists within a container. This might mean iterating through the container, accessing a key in a map, or something implementation specific. The `in` keyword uses this function in the following way: `x in y` evaluates to `y.__contains__(x)`.

#### 2.1.1.3 Sequences <a name="sequences"></a>

For containers with data that is represented sequentially in memory or for containers that allow some form of random access, get and set methods (that take an index or key) should be provided. These methods are the syntactic sugar created by subscripting such as `a[b]`.

##### 2.1.1.3.1 `__getitem__` <a name="__getitem__"></a>

Subscripting for accessing elements in a container turns `x = a[b]` into `x = a.__getitem__(b)`. The indexer can be an integer, slice, key, or any value at all.

##### 2.1.1.3.2 `__setitem__` <a name="__setitem__"></a>

Subscripting for modifying elements in a container turns `a[b] = x` into `a.__getitem__(b, x)`. The indexer can be an integer, slice, key, or any value at all.

#### 2.1.1.4 Maps  <a name="maps"></a>

Types that are used as keys in maps should implement the `__hash__` function.

##### 2.1.1.4.1 `__hash__` <a name="__hash__"></a>

Any types that are used as keys in a map should implement `__hash__`. For stack types this should involve calling hash on each field, and for heap types this should involve calling hash on the [`__id__`](#__id__) of the value.

#### 2.1.1.5 Properties <a name="special_properties"></a>

Objects can implement getters and setters with the following functions, for more information about properties see [2.2](#properties).

##### 2.1.1.5.1 `__get_IDENTIFIER__` <a name="__get_IDENTIFIER__"></a>

Getter, since `x = a.value` converts into `x = a.__get_value__()`, this function can be used to simulate phantom member variables and allow structural typing based on member variables by exposing getters. IDENTIFIER is the name of the attribute to get, this need not be a member variable.

##### 2.1.1.5.2 `__set_IDENTIFIER__` <a name="__set_IDENTIFIER__"></a>

Setter, since `a.value = x` converts into `a.__set_value__(x)`, similarly to the getter, this function can be used to simulate phantom member variables and allow structural typing based on member variables by exposing setters. IDENTIFIER is the name of the attribute to set, this need not be a member variable.

#### 2.1.1.6 Binary Operators <a name="binop"></a>

#### 2.1.1.7 Unary Operators <a name="unop"></a>

#### 2.1.1.8 Compares <a name="cmpop"></a>

Compares take no arguments, and there are no explicit requirements on the return types of compares. However they must return values that implement the logical functions (and, or, not, xor) and must implement `__bool__`.

##### 2.1.1.8.1 `__lt__` <a name="__lt__"></a>

Less than comparrison, `<`.

##### 2.1.1.8.2 `__le__` <a name="__le__"></a>

Less than or equal to comparrison, `<=`.

##### 2.1.1.8.3 `__eq__` <a name="__eq__"></a>

Equal to comparrison, `==`.

##### 2.1.1.8.4 `__ne__` <a name="__ne__"></a>

Not equal to comparrison, `!=`.

##### 2.1.1.8.5 `__gt__` <a name="__gt__"></a>

Greater than comparrison, `>`.

##### 2.1.1.8.6 `__ge__` <a name="__ge__"></a>

Greater than or equal to comparrison, `>=`.

#### 2.1.1.9 Augmented Assign <a name="augop"></a>

#### 2.1.1.10 Iterable <a name="iterable"></a>

Any iterator must implement the `__next__` function and the `__iter__` function itself (which for iterators themselves just returns `self`, this is for compatibility with for loops (see [8.2](#for_statement) for more information on loops))

##### 2.1.1.10.1 `__next__` <a name="__next__"></a>

Calling `__next__` on an iterator type should advance the iterator to the next state, returning a value wrapped in a some or a none if the iterator has finished.

##### 2.1.1.10.2 `__iter__` <a name="__iter__"></a>

The `__iter__` function contains no arguments and there are no restrictions on the return value, but returned values should be an iterator and they must implement [`__next__`](#__next__) and `__iter__`

#### 2.1.1.11 Callable  <a name="callable"></a>

Objects that are callable can be treated, in a way, as functions for example `a(b)` where `a` is an object.

##### 2.1.1.11.1 `__call__` <a name="__call__"></a>

This function has no restriction on the number of paramaters, type or the return type. Implement this function to make an object callable, i.e. `a(b)` evaluates to `a.__call__(b)` if `a` is an object and has the correct implementation of `__call__`.

#### 2.1.1.12 Complex <a name="complex"></a>

Any type that exists in the complex plane should implement the following functions, this includes numbers that are real.

##### 2.1.1.12.1 `__real__` <a name="__real__"></a>

Implement this function if the object has a real part. Takes no arguments and there are no restrictions on return type. If this type is implemented on real numbers, then it should simply return `self`

##### 2.1.1.12.2 `__imag__` <a name="__imag__"></a>

Implement this function if the object has an imaginary part. Takes no arguments and there are no restrictions on return type. If this type is implemented on real numbers, this should return 0, or more specifically [`__zero__`](#__zero__)

#### 2.1.1.12 Identities <a name="identities"></a>

Any numeric type should implement the additive and multiplicative identities. More formally, if the type is a mathematical ring (see [this](https://en.wikipedia.org/wiki/Ring_(mathematics)) for more information) it should have a way to expose the additive identity (`__zero__`) and the multiplicative identity (`__one__`)

##### 2.1.1.13.1 `__zero__` <a name="__zero__"></a>

If the type is a ring, has an additive identity or has a natural zero number, this function should return that value. No arugments and no restrictions on return type.

##### 2.1.1.13.2 `__one__` <a name="__one__"></a>

If the type is a ring, has a multiplicative identity or has a natural one number, this function should return that value. No arugments and no restrictions on return type.

#### 2.1.1.14 Fallable <a name="fallable"></a>

Any type that has a pass or fail style (for example [Result](#bi_result) or [Option](bi_option)) it must expose these functions

##### 2.1.1.14.1 `__unwrap__` <a name="__unwrap__"></a>

This function should unwrap the value and return the stored 'pass' value (Some for option and Ok for result) or panic if the value is a 'fail' type (None for option and Err for result). Types that are not pass or fail may still want to implement `__unwrap__` and if this is the case they should return `self` and never panic.

#### 2.1.1.15 Identity <a name="identity"></a>

All values implement this function automatically and overloading this function will (maybe?) produce a compiler error.

##### 2.1.1.15.1 `__id__` <a name="__id__"></a>

Returns a number unique to the object. This function has no parameters and must return an [ID](#bi_id). This function is implemented as returning the address of the object cast to an [ID](#bi_id). See [3.4](#bi_id) for more information.

#### 2.1.1.16 Paths <a name="paths"></a>

Path types are types that store OS paths and return a string version of this for displaying or use in OS functions.

##### 2.1.1.16.1 `__path__` <a name="__path__"></a>

Returns a string representation of the path object. Takes no parameters and returns a string. Functions that take paths (like the [open](bf_open) function for example) can take path-like objects and call `__path__` to extract the path.

#### 2.1.1.17 Heap Values <a name="heap_values"></a>

Heap values call `__drop__` when the reference count reaches zero (or a cycle is unreachable). For special types (for example file handles) extra behaviour can be added to clean up other resources.

##### 2.1.1.17.1 `__drop__` <a name="__drop__"></a>

Called when the heap value's reference count reaches zero or a cycle has been identified as unreachable.

### 2.1.2 Operator Overloading <a name="operator_overloading"></a>

Mylang provides operator overloading the same way Python does, by implementing certain special functions corresponding operators can be used in place as syntactic sugar. See [2.1.1](#specials) for a list of special functions, some of which are used in operator overloading.

### 2.1.3 Built-in functions <a name="bi_functions"></a>

#### `abs(x)` <a name="bf_abs"></a>

Evaluates `abs(x)` to `x.__abs__()` using [`__abs__`](#__abs__) to calculate the absolute value of a number.

Requirements: `x` must implement[`__abs__`](#__abs__).

#### `all(iterable)` <a name="bf_all"></a>

Returns `true` if all elements in `iterable` return `true` when [`__bool__`](#__bool__) is called on them.

Requirements: `iterable` must implement [`__iter__`](#__iter__) and [`__next__`](#__next__), and the elements returned from next must implement [`__bool__`](#__bool__).

#### `any(iterable)` <a name="bf_any"></a>

Returns `true` if any element in `iterable` return `true` when [`__bool__`](#__bool__) is called on them.

Requirements: `iterable` must implement [`__iter__`](#__iter__) and [`__next__`](#__next__), and the elements returned from next must implement [`__bool__`](#__bool__).

#### `assert(condition)` <a name="bf_assert"></a>
#### `assert(condition, message)`

Contains one or two paramaters, the first is the expression to test which if it fails will panic. The second is an optional argument which is converted into a string to show in the panic message.

Requirements: `condition` must implement [`__bool__`](#__bool__) and `message` must implement [`__str__`](#__str__)

#### `chr` <a name="bf_chr"></a>



#### `enumerate(iterable)` <a name="bf_enumerate"></a>
#### `enumerate(iterable, start)`

Returns an iterable that has an object-index pair. 

Requirements: `iterable` must [`__iter__`](#__iter__) and [`__next__`](#__next__). `start` must implement [`__add(x: integer)__`](#__add__)

#### `err(error)` <a name="bf_err"></a>

Represents an error value, similar to Rust's `Result::err`. Used in conjunction with [`ok`](#bf_ok).

Requirements: `error` must implement [`__str__`](#__str__).

#### `filter(functor, iterable)` <a name="bf_filter"></a>

Constructs a new iterator from the elements in `iterable` for which `functor` evaluates true.

Requirements: `functor` must implement [`__call__`](#__call__(x)) where the return value implements [`__bool__`](#__bool__). `iterable` must implement [`__iter__`](#__iter__) and [`__next__`](#__next__) and the return value of `__next__` must be compatible with the argument in `functor.__call__()`.

#### `format(value, specs: String)` <a name="bf_format"></a>

Convert a value into a string using `specs` to specify the format used. Converted into [`__fmt__`](#__fmt__) under the hood.

Requirements: `value` must implement [`__fmt__`](#__fmt__). `specs` must be a string.

#### `hash(object)` <a name="bf_hash"></a>

Calcuale the hash of an object used in dictionary and set-like objects. Converts to [`__hash__`](#__hash__) under the hood.

Requirements: `object` must implement [`__hash__`](#__hash__)

#### `id(object)` <a name="bf_id"></a>

Return an object of type `Id` which represents an object as a unique value. Converts to [`__id__`](#__id__) under the hood.

Requirements: `object` must implement [`__id__`](#__id__)

#### `input()` <a name="bf_input"></a>
#### `input(prompt)`

Reads input from stdin and returns this value as a string. If `prompt` is supplied, this value is printed as a message before the functions reads input.

Requirements: `prompt` must implement [`__str__`](#__str__)

#### `iter(x)` <a name="bf_iter"></a>

Returns an iterable type, syntactic sugar for `x.__iter__()`

Requirements: `x` must implement [`__iter__`](#__iter__) and the return value of this must implement [`__iter__`](#__iter__) and [`__next__`](#__next__)

#### `len(x)` <a name="bf_len"></a>

Returns the length of a container type, syntactic sugar for `x.__len__()`

Requirements: `x` must implement [`__len__`](#__len__)

#### `map(functor, iterable)` <a name="bf_map"></a>

Constructs a new iterator that applies `functor` to every item in `iterable`.

Requirements: `functor` must implement [`__call__`](#__call__(x)), `iterable` must implement [`__iter__`](#__iter__) and [`__next__`](#__next__) and the return value of `__next__` must be compatible with the argument in `functor.__call__()`.

#### `max(iterable)` <a name="bf_max"></a>
#### `max(a1, a2)`

Returns the maximum value out of a pair of values or an iterable. If one argument is provided, it is expected to be an iterable type. If two arguments are provided we find the maximum of the two values.

Requirements: `a1` and `a2` must implement [`__gt__`](#__gt__). `iterable` must implement [`__iter__`](#__iter__) and [`__next__`](#__next__), the return value of `__next__` must implement `__gt__`.

#### `min(iterable)` <a name="bf_min"></a>
#### `min(a1, a2)`

Returns the minimum value out of a pair of values or an iterable. If one argument is provided, it is expected to be an iterable type. If two arguments are provided we find the minimum of the two values.

Requirements: `a1` and `a2` must implement [`__lt__`](#__lt__). `iterable` must implement [`__iter__`](#__iter__) and [`__next__`](#__next__), the return value of `__next__` must implement `__lt__`.

#### `next(iterator)` <a name="bf_next"></a>

Returns the next value in an iterator. If there is no value, `None` is returned. Equivalent to `iterator.__next__`

Requirements: `iterator` must implement [`__next__`](#__next__)

#### `ok` <a name="bf_ok"></a>



#### `open` <a name="bf_open"></a>


#### `path(pathlike)` <a name="bf_path"></a>

Converts pathlike objects into a path string. Delagates to `pathlike.__path__()` via [`__path__`](#__path__)

#### `pow` <a name="bf_pow"></a>



#### `print` <a name="bf_print"></a>

Takes a string (formatted strings are also acceptable, see [this](#g_formatted_string)) and prints it to stdout.

#### `round(number)` <a name="bf_round"></a>
#### `round(number, ndigits)`

Rounds `number` to the nearest integer or, if ndigits is provided, to `ndigits` of precision. This function delagetes to `number.__round__` via [`__round__`](#__round__) 

#### `sorted` <a name="bf_sorted"></a>



#### `some` <a name="bf_some"></a>



#### `sum(iterable)` <a name="bf_sum"></a>
#### `sum(iterable, start)`

Sums up `start` (or zero if it is not provided) and all the iterable elements and returns this value

Requirements: `start` must implement [`__add__`](#__add__) on the return value of `__next__`. `iterable` must implement [`__iter__`](#__iter__) and [`__next__`](#__next__), the return value of `__next__` must implement `__add__` on other values of `__next__`. 

## 2.2 Properties <a name="properties"></a>

Properties work like getters and setters on objects. Getters and setters can be implemted for actual member variables, but they can be implemented for any variable name whether it is a member variable or not. See the following titles for more.

### 2.2.1 Getter  <a name="getter"></a>

Take the snippet `a = object.value`. This is syntactic sugar for `a = object.__get_value__()` and provided `object` implements [`__get_value__`](#__get_IDENTIFIER__), this is valid code. It does not matter whether or not `value` is a member variable or not. All Mylang checks for is that the correct function is implemented, then calls it.

### 2.2.2 Setter  <a name="setter"></a>

Take the snippet `object.value = a` which is syntactic sugar for `object.__set_value__(a)`. Once again, as long as `object` implements [`__set_value__`](#__set_IDENTIFIER__) for `a` as an argument, this is valid code because the compiler only cares if the function is implemnented, it does not check that `value` is a member variable.

# 3 Built-in Types <a name="bi_types"></a>

## 3.1 `bool` <a name="bi_bool"></a>

Boolean type can be `true` or `false` based on Rust's [bool](https://doc.rust-lang.org/std/primitive.bool.html)

## 3.2 `int` <a name="bi_integer"></a>

Signed 64-bit integer based on Rust's `i64`

## 3.3 `char` <a name="bi_char"></a>

Signed character type based on Rust's `Char`

## 3.4 `float` <a name="bi_float"></a>

Double precision 64-bit float based on Rust's [f64](https://doc.rust-lang.org/std/primitive.i64.html)

## 3.5 `Id` <a name="bi_id"></a>

Integer like value representing a unique ID given to variables, accessed with the [`__id__`](#__id__) function. Based on Rust's [usize](https://doc.rust-lang.org/std/primitive.usize.html)

## 3.6 `List` <a name="bi_list"></a>

Vector of elements stored sequentially in memory. Based on Rust's [Vec\<T\>](https://doc.rust-lang.org/std/vec/struct.Vec.html)

## 3.7 `String` <a name="bi_string"></a>

Stores a string

## 3.8 `Bytes` <a name="bi_bytes"></a>

[List](#bi_list) of bytes

## 3.9 `Dictionary` <a name="bi_dict"></a>

Dictionary mapping keys to values. Keys call [`__hash__`](#__hash__) to compute hash values. Based on Rust's [HashMap\<K\>\<V\>](https://doc.rust-lang.org/std/collections/struct.HashMap.html) 

## 3.10 `Set` <a name="bi_set"></a>

A mathematical set, based on Rust's [HashSet\<T\>](https://doc.rust-lang.org/std/collections/struct.HashSet.html)

## 3.11 `Option` <a name="bi_option"></a>

Value that can either be `None` or `Some` containing some value. Based on Rust's [Option](https://doc.rust-lang.org/std/option/). A value can be used as an option by either setting it to the constant `None` or by calling [`some()`](#bf_some) and passing the object as an agrument.

## 3.12 `Result` <a name="bi_result"></a>
 
Value that can either be `Ok` representing a success and containing a value or `err` representing failure and containing the error. Based on Rust's [Result](https://doc.rust-lang.org/std/result/). A success result can be created with [`ok()`](#bf_ok) and a failure with [`err()`](#bf_err) passing the success or error respectively.

# 4 Exceptionless <a name="exceptionless"></a>

One of the main ways Mylang differs from Python is error handling. While Python prefers exception based error handling, we use an approach similar to Rust where functions return a [`Result`](#bi_result) which can communicate success or failure, and a success value or an error value. Results can be unwrapped to produce a panic, or they can be passed on and handles with the [`OkError`](#okerr_statement) statement.

# 5 Stack, Heap and the Rule of Three <a name="stack_heap_rot"></a>

Definition: Location. The location of a variable is where it exists in memory, i.e. Stack or heap.

In this section, we explain the difference between stack and heap variables within the context of Mylang and then we take a brief look into how the compiler determines the location of a variable.

## 5.1 Stack <a name="stack"></a>

If a variables location is determined to be the stack, then it is allocated on the stack. This follows the same rules as most other languages such as declared on the stack frame and deallocated when the frame is deallocated. Stack variables are also shallow copied when moved around, which means a bitwise copy of the structure.

## 5.2 Heap <a name="heap"></a>

If a variable's location is determined to be the heap, then it is allocated using `malloc` and placed on the heap. Extra information is included with the value to allow reference counting and cycle cleaning. When a copy of a heap variable is required, a copy of the pointer to the heap value is created and its reference count is incrememted. When a heap value falls out of scope, its reference count is decrememnted, if the count is zero it is freed, and if it is a cyclic reference counter then a test for cycles is performed too. For more information on Mylang's garbage collection strategy, see [6](#garbage_collection).

## 5.3 Rule of Three Explanation <a name="rule_of_three_e"></a>

First it is worth noting that Python implements built in primitives on the stack, and everything else on the heap. With this, we notice three big difference between stack and heap values in python, that is, stack values are:

a) Sized - Size is known at compile time
b) Simple - Stack member fields must all be stack types
	i) Types that do not contain any references, i.e. cannot contain other heap values.
	ii) Types that do not contain any OS handles
c) Immutable - Cannot contain any function (other than `__init__` and [getters/setters](#properties)) that changes member variables.

Firstly, a) is required because the size must be known at compile time to allocate on the stack. Next b) is required because a shallow copy of a heap pointer would not respect the reference counting rules required in garbage collection. Finally c) is required because one way values are used is to be passed into functions and mutated in place, which would not be possible with stack types.

Since the size of all user created types is known at compile times, the sized rule is not required. However, another rule is added:

a) Small - Types that are only N machine words long, where N is a value to be determined.

This is required to prevent extremely large classes being copied which would be overly expensive. This gives us our three rules:

## 5.4 Rule of Three <a name="rule_of_three"></a>

a) Small - Types that are only N machine words long, where N is a value to be determined.
b) Simple - Stack member fields must all be stack types
	i) Types that do not contain any references, i.e. cannot contain other heap values.
	ii) Types that do not contain any OS handles
c) Immutable - Cannot contain any function (other than `__init__` and [getters/setters](#properties)) that changes member variables.

## 5.5 Drop <a name="drop"></a>

Drop, similar to Rust's drop, is called when a value goes out of scope. Drop is called at different times depending on the variable location:

- Stack: When the stack variable goes out of scope
- Heap: When the garbage collector algorithm frees the object (see [6](#garbage_collector) for more)

# 6 Garbage Collection <a name="garbage_collection"></a>

For heap allocated variables, Mylang uses reference counting garbage collection and for types that might produce cycles a second type of reference counting that finds and frees cycles is used.

## 6.1 Standard Reference counting <a name="reference_counting"></a>

When the compiler performs its static analysis, it traverses all the classes and their members to determine if a class can be a part of a cycle. If it cannot, then it uses standard reference counting for its garbage collecting strategy.

## 6.2 Collecting cycles <a name="collecting_cycles"></a>

For all classes in a Mylang codespace, the compiler walks through all of them to see if any can be involved in a cycle. If they are, these use a special type of reference counting that, when the count reaches zero also checks for unreachable cycles. See [this](https://crates.io/crates/dumpster) Rust crate for information.

# 7 Function Overloading <a name="function_overloading"></a>

Function overloading is allowed, but only under certain conditions that can be enforced by the compiler. These conditions are outlined in the following sections:

## 7.1 By parameter count <a name="by_count"></a>

Functions can overload by the number of parameters. If multiple overloads exist with the same number of parameter counts, they must be distinguishable by specificity ([7.2](#by_specificity))

## 7.2 By explicit type  <a name="by_specificity"></a>

Functions can also overload by paramater type if one is explicitly mentioned. An overload can exist for a paramater if there are Any number of explicitly typed paramaters, and one or zero overloads where no explicit type is mentioned. This means that if a paramater has an overload of an explicit type, it will use that otherwise it will default to the overload with no explicit type, if there is one.

More than one overload may not exist if a paramater has no explicit type, as it is not possible to know which one to use.

# 8 Control Flow <a name="control_flow"></a>

## 8.1 If <a name="if_statement"></a>

Conditional if statement with optional else block. The compiler calls [`__bool__`](#__bool__) on the condition.

```Python

if condition: 
	# if condition.__bool__() is true
	...
else:
	# If condition.__bool__() is false
	...

```

## 8.2 For <a name="for_statement"></a>

Iterator based for loop. [`__iter__`](#__iter__) is called on the iterable object.

```Python

for item in iterable:
	# Iterates over iterable yielding each element as item
	...
else
	# If we leave the loop via a break, program flow will reach this block
	...
```

## 8.3 While <a name="while_statement"></a>

Loop that continues while some condition is met. The result of the condition expression itself must implement [`__bool__`](#__bool__)

```Python

while condition:
	# Loop over this block while condition.__bool__() evaluates true
	...
else:
	# If we leave the loop via a break, program flow will reach this block
	...
```

## 8.4 Loop <a name="loop_statement"></a>

Loop that continues indefinitely, without conditions. Can be stopped with `break`

```Python

loop:
	# Loop over this block until break statement
	...
```

## 8.5 OkError <a name="okerr_statement"></a>

## 8.6 SomeNone <a name="somenone_statement"></a>

# 9 Grammar <a name="grammar"></a>

Note: The grammar we describe here is the grammar AFTER code has been converted to its syntactic sugar equivalent. This means it does not include operators.

<style>
.d {
    color: #aee440;
    font-weight: bold;
}

.s {
    color: #ff4b8c;
}

.c {
    color: #9c9386;
}
</style>

<span class="c">-- identifier represents identifiers as defined in the C programming language</span>

module = <span class="d">Module</span>(function<span class="s">\*</span> functions, class<span class="s">\*</span> classes)

class = <span class="d">ClassDef</span>(identifier name, function<span class="s">\*</span> functions)

function = <span class="d">FunctionDef</span>(identifier name, identifier<span class="s">\*</span> args, stmt<span class="s">\*</span> body)

stmt = <span class="d">Return</span>(expr<span class="s">?</span> value)  
	 | <span class="d">Assign</span>(expr<span class="s">\*</span> targets, expr value)  
	 | <span class="d">For</span>(expr target, expr iter, stmt<span class="s">\*</span> body, stmt<span class="s">\*</span> orelse)  
	 | <span class="d">While</span>(expr test, stmt<span class="s">\*</span> body, stmt<span class="s">\*</span> orelse)  
	 | <span class="d">Loop</span>(stmt<span class="s">\*</span> body)  
	 | <span class="d">If</span>(expr test, stmt<span class="s">\*</span> body, stmt<span class="s">\*</span> orelse)  
	 | <span class="d">SomeNone</span>(expr value, expr some_target, stmt<span class="s">\*</span> some_body, stmt<span class="s">\*</span> none_body)  
	 | <span class="d">OkErr</span>(expr value, expr ok_target, expr err_target, stmt<span class="s">\*</span> ok_body, stmt<span class="s">\*</span> err_body)  
	 | <span class="d">Expr</span>(expr value)  
	 | <span class="d">Pass</span>  
	 | <span class="d">Break</span>  
	 | <span class="d">Continue</span>  

expr = <span class="d">IfExp</span>(expr test, expr body, expr orelse)  
	 | <span class="d">Dict</span>(expr<span class="s">\*</span> keys, expr<span class="s">\*</span> values)  
	 | <span class="d">Set</span>(expr<span class="s">\*</span> items)  
	 | <span class="d">FormattedString</span>(expr<span class="s">\*</span> values)  
	 | <span class="d">Constant</span>(constant value)  
	 | <span class="d">Attribute</span>(expr value, identifier attr, expr_context ctx)  
	 | <span class="d">Name</span>(identifier id, expr_context ctx)  
	 | <span class="d">List</span>(expr<span class="s">\*</span> items, expr_context ctx)  
	 | <span class="d">SolitarySelf</span>()   
	 | <span class="d">SelfMemberVariable</span>(identifier id)  
	 | <span class="d">SelfMemberFunction</span>(identifier id, expr<span class="s">\*</span> args)
	 | <span class="d">MemberFunction</span>(identifier id, expr exp, expr<span class="s">\*</span> args)  
	 | <span class="d">MyCall</span>(identifier id, expr<span class="s">\*</span> args)  


expr_context = <span class="d">Load</span> | <span class="d">Store</span>
