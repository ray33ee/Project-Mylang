# Contents

- 1 [Introduction](#introduction)
- 2 [Structural Typing](#structural_typing)
	- 2.1 [Special Methods](#special_methods)
		- 2.1.1 [Specials](#specials)
			- 2.1.1.1 [Conversions and casts](#conversions_casts)
				- 2.1.1.1.1 [\_\_float\_\_](#__float__)
				- 2.1.1.1.2 [\_\_int\_\_](#__int__)
				- 2.1.1.1.3 [\_\_index\_\_](#__index__)
				- 2.1.1.1.4 [\_\_bool\_\_](#__bool__)
				- 2.1.1.1.5 [\_\_str\_\_](#__str__)
				- 2.1.1.1.6 [\_\_bytes\_\_](#__bytes__)
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
			- [open](#bf_open)
	- 2.2 [Properties](#properties)
		- 2.2.1 [Getter](#getter)
		- 2.2.2 [Setter](#setter)
- 3 [Built-in Types](#bi_types)
	- 3.1 [Boolean](#bi_bool)
	- 3.2 [Integer](#bi_integer)
	- 3.3 [Float](#bi_float)
	- 3.4 [Id](#bi_id)
	- 3.5 [List](#bi_list)
	- 3.6 [String](#bi_string)
	- 3.7 [Bytes](#bi_bytes)
	- 3.8 [Dictionary](#bi_dict)
	- 3.9 [Set](#bi_set)
	- 3.10 [Option](#bi_option)
	- 3.11 [Result](#bi_result)
- 4 [Exceptionless](#exceptionless)
- 5 [Stack, Heap and the Rule of Three](#stack_heap_rot)
	- 5.1 [Stack](#stack)
	- 5.2 [Heap](#heap)
	- 5.3 [Rule of Three](#rule_of_three)
	- 5.2 [Drop](#drop)
- 6 [Garbage collection](#garbage_collection)
	- 6.1 [Standard Reference Counting](#reference_counting)
	- 6.2 [Collecting Cycles](#collecting_cycles)
- 7 [Function overloading](#function_overloading)
	- 7.1 [By paramater count](#by_count)
	- 7.2 [By specificity](#by_specificity)
- 8 [Control Flow](#control_flow)
	- 8.1 [If](#if_statement)
	- 8.2 [For](#for_statement)
	- 8.3 [Loop](#loop_statement)
- 9 [Grammar](#grammar)

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

#### 2.1.1.1 Conversions and Casts <a name="conversions_casts"></a>

##### 2.1.1.1.1 `__float__` <a name="__float__"></a>

This function should convert a type into a float-like object. For primitive types that implement it, this returns `f64`. It takes no arguments, and the return type has no type restrictions.

##### 2.1.1.1.2 `__int__` <a name="__int__"></a>

Used to convert an object into an integer-like object. For primitives that implement it, this returns `i64`. Takes no arguments and the return type has no restrictions.

##### 2.1.1.1.3 `__index__` <a name="__index__"></a>

Converts an object into a value that can be used to index arrays. Takes no arguments and the return type must be `usize`

##### 2.1.1.1.4 `__bool__` <a name="__bool__"></a>

Converts an object into a boolean value. Takes no arguments and the return type must be `bool`. This function is automatically called by any expression in statements that require boolean expressions (`if`, `while`, etc.)

##### 2.1.1.1.5 `__str__` <a name="__str__"></a>

Converts an object into a string. Takes no arguments and must return `String`. This function is automatically called by any expression in formatted `print` statements.

##### 2.1.1.1.6 `__bytes__` <a name="__bytes__"></a>

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

##### 2.1.1.8.2 `__le__` <a name="__le__"></a>

##### 2.1.1.8.3 `__eq__` <a name="__eq__"></a>

##### 2.1.1.8.4 `__ne__` <a name="__ne__"></a>

##### 2.1.1.8.5 `__gt__` <a name="__gt__"></a>

##### 2.1.1.8.6 `__ge__` <a name="__ge__"></a>

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

### 2.1.3 Built-in functions <a name="bi_functions"></a>

## 2.2 Properties <a name="properties"></a>

Properties work like getters and setters on objects. Getters and setters can be implemted for actual member variables, but they can be implemented for any variable name whether it is a member variable or not. See the following titles for more.

### 2.2.1 Getter  <a name="getter"></a>

Take the snippet `a = object.value`. This is syntactic sugar for `a = object.__get_value__()` and provided `object` implements `__get_value__`, this is valid code. It does not matter whether or not `value` is a member variable or not. All Mylang checks for is that the correct function is implemented, then calls it.

### 2.2.2 Setter  <a name="setter"></a>

Take the snippet `object.value = a` which is syntactic sugar for `object.__set_value__(a)`. Once again, as long as `object` implements the function for `a` as an argument, this is valid code because the compiler only cares if the function is implemnented, it does not check that `value` is a member variable.

# 3 Built-in Types <a name="bi_types"></a>

# 4 Exceptionless <a name="exceptionless"></a>

# 5 Stack, Heap and the Rule of Three <a name="stack_heap_rot"></a>

## 5.1 Stack <a name="stack"></a>

## 5.2 Heap <a name="heap"></a>

## 5.3 Rule of Three <a name="rule_of_three"></a>

## 5.4 Drop <a name="drop"></a>

- Drop is only called on heap values

# 6 Garbage Collection <a name="garbage_collection"></a>

## 6.1 Standard Reference counting <a name="reference_counting"></a>

## 6.2 Collecting cycles <a name="collecting_cycles"></a>

# 7 Function Overloading <a name="function_overloading"></a>

## 7.1 By paramater count <a name="by_count"></a>

## 7.2 By specificity  <a name="by_specificity"></a>

# 8 Control Flow <a name="control_flow"></a>

## 8.1 If <a name="if_statement"></a>

## 8.2 For <a name="for_statement"></a>

## 8.3 Loop <a name="loop_statement"></a>

# 9 Grammar <a name="grammar"></a>

Note: The grammar we describe here is the grammar AFTER code has been converted to its syntactic sugar equivalent.

