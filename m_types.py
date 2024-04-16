
# The following classes represent all the 'types' that Mylang objects can be

class Boolean:
    pass


class Integer:
    pass


class Floating:
    pass


class String:
    pass


class Bytes:
    pass


class Vector:
    def __init__(self, element_type):
        self.element_type = element_type


class Dictionary:
    def __init__(self, key_type, value_type):
        self.key_type = key_type
        self.value_type = value_type


class DynamicSet:
    def __init__(self, element_type):
        self.element_type = element_type


class Option:
    def __init__(self, contained_type):
        self.contained_type = contained_type


class Result:
    def __init__(self, ok_type, err_type):
        self.ok_type = ok_type
        self.err_type = err_type


class Function:
    def __init__(self, param_types, return_type):
        self.param_types = param_types
        self.return_type = return_type


class UserClass:
    def __init__(self, identifier):
        self.identifier = identifier
