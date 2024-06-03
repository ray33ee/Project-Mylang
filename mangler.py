import demangler
from m_types import MType

# Describes an identifier, such as the name of a function or class.
# Constructed of a set of strings which represent namespaces, modules, any kind of scoped access
class Name:
    def __init__(self, names):
        if type(names) is str:
            self.names = [names]
        elif type(names) is list:
            self.names = names

    def mangle(self):
        s = "N"

        for name in self.names:
            s = s + str(len(name)) + name

        return s + "E"

    def __repr__(self):
        s = self.names[0]

        for i in range(len(self.names) - 1):
            s = s + "." + self.names[i+1]

        return s


class Function:
    def __init__(self, args):
        self.args = args

    def mangle(self):
        mang = "F"

        for a in self.args:
            mang = mang + a.mangle()

        return mang

    def __repr__(self):
        return "Function(" + repr(self.args) + ")"


class Class(MType):
    def __init__(self, fields,  name: Name = None):
        self.fields = fields
        self.name = name

    def mangle(self):
        if self.name:
            mang = self.name.mangle()
        else:
            mang = ""

        for field in self.fields:
            mang = mang + field.mangle()

        return "C" + str(len(mang)) + mang

    def __repr__(self):
        if self.name:
            return "Class('" + repr(self.name) + "', " + repr(self.fields) + ")"
        else:
            return "Class(" + repr(self.fields) + ")"





class Mangle:
    def __init__(self, *args):
        if len(args) == 1:
            s = args[0]
            if type(s) is not str:
                raise "Single argument constructor must contain a string"
            self.mangled_string = s
            d = demangler.Demangler()
            self.name, self.body = d(s)
        elif len(args) == 2:
            n = args[0]
            b = args[1]

            if type(n) is str:
                mangled_name = Name(n).mangle()
            else:
                mangled_name = n.mangle()

            self.mangled_string = "_Z" + mangled_name + b.mangle()
            self.name = n
            self.body = b

        else:
            raise "Only accepts 1 or 2 args"

    def get_name(self):
        return self.name.names[-1]

    def __getitem__(self, item):
        return self.mangled_string[item]

    def __hash__(self):
        return hash(self.mangled_string)

    def __eq__(self, other: str):
        return self.mangled_string == other

    def __str__(self):
        return str(self.mangled_string)

    def __repr__(self):
        return repr(self.mangled_string)


def mangler_demanger_test(body, verbose=False):

    if type(body) is list:
        for b in body:
            mangler_demanger_test(b, verbose)
    else:
        identifier = Name("test")

        mangled = Mangle(identifier, body)
        demangled = Mangle(str(mangled))

        bod = demangled.body

        if verbose:
            print("Body:      " + repr(body))
            print("Demangled: " + repr(bod))
            print("Mangled:   " + str(mangled))



        assert repr(bod) == repr(body)



