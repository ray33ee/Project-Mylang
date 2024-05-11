import m_types
import mangler


class Demangler:

    def __init__(self):
        pass

    def demangle_identifier(self, string):
        namespaces = []

        if string[0] != "N":
            return None, string

        string = string[1:]

        while string[0] != "E":

            name, string = self.get_lengthed_data(string)

            namespaces.append(name)

        if string[0] != "E":
            raise "demangle error"

        return mangler.Name(namespaces), string[1:]

    def demangle_type(self, string):
        ident = string[0]

        if ident == "b":
            return m_types.Boolean(), string[1:]
        elif ident == "i":
            return m_types.Integer(), string[1:]
        elif ident == "f":
            return m_types.Floating(), string[1:]
        elif ident == "a":
            return m_types.ID(), string[1:]
        elif ident == "l":
            t, mstring = self.demangle_type(string[1:])
            return m_types.Vector(t), mstring
        elif ident == "u":
            return m_types.String(), string[1:]
        elif ident == "m":
            return m_types.Bytes(), string[1:]
        elif ident == "d":
            a, mstring = self.demangle_type(string[1:])
            b, nstring = self.demangle_type(mstring)
            return m_types.Dictionary(a, b), nstring
        elif ident == "s":
            t, mstring = self.demangle_type(string[1:])
            return m_types.DynamicSet(t), mstring
        elif ident == "o":
            t, mstring = self.demangle_type(string[1:])
            return m_types.Option(t), mstring
        elif ident == "r":
            a, mstring = self.demangle_type(string[1:])
            b, nstring = self.demangle_type(mstring)
            return m_types.Result(a, b), nstring
        elif ident == "C":
            return self.demangle_class(string)
        else:
            raise "Demangle error"

    def demangle_class(self, string):

        fields = []

        string = string[1:]

        data, string = self.get_lengthed_data(string)

        namespaces, field_text = self.demangle_identifier(data)

        while field_text != "":

            field, field_text = self.demangle_type(field_text)

            fields.append(field)


        return mangler.Class(fields, namespaces), string

    def demangle_function(self, string):

        args = []
        ret = None

        while True:
            if string == "":
                break
            else:
                if string[0] == "R":
                    break

            arg, string = self.demangle_type(string)

            args.append(arg)

        if string != "":
            if string[0] == "R":
                ret, string = self.demangle_type(string[1:])

                if string != "":
                    raise "Demangle error"
            else:
                raise "Demangle error"

        return mangler.Function(args, ret)


    def get_lengthed_data(self, string):

        start = -1
        for i in range(len(string)):
            if not string[i].isnumeric():
                start = i
                break

        if start == -1:
            raise "Could not find non numeric character in namespace list"


        l = int(string[:start])

        data = string[start:start + l]

        string = string[start + l:]

        return data, string

    def __call__(self, string):

        if string[:2] != "_Z":
            raise "Demangle error"

        string = string[2:]

        namespaces, string = self.demangle_identifier(string)

        if string[0] == "F":
            return namespaces, self.demangle_function(string[1:])
        elif string[0] == "C":
            return namespaces, self.demangle_class(string)[0]
        else:
            raise "demangle error"



