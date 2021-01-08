from collections.abc import MutableMapping


class VarDict(MutableMapping):
    def __init__(self, data=()):
        self.mapping = {}
        self.update(data)       # calls self.__setitem__()

    def __getitem__(self, key):
        if not key.isalpha():
            raise SyntaxError("Invalid identifier")  # var name can only contain letters

        try:
            return self.mapping[key]

        except KeyError:
            raise NameError("Unknown variable")

    def __delitem__(self, key):
        try:
            del self.mapping[key]

        except KeyError:
            raise NameError("Unknown variable")

    def __setitem__(self, key, value):
        if not isinstance(key, str) or not key.isalpha():
            raise SyntaxError("Invalid identifier")  # var name can only contain letters

        elif not isinstance(value, int):
            if isinstance(value, str):            # value stores a variable
                try:
                    self.__getitem__(value)
                    self.mapping[key] = value

                except SyntaxError:
                    raise ValueError("Invalid assignment")      # "Invalid identifier" for the variable in value

                except KeyError as e:               # the variable in value doesn't exist
                    raise NameError(e.args[0])     # "Unknown variable" for the variable in value

            else:
                raise TypeError("Invalid assignment")

        else:
            self.mapping[key] = value

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

    def __repr__(self):
        return f"{type(self).__name__}({self.mapping})"
