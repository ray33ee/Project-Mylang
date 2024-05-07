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
				- 2.1.1.5.1 [\_\_get_VARIABLE\_\_](#__get_VARIABLE__)
				- 2.1.1.5.2 [\_\_set_VARIABLE\_\_](#__set_VARIABLE__)
			- 2.1.1.6 [Binary Operator](#binop)
			- 2.1.1.7 [Unary Operator](#unop)
			- 2.1.1.8 [Compares](#cmpop)
				- 2.1.1.8.1 [\_\_lt\_\_](#__lt__)
				- 2.1.1.8.2 [\_\_le\_\_](#__le__)
				- 2.1.1.8.3 [\_\_eq\_\_](#__eq__)
				- 2.1.1.8.4 [\_\_ne\_\_](#__ne__)
				- 2.1.1.8.5 [\_\_gt\_\_](#__gt__)
				- 2.1.1.8.6 [\_\_ge\_\_](#__ge__)
			- 2.1.1.9 [Augmented Assign](#augop)
			- 2.1.1.10 [Iterable](#iterable)
				- 2.1.1.10.1 [\_\_iter\_\_](#__iter__)
				- 2.1.1.10.1 [\_\_next\_\_](#__next__)
			- 2.1.1.11 [Callable](#callable)
				- 2.1.1.11.1 [\_\_call\_\_](#__call__)
			- 2.1.1.12 [Complex](#complex)
				- 2.1.1.12.1 [\_\_real\_\_](#__real__)
				- 2.1.1.12.2 [\_\_imag\_\_](#__imag__)
		- 2.1.2 [Operator Overloading](#operator_overloading)
		- 2.1.3 [Built-in functions](#bi_functions)
	- 2.2 [Properties](#properties)
		- 2.2.1 [Getter](#getter)
		- 2.2.2 [Setter](#setter)
- 3 [Built-in Types](#bi_types)
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
- 8 [Grammar](#grammar)

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

#### 2.1.1.1.1 `__float__` <a name="__float__"></a>

This function should convert a type into a float-like object. For primitive types that implement it, this returns `f64`. It takes no arguments, and the return type has no type restrictions.

#### 2.1.1.1.2 `__int__` <a name="__int__"></a>

Used to convert an object into an integer-like object. For primitives that implement it, this returns `i64`. Takes no arguments and the return type has no restrictions.

#### 2.1.1.1.3 `__index__` <a name="__index__"></a>

Converts an object into a value that can be used to index arrays. Takes no arguments and the return type must be `usize`

#### 2.1.1.1.4 `__bool__` <a name="__bool__"></a>

Converts an object into a boolean value. Takes no arguments and the return type must be `bool`. This function is automatically called by any expression in statements that require boolean expressions (`if`, `while`, etc.)

#### 2.1.1.1.5 `__str__` <a name="__str__"></a>

Converts an object into a string. Takes no arguments and must return `String`. This function is automatically called by any expression in formatted `print` statements.

#### 2.1.1.1.6 `__bytes__` <a name="__bytes__"></a>

Converts an object into a list of bytes. Takes no arguments and should return a bytes-like object.

#### 2.1.1.X `__unwrap__`

This function is called on error or option types to obtain there underlying ok value (for error types) or some value (for options). For other types, `__unwrap__` should return `self`

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

# 8 Grammar <a name="grammar"></a>

Note: The grammar we describe here is the grammar AFTER code has been converted to its syntactic sugar equivalent.

