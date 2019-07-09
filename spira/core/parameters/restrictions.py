

class __ParameterRestriction__(object):

    def __init__(self, **kwargs):
        pass

    def __and__(self, other):
        if isinstance(other, __ParameterRestriction__):
            return __ParameterRestrictionAnd__(self, other)
        elif other is None:
            return self
        else:
            raise TypeError("Cannot AND __PropertyRestriction__ with %s" % type(other))

    def __call__(self, value, obj=None):
        return self.validate(value, obj)

    def validate(self, value, obj=None):
        """ Returns True if the value passes the restriction """
        return True

    def __repr__(self):
        return "General Restriction" 


class __ParameterRestrictionAnd__(__ParameterRestriction__):
    def __init__(self, restriction1, restriction2):
        self.restriction1 = restriction1
        self.restriction2 = restriction2

    def validate(self, value, obj=None):
        return self.restriction1(value, obj) and self.restriction2(value, obj)

    def __repr__(self):
        return "(%s and %s)" % (self.restriction1, self.restriction2)


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
        if hasattr(value, '__call__'):
           value = value()
        return isinstance(value, self.allowed_types)

    def __repr__(self):
        return ' Type Restriction: ' + ', '.join([t.__name__ for t in self.allowed_types])

    def __str__(self):
        return self.__repr__()


class RestrictRange(__ParameterRestriction__):
    """ Restrict the parameter to be in a given range. """
    def __init__(self, lower=None, upper=None, lower_inc=True, upper_inc=False):
        self.lower = lower
        self.upper = upper
        self.lower_inc = lower_inc
        self.upper_inc = upper_inc
        if lower is None and upper is None:
            raise ValueError("Range Restriction should have an upper or lower limit")
        if not upper is None and not lower is None:
            if lower > upper:
                raise ValueError("lower limit should be smaller than upper limit in Range Restriction")

    def validate(self, value, obj=None):
        if self.lower is None:
            if self.upper_inc:
                return value < self.upper
            else:
                return value <= self.upper
        elif self.upper is None:
            if self.lower_inc:
                return value >= self.lower
            else:
                return value > self.lower
        else:
            if self.lower_inc:
                T1 = value >= self.lower
            else:
                T1 = value > self.lower
            if self.upper_inc:
                T2 = value <= self.upper
            else:
                T2 = value < self.upper
            return T1 and T2

    def __repr__(self):
        if self.lower_inc:
            west_b = "["
        else:
            west_b = ")"

        if self.upper_inc:
            right_b = "]"
        else:
            right_b = ")"
        S = "Range Restriction: {}{}, {}{} ".format(west_b, str(self.lower), str(self.upper), right_b)
        return S


class RestrictContains(__ParameterRestriction__):
    """ Restrict the argument to an object with contains at least one of a set of allowed values """

    def __init__(self, allowed_values):
        self.allowed_values = allowed_values

    def validate(self, value, obj=None):
        for v in self.allowed_values:
            if v in value:
                return True
        return False

    def __repr__(self):
        return  "Contains Restriction: {}".format(str(self.allowed_values))


class RestrictValueList(__ParameterRestriction__):
    """ Restrict the argument to a list of allowed values """
    def __init__(self, allowed_values):
        self.allowed_values = allowed_values

    def validate(self, value, obj=None):
        return value in self.allowed_values

    def __repr__(self):
        return "Value List Restriction: [" + ",".join([str(T) for T in self.allowed_values]) + "]"


class RestrictList(__ParameterRestriction__):
    """ subject all individual elements of an iterable to a certain restriction """
    def __init__(self, restriction):
        self.restriction = restriction

    def validate(self, value, obj=None):
        try:
            for i in value:
                if not self.restriction.validate(i):
                    return False
            return True
        except:
            return False

    def __repr__(self):
        return "List Restriction: %s" % self.restriction


class RestrictTypeList(RestrictList):
    """ Restrict the argument to a list which contains a given type or types. Pass a type or tuple of types """
    def __init__(self, allowed_types):
        super().__init__(restriction=RestrictType(allowed_types))

    def __repr__(self):
        return "Type List Restriction:" + ",".join([T.__name__ for T in self.restriction.allowed_types])

