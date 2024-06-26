import os

import logging
import re

import m_types

logger = logging.getLogger(__name__)

# Used to convert rust template code into a the built_in_map used to obtain return types for built in functions
class Parser:



    # Thin wrapper around lists that can be hashed
    # Be careful not to externally mutate keys
    class HashableList:

        def __init__(self, iterable=[]):
            self.l = list(iterable)

        def __hash__(self):
            h = 0

            for i, item in enumerate(self.l):
                h ^= hash(hash(item) ^ hash(i))

            return h

        def __eq__(self, other):
            return self.l == other.l

        def __repr__(self):
            return f"HashableList({repr(self.l)})"

    path = "E:\\Software Projects\\IntelliJ\\mylang_template\\src\\built_ins"

    def __init__(self):

        self.map = {}

        for file in os.listdir(self.path):
            class_name = file[:-3]

            self.parse_file(class_name)



    # Some functions do not conform to the rules we use, so rather than adding complex code to include them,
    # we simply manually add them in this function
    def add_exceptions(self):
        pass

    def get_closing_brace(self, string):
        tracker = 0
        index = 0

        open_brace = None

        for i, ch in enumerate(string):
            if ch == "{":

                if open_brace is None:
                    open_brace = i
                    tracker += 1
                    continue

                tracker += 1
            elif ch == "}":
                tracker -= 1

            if tracker == 0 and open_brace is not None:
                return string[open_brace+1:i], string[:open_brace], i+1

        return None



    def parse_file(self, class_name):

        path = self.path + "\\" + class_name + ".rs"

        file_contents = ""
        with open(path) as fh:
            file_contents = fh.read()

        # Search for the impl block
        impl = file_contents.find(f"impl {class_name}")

        # If we can't find an impl block, look for the '/*START PARSE HERE*/' identifier
        if impl == -1:
            impl = file_contents.find(f"/*START PARSE HERE*/")

        # If we cannot find an impl block or identifier, error
        if impl == -1:
            logger.error(f"Could not find impl block or '/*START PARSE HERE*/' in '{class_name}' ({path})")
            raise "see log"

        inner_impl, _, _ = self.get_closing_brace(file_contents[impl:])

        while True:

            ret = self.get_closing_brace(inner_impl)

            if ret is None:
                break

            _, signature, end = ret

            self.parse_function(class_name, ''.join(signature.split()))

            inner_impl = inner_impl[end:]

    def parse_function(self, class_name, signature):
        r = self.parse_signature(signature)
        if r is None:
            return

        name, arg_types, ret_type = r

        self.add_item(class_name, name, arg_types, ret_type)


    def parse_signature(self, signature):

        regex = "pubfn_ZF(?:[0-9]+)N(?:[0-9]+)(?P<name>[_0-9a-zA-z]+)E[_0-9a-zA-z]*\\(&(?:mut)?self(?P<args>(?:,[_0-9a-zA-z]+:[_0-9a-zA-z]+)*)\\)(?:->(?P<ret>[_0-9a-zA-z]+))?"

        m = re.search(regex, signature)

        if m is not None:

            name = m.group("name")
            arg_types = self.parse_args(m.group("args"))
            ret_type = self.parse_type(m.group("ret"))

        else:
            return None

        return name, arg_types, ret_type

    def parse_args(self, arg_string):
        regex = ",[_0-9a-zA-z]+:(?P<type>[_0-9a-zA-z]+)"

        return [self.parse_type(m.group("type"), True) for m in re.finditer(regex, arg_string)]

    def parse_type(self, t, instantiate=False):

        if t == "Integer":
            r = m_types.Integer
        elif t == "Float":
            r = m_types.Floating
        elif t == "Bool":
            r = m_types.Boolean
        elif t == "String":
            r = m_types.String
        elif t is None:
            r = m_types.Ntuple([])
        elif t == "T": # Templated list
            r = "element_type"
        elif t == "O": # Templated Option
            r = "contained_type"
        else:
            logger.error(f"Not implemented for {t}")
            raise NotImplemented()

        if instantiate and type(r) is not str:
            return r()
        else:
            return r

    def add_item(self, class_name, func_name, args, ret_type):
        print((class_name, func_name, args, ret_type))

    # Function to find the return type of a mamber function 'func_name' in class 'class_name' with 'args.
    # If the lookup fails then the function should panic, warning the user that there is no entry
    # (suggest that maybe the function is a Rust template and to make sure it is in the 'add_exceptions' function)
    def get_item(self, class_name, func_name, args):
        pass