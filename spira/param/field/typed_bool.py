


from spira.core.descriptor import DataFieldDescriptor
class BoolField(DataFieldDescriptor):

    def __init__(self, default=False, **kwargs):
        kwargs['default'] = bool(default)
        super().__init__(**kwargs)

    def __set__(self, obj, value): 
        if isinstance(value, bool):
            obj.__store__[self.__name__] = value
        else:
            raise TypeError("Invalid type in setting value " + 
                            "of {} (expected {}): {}"
                            .format(self.__class_, type(value)))

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        return value

    def __repr__(self):
        value = obj.__store__[self.__name__]
        return ("[SPiRA: Bool] (value {})").format(value)

    def __str__(self):
        return self.__repr__()





