

class __ParameterRestriction__(object):

    def __init__(self, **kwargs):
        pass

    def __call__(self, value, obj=None):
        return self.validate(value, obj)

    def validate(self, value, obj=None):
        """ Returns True if the value passes the restriction """
        return True

    def __repr__(self):
        return "General Restriction" 


class RestrictNothing(__ParameterRestriction__):
    """ No restriction on the property value """
    def __repr__(self):
        return 'No Restriction'


class RestrictType(__ParameterRestriction__):
    """ Restrict the type or types the argument can have. Pass a type or tuple of types """
    def __init__(self, allowed_types):
        self.allowed_types = ()
        self .__types_set = False
        self.__add_type__(allowed_types)
        if not self.__types_set:
            raise ValueError("allowed_typed of Type Restriction should be set on initialization")

    def __add_type__(self, type_type):
        if isinstance(type_type, type):
            self.allowed_types += (type_type,)
            self .__types_set = True
        elif isinstance(type_type, (tuple, list)):
            for T in type_type:
                self.__add_type__(T)
        else:
            raise TypeError("Restrict type should have a 'type' or 'tuple' of types as argument")

    def validate(self, value, obj=None):
        return isinstance(value, self.allowed_types)

    def __repr__(self):
        return 'Type Restriction: ' + ','.join([t.__name__ for t in self.allowed_types])

    def __str__(self):
        return self.__repr__()


