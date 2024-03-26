Mylang reference counting

# About

Mylang is a Python like language and syntax that produces code more like Rust. Rust uses owndership, borrowing and reference counted objects to solve memory safety issues. Reference counting has its issues, namely cyclic references. This is solved using weak references, but this requires input and knowlege of the programmer to do so. Here we propose a scheme to reference count even cyclic variables if the language is statically typed, at the expense of a runtime cost.

# Fact/Proofs

Here we present a list of facts and proofs/demonstrations, some relevant some not so:

### Fact 1: Reference counting alone is not enough to solve cyclic references

### Proof:

Take two objects, A and B and a stack variable r_1. Suppose r_1 refers to A, A refers to B, and B refers back to A:

r_1 ---> A ----> B
		 ^       |
		 ---------

r_1 is a stack variable so contains no reference count. A's count is 2 (one from r_1 and one from B) and B's count is 1 (one from A). When r_1, falls out of scope, the reference count for A is decremented to 1. Now we have

         A ----> B
		 ^       |
		 ---------

Both A and B have a count of 1, but are not referenced by any root variables, so are garbage that will never be collected by the reference counting system.

### Fact 2: We can identify possible cycles at compile time

### Proof:

Since the language must be static, the types of all variables (stack and heap) are known at compile time (this excludes polymorphism RIP) and so cycles can be traced. By iterating over each type, and recursively following any stored references, we can identify cycles. For example, similar to the example above, we have types X and Y. X contains a reference to a Y object, and Y contains a reference to an X object. The compiler knows that X and Y contain these references since it is a static language, and so can trace the references to identify cycles. If we apply this algorithm to all types, we can obtain a set of types that can form cycles.

### Fact 3: We cannot know for certain whether these compile time cycles will definitely be cycles at runtime

If references exist in an array, it is possible for a link to only be known at runtime. Take the r_1, A, B example from Fact 1. Say that, instead of a reference to A, B contained a list of references to A. If that list contains a reference to A, there is a cycle. If the list is empty, then r_1 points to A, a points to B and this is it. There is no cycle, and normal reference counting is adequate here. Since the nature of the list may not only be known at runtime, this cannot be resolved at compile time.

### Fact 4: Confirming a set of objects forms a cycle must be performed at runtime

### Proof: 

This is a direct consequence to Fact 3. Using the list of types that can form cycles (See Fact 2) we can then obtain a list of variables that can form cycles (i.e. any variable that is of a type that can form cycles) and we can pass these to a runtime algorithm that checks for cycles.

### Fact 5: The topology of possible cycles cannot be known at compile time

### Proof:

Imagine a type C that contains a list of references to C. At runtime, any tree can be made with enough Cs. One large cycle across all objects, hundreds of small cycles, or thousands of cycles with evey C pointing to every other C. There are situations where this is entirely determined at runtime.

### Fact 6: A cycle can itself be treated as a single reference counted object.

### Proof:

If the topology of the cycle stays the same, then the internal references between nodes in a cycle don't change. So the cycle can be considered one super object. If we keep track of references to this super object (i.e. an increase to any of the child objects reference count increases the count of the overall object) then when the overall count is 0, we can deallocate all objects in the cycle.

### Fact 7: Non-cycles cannot be treated as cycles as this can result in garbage not collected

Imagine a large cycle. If this cycle breaks up into two indepepdent pieces and one of the pieces looses all references to outside itself, this piece will be garbage. By sticking to the reference count of the original unbroken cycle, this piece would not be freed and would be uncleaned garbage.

### Fact 8: When a cycle is broken, we must stop treating the set of objects as one cycle and instead as several reference counted objects

### Proof:

Because Fact 7 says we cannot treat non-cycles as cycles. This means that when a cycle is broken and it turns into non-cycles, it must not be treated as a cycle

### Fact 9: Even when a ser of objects are deemed a cycle, their individual reference counts must be kept

## Proof:

Reference counts must be kept up to data in case cycles are broken and must revert to individual counting, as in Fact 8. When keeping individual counts in a cycle, the same rules apply. If any reference count becomes 0, the object is freed.

### Fact 10: THe compiler can find assignments that start cycles

### Proof:

Lets start with

r_1 ---> A ----> B

where r_1 is a stack variable pointing to A, and A contains a pointer to B, and B contains a list of pointers to A, but this list starts empty. In this example there is the possibility for a cycle, but no cycle yet. When the list in B is populated with a reference to A, we have

r_1 ---> A ----> B
		 ^       |
		 ---------

which forms a cycle. Therefore the compiler can identify the step where the cycle is completed. It is here that code can be placed check a cycle has been created or broken. Some/nones and mutable containers are prime candidates for checking. Changing to a some, appending containers and assigning elements in containers can start cycles. Changing back to none, removing elements and assigning elements in containers can break cycles.

# Definitions

- At compile time, all types are sorted into two categories. At risk, and not at risk of producing cycles at runtime. These are known as At risk and not at risk types.

```Python
class A:
	def __init__():
		self.a = []

	def attach(a):
		self.a.append(a)

class B:
	def __init__(a):
		self.b = a

def main():
	a_1 = A()
	a_2 = A()
	a_3 = A()

	# For a cycle of A objects
	a_1.attach(a_2)
	a_2.attach(a_3)
	a_3.attach(a_1)

	# B points to the first a_1, but it does not contribute to the cycle.
	b = B(a_1)


```

In the above example, `A` contains a list of references to other `A` obejcts (this is deduced by the compiler as we pass A objects to the `attach` function). `B` contains a reference to an `A` object, but does not itself form a cycle. `A` would be considered an at risk type, and `B` would be a not at risk type. Note that the definitions of `A` and `B` alone are not enough to determine cyclic nature, as the types of `self.a` and `self.b` are not known without type deduction. 

- At compile time, all variables are sorted into the same two categories above, depending on whether they are an at risk or not at risk type. These are known as at risk and not at risk variables.

In the above example, objects `a_1`, `a_2` and `a_3` are at risk variables whereas `b` is not at risk.

- For at risk types, there are two catagories, types containing references set at compile time (Think of a class that takes a reference as an argument and never changes it) and references set at runtime (Think of a class that contain a some/none of a reference, or a list of references or a reference that can be changed) which are refered to as hard and soft references, respectively.

```Python

class C:
	def __init__(d):
		self.c = d

class D:
	def __init__():
		self.d = []

	def attach(c):
		self.d.append(c)

	def detach(c):
		self.d.remove(c)

def main():
	d = D()

	c = C(d)

	# The following call creates a cycle
	d.attach(c)

	# The following call breaks the cycle and can be freed by reference counting
	d.detach(c)

```

In the above example, the reference in `C` is a hard reference as it is set at compile time. This reference to `D` exists from the creation to the destruction of `C`. However, the reference in `D` is soft as it is setup at runtime. Linking the soft reference (i.e. `d.attach(c)`) creates a cycle. Similarly, if we were to remove this reference at runtime, this would break the cycle. Hard cycles do not need to be tracked as they are static and known at compile time. Only soft references need to be tracked, when they are created and when they are destroyed.

Also a series of hard links does not need to be traversed by the GC, they can be treated as one whole link and skipped to the end of the hard link set.

- Variables that contain soft references are called soft variables

- Functions that create soft references at runtime are of particular interest because these create cycles.

In the above example, `attach` and specifically calling `append` on a list of references creates the cycle.

- Functions that destroy soft references at runtime are also important because they turn cycles back into structures that can be freed with normal reference counting.
 
In the above example, `detach` and specifically calling `remove` on the list of references breaks the cycle.

- We create our own function that takes a single object and a newly created soft reference in that object, and applies a depth-first search of the references and objects. If any of the references lead back to the original object, we have a cycle. If it does not, this object is not in a cycle. 

Applying this algorithm to every function that can create or break cycles gives us an automatic way to detect cycle creation and destruction.

- When a new reference is created that forms a cycle (in accordance with the previous point) a copy of the reference and a reference to the object can be stored in the engine. This can be used to traverse the cycle by the engine itself.

- During compilation, the compiler can keep a table of all types and the offsets for any references they contain. This can be used to traverse variables based on type

# Strategy

At compile time we iterate over all types to determine at risk types, then any variables to determine at risk variables. Any variable with at risk types that also contain or are soft references are added to a compile time list.

Extra information needs to be bundles with these at risk types at runtime to allow traversal. Hard links and not at risk variables to not need this extra information.

At runtime the list is traversed to detect cycles using the extra information. Take the following simple example

```Python 

class A:
	def __init__(b):
		self.b = b

class B:
	def __init__():
		self.a = None

	def set_a(a):
		self.a = Some(a)

def initialise():
	b = B()

	a = A(b)

	b.set_a(a)

	return a

def main():
	r = initialise()

```

The compiler identifies A and B as at risk by traversing all user defined types and their references. Variables a, b and r are flagged as at risk variables. Links from stack variables are ignored as they are are cleaned up by the stack. The assignment of `self.a = Some(a)` forms a soft reference as it is assigned, and not part of the object's constructor. Every time the soft variable `self.a` is assigned to, the compiler adds extra code to add the address of the soft variable into a table or map. Also, because A and B are at risk classes, extra information is prepended to them which is used to help the GC traverse them. (This extra information might be a few bits of the reference count used as an index to an array of class metadata created at compile time) 

```Python

class Parent:
	def __init__():
		self.children = []


	def add_child(child):
		self.children.append(child)


class Child:
	def __init__(parent):
		self.parent = parent

class Master:
	def __init__(parent):
		self.parent = parent

def initialise():
	parent = Parent()

	master = Master(parent)

	child_1 = Child(parent)
	child_2 = Child(parent)
	child_3 = Child(parent)

	parent.add_child(child_1)
	parent.add_child(child_2)
	parent.add_child(child_3)

	return master

def main():
	initialise()
	

```

First the compiler will iterate over all types (Parent, Child, Master and List<Child>) to identify any cycles. A (Parent -> List<&Child> -> Child -> Parent) cycle exists, so all of these types are flagged as at risk. All remaining types (Master) are flagged as not at risk. 

Any variable that is an at risk type (parent, child_1, child_2, child_3, self.children, self.parent in Child) is investigated for the type of reference it contains. parent, child_1, child_2, child_3, self.children and self.parent in Child are all hard references. The soft references are the references stored in the list itself. However, instead of 

# Example

Examples are in Mylang.

```Python

class A:
	def __init__(b):
		self.b = b

class B: 
	def __init__():
		self.a_list = []

	def attach(a):
		self.a_list.append(a)

	def detatch(a):
		self.a_list.remove(a)

def cycle():
	# Create an empty B object
	b = B()

	# Create an A object that points to our b
	a = A(b)

	# Go back and attach a pointer to a in our b. At this point, a circular reference is completed. 
	# At this point, the a,b pair should be treated as a single reference counted object with two references (the stack variables a and b)
	b.attach(a)

	# When a and b fall out of scope, the heap objects a and b point to each other, with a reference count of 1. Normal reference counting would end here 
	# as the cycle is lost. However, because we have treated a and b as a single item, when a and b fall out of scope the count goes to zero. This means that the
	# a, b pair have no more references (except to each other) and so must be freed. We do this by arbitrarily picking an item in the cycle, setting its count to 0.

	# Lets say the function doesn't end here, and we execute the following line:
	# b.remove(b)

	# At this point the cycle is broken. We still perform the cycle reference count implemented automatically by the compiler, but this time when a and b fall out of scope, the reference count to a falls to 0, so it is freed. This drops the reference count of b to 0, which is also freed.

	


```

# Bane

Take the following class

```Python

class F:
	def __init__():
		self.f = []


	def attach(f: F):
		self.f.append(f)

```

The class `F` represents an interesting problem in handling reference counted cycles. At runtime, any directed graph can be made with enough objects `F` and so any combination of cycles can be made. Worse off, all the connections are soft references, so any time `attach` is called a cycle may be created. This is certainly an extreme example of cyclic references, but it demonstrates a very possible albeit extreme case. Solving this case should solve most if not all cyclic problems.

# Soft reference

Soft reference is a special type that holds a pointer. When a soft reference is instantiated, a copy of the address and the address of the soft reference itself is added to the garbage collector. When the soft reference is deleted, the copy is removed from the list.