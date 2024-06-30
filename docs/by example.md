
# Mylang by example

This document includes Mylang example code, explanations, and the corresponding rust code created

# Hello world

```Python

def main():
	print("Hello world!")

```

```Rust

fn main() {
	println!("Hello world!");
}

```

# Templating

```Python

def print_object(x):
	print(x)

def main():

	print(300)
	print(True)


```

```Rust

fn _ZN12print_objectEFi(x: i64) {
	println!("{}", x.__str__())
}

fn _ZN12print_objectEFb(x: bool) {
	println!("{}", x.__str__())
}

fn main() {
	_ZN12print_objectEFi(300)
	_ZN12print_objectEFb(true)
}

```

# Structural typing

```Python

def to_string(x):
	return str(x)

def main():
	print(to_string(4))
	print(to_string(True))

```

```Rust

fn _ZN9to_stringEFi(x: i64) {
	return x.__str__()
}

fn _ZN9to_stringEFb(x: bool) {
	return x.__str__()
}

```

# Classes

```Python

class Complex:
	def __init__(real, imag):
		self.real = real
		self.imag = imag

	def __get_real__():
		return self.real

	def __get_imag__():
		return self.imag

	def __str__(self):
		return f"{self.real} + {self.imag}i"

def main():
	c1 = Complex(1, 2)
	c2 = Complex(1.0, 2.0)

	print(c1)
	print(c2)

```

```Rust

#[derive(Copy, Clone)]
struct _ZN7ComplexEC2ii {
	real: i64,
	imag: i64,
}

impl _ZN7ComplexEC2ii {
	fn _ZN8__init__EFii(real: i64, imag: i64) -> Self {
		Self {
			real,
			imag,
		}
	}

	fn _ZN7__str__EF(& self) -> String {
		return format!("{} + {}i", self.real, self.imag)
	}
}

#[derive(Copy, Clone)]
struct _ZN7ComplexEC2ff {
	real: f64,
	imag: f64,
}

impl _ZN7ComplexEC2ff {
	fn _ZN8__init__EFff(real: f64, imag: f64) -> Self {
		Self {
			real,
			imag,
		}
	}

	fn _ZN7__str__EF(& self) -> String {
		return format!("{} + {}i", self.real, self.imag)
	}
}

fn main() {
	let c1 = _ZN7ComplexEC2ii::_ZN8__init__EFii(1, 2);
	let c2 = _ZN7ComplexEC2ff::_ZN8__init__EFff(1.0, 2.0);

	println!("{}", c1._ZN7__str__EF())
	println!("{}", c2._ZN7__str__EF())
}

```

# Properties

```Python

class Complex:
	def __init__(real, imag):
		self.real = real
		self.imag = imag

	def __get_real__(self):
		return self.real

	def __get_imag__(self):
		return self.imag

	def __real__(self):
		return self.real

	def __imag__(self):
		return self.imag

	def __add__(self, rhs):
		return Complex(real(self) + real(rhs), imag(self) + imag(rhs))

	def __str__(self):
		return f"{self.real} + {self.imag}i"

def main():
	c1 = Complex(1, 2)
	c2 = Complex(1.0, 2.0)

	c3 = c2 + c1

	c1 = c1 + 5

	print(c1)
	print(c2)
	print(c3)

```

```Rust

#[derive(Copy, Clone)]
struct _ZN7ComplexEC2ii {
	real: i64,
	imag: i64,
}

impl _ZN7ComplexEC2ii {
	fn _ZN8__init__EFii(real: i64, imag: i64) -> Self {
		Self {
			real,
			imag,
		}
	}

	fn _ZN12__get_real__EF(& self) -> i64 {
		return self.real
	}

	fn _ZN12__get_imag__EF(& self) -> i64 {
		return self.imag
	}

	fn _ZN8__real__EF(& self) -> i64 {
		return self._ZN12__get_real__EF()
	}

	fn _ZN8__imag__EF(& self) -> i64 {
		return self._ZN12__get_imag__EF()
	}

	fn _ZN7__add__EFi(& self, rhs: i64) -> _ZN7ComplexEC2ii {
		return _ZN7ComplexEC2ii::_ZN8__init__EFii(self._ZN8__real__EF().__add__(rhs.__real__()), self._ZN8__imag__EF().__add__(rhs.__imag__()))
	}

	fn _ZN7__str__EF(& self) -> String {
		return format!("{} + {}i", self.real, self.imag)
	}
}

```

# Function Overloading

# Type annotation
