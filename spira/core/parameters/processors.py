

__all__ = [
    'ParameterProcessor',
    'ProcessorTypeCast',
    'ProcessorInt',
    'ProcessorFloat',
    'ProcessorString',
    'ProcessorIntRound',
    'ProcessorRange'
]


class ParameterProcessor(object):
    """ Processes a value before it is passed as a property. """

    def __init__(self):
        pass

    def __add__(self, other):
        if isinstance(other, ParameterProcessor):
            return __CompoundPropertyProcessor__([self, other])
        elif other is None:
            return self
        else:
            raise ValueError("Cannot add %s to PropertyProcessor " % type(other))

    def __iadd__(self, other):
        C = self.__add__(other)
        self = C
        return self

    def __call__(self, value, obj=None):
        return self.process(value, obj)

    def process(self, value, obj=None):
        return value

    def __repr__(self):
        return "<Property Processor >"


class __CompoundPropertyProcessor__(ParameterProcessor):
    """ Compound parameter processor class """

    def __init__(self, processors=[]):
        self.__sub_processors = processors

    def __add__(self, other):
        if isinstance(other, __CompoundPropertyProcessor__):
            return __CompoundPropertyProcessor__(self.__sub_processors + other.__sub_processors)
        elif isinstance(other, PropertyProcessor):
            return __CompoundPropertyProcessor__(self.__sub_processors + [other])
        else:
            raise ValueError("Cannot add %s to PropertyProcessor" % type(other))

    def __iadd__(self, other):
        if isinstance(other, __CompoundPropertyProcessor__):
            self.__sub_processors += other.__sub_processors
            return self
        elif isinstance(other, PropertyProcessor):
            self.__sub_processors += [other]
            return self
        else:
            raise ValueError("Cannot add %s to PropertyProcessor" % type(other))

    def process(self, value, obj=None):
        v = value
        for R in self.__sub_processors:
            v = R.process(self, value, obj)
        return v

    def __repr__(self):
        S = "< Compound Property Processor:"
        for i in self.__sub_processors:
            S += "   %s" % i.__repr__()
        S += ">"
        return S


class ProcessorTypeCast(ParameterProcessor):
    """ Restrict the type or types the argument can have, and tries a typecast where possible. """

    def __init__(self, cast_type):
        if not isinstance(cast_type, type):
            raise ValueError("cast_type argument %s in TypeCast Processor should be of type 'type'" % cast_type)
        self.cast_type = cast_type

    def process(self, value, obj=None):
        if isinstance(value, self.cast_type):
            return value
        else:
            return self.cast_type(value)

    def __repr__(self):
        S = "<Type Cast Processor: %s >" % self.cast_type.__name__


def ProcessorInt():
    return ProcessorTypeCast(int)


def ProcessorFloat():
    return ProcessorTypeCast(float)


def ProcessorString():
    return ProcessorTypeCast(str)


class ProcessorIntRound(ParameterProcessor):
    """ rounds a number to the nearest integer"""

    def process(self, value, obj=None):
        return int(round(value))

    def __repr__(self):
        S = "<Int Round Processor >"


class ProcessorRange(ParameterProcessor):
    """ Brings a number to within a certain range. """

    def __init__(self, lower=None, upper=None):

        if lower is None and upper is None:
            raise ValueError("Range Processor should have an upper or lower limit")

        if (not upper is None) and (not lower is None):
            if lower > upper:
                raise ValueError("lower limit should be smaller than upper limit in Range Processor")

        self.lower = lower
        self.upper = upper

    def process(self, value, obj=None):
        if not self.lower is None:
            if value < self.lower:
                return self.lower
        if not self.upper is None:
            if value > self.upper:
                return self.upper
        return value

    def __repr__(self):
        S = "<Range Processor: [%s, %s] >" % (str(self.lower), str(upper))


