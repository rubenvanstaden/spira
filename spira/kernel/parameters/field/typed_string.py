
class __String__(str):

    def __new__(cls, value):
        if isinstance(value, int):
            value = str(value)
        return str.__new__(cls, value)

    def __str__(self):
        return str.__str__(self)


from spira.kernel.parameters.descriptor import DataFieldDescriptor
class StringField(DataFieldDescriptor):
    __type__ = __String__

    def __init__(self, default='', **kwargs):
        kwargs['default'] = self.__type__(default)
        super().__init__(**kwargs)

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        return value.__str__()

    def __set__(self, obj, value):
        if isinstance(value, self.__type__):
            obj.__store__[self.__name__] = value
        elif isinstance(value, (str, int)):
            obj.__store__[self.__name__] = self.__type__(value)
        else:
            raise TypeError("Invalid type in setting value " +
                            "of {} (expected {}): {}"
                            .format(self.__class_, type(value)))

