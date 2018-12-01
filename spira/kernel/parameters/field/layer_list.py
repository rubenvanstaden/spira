from spira.kernel.parameters.field.typed_list import TypedList


class LayerList(TypedList):

    def __init__(self, items=list()):
        super().__init__(items)

    def __repr__(self):
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        if isinstance(key, int):
            for i in self._list:
                if i.layer == key: return i
            raise IndexError('layer ' + str(key) + ' cannot be found in LayerList.')
        elif isinstance(key, str):
            for i in self._list:
                if i.name == key: return i
            raise IndexError('layer ' + str(key) + ' cannot be found in LayerList.')
        elif isinstance(key, tuple):
            for i in self._list:
                if self.__key() == key: return i
            raise IndexError('layer ' + str(key) + ' cannot be found in LayerList.')
        else:
            raise TypeError('Index is wrong type ' + str(type(key)) + ' in LayerList')


from spira.kernel.parameters.descriptor import DataFieldDescriptor
class LayerListProperty(DataFieldDescriptor):
    __type__ = LayerList

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f(self.__type__())
        if value is None:
            value = self.__type__()
        obj.__store__[self.__name__] = value
        return value
