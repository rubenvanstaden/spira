

__all__ = ['ParameterProcessor', 'ProcessorTypeCast']


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
            raise ProcessorException("Cannot add %s to PropertyProcessor" % type(other))

    def __iadd__(self, other):
        if isinstance(other, __CompoundPropertyProcessor__):
            self.__sub_processors += other.__sub_processors
            return self
        elif isinstance(other, PropertyProcessor):
            self.__sub_processors += [other]
            return self
        else:
            raise ProcessorException("Cannot add %s to PropertyProcessor" % type(other))

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
