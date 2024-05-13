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





# Take a name (as a list of namespaces to allow scoped name) and a body (as either a function or a class) and
# produce a mangled string identifier
class Mangler:
    def __init__(self):
        pass

    def __call__(self, name: Name, body):
        return "_Z" + name.mangle() + body.mangle()



def mangler_demanger_test(body, verbose=False):

    if type(body) is list:
        for b in body:
            mangler_demanger_test(b, verbose)
    else:
        identifier = Name("test")

        m = Mangler()

        mangled = m(identifier, body)


        d = demangler.Demangler()

        _, bod = d(mangled)

        if verbose:
            print("Body:      " + repr(body))
            print("Demangled: " + repr(bod))
            print("Mangled:   " + mangled)



        assert repr(bod) == repr(body)