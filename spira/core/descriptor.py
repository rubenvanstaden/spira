

class BaseField(object):
    """
    Sets the values of the Field when initialized.
    Binds a Field object with a class parameter.

    class Via(spira.Cell):
        layer = param.LayerField()

    >>> via = Via()
    >>> via.layer
    <spira.gdsii.DataFieldDescriptor>
    >>> via.layer.default
    [SPiRA: Layer] (name '', number 0, datatype 0)
    """

    __keywords__ = ['default', 'fdef_name', 'locked', 'doc']

    def __init__(self, **kwargs):
        self.__doc__ = 'No documenation generated'
        if 'doc' in kwargs:
            self.__doc__ = kwargs['doc']
            kwargs.pop('doc')
        for k, v in kwargs.items():
            if k in self.__keywords__:
                object.__setattr__(self, k, v)

    def bind_property(self, cls, name):
        pass

    def validate_binding(self, host_cls, name):
        return True


class DataFieldDescriptor(BaseField):
    __keywords__ = ['default', 'fdef_name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.locked = False

        if 'constraint' in kwargs:
            self.constraint = kwargs['constraint']
        else:
            self.constraint = None

        if 'fdef_name' not in kwargs:
            self.fdef_name = None

    def __field_was_stored__(self, obj):
        return self.__name__ in obj.__store__

    def __get__(self, obj, type=None):
        """
        Called when retieving a value from an instance.
        Following from `via` in __set__, the following
        can be executed:

        Information:
        >>> via.layer
        50
        """
        if obj is None:
            return self
        if not self.__field_was_stored__(obj):
            f = self.get_param_function(obj)
            if f is None:
                if hasattr(self, 'default'):
                    value = self.default
                else:
                    value = self
            else:
                value = self.call_param_function(obj)
        else:
            value = self.get_stored_value(obj)
        return value

    def __set__(self, obj, value):
        """
        Store the value of the object keyword argument
        in the __store__ variable of the instance. This
        setter is calle from the FieldInitializer class.
        This is called when creating a class instance:

        self -> The Field being set.
        obj -> Class to which value are set.

        -------------------------------------------------
        class Via(spira.Cell):
            layer = param.LayerField()

        via = Via(layer=50)
        -------------------------------------------------

        Information:
        >>> via.__store__['__param_layer__']
        50
        >>> obj.__class__.__name__
        Via
        """
        obj.__store__[self.__name__] = value

    def bind_property(self, cls, name):
        self.name = name
        if not hasattr(self, '__name__'):
            self.__name__ = '__param_{}__'.format(name)

    def validate_binding(self, host_cls, name):
        if self.fdef_name is None:
            self.auto_fdef_name = 'create_' + name

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        return value

    def get_param_function(self, obj):
        if self.fdef_name is None:
            if hasattr(obj, self.auto_fdef_name):
                return getattr(obj, self.auto_fdef_name)
            else:
                return None
        else:
            return getattr(obj, self.fdef_name)

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f()
        obj.__store__[self.__name__] = value
        return value


class FunctionField(BaseField):
    """ Property which calls a get and set method to set the variables.
    the get and set method are specified by name, so it supports override, 
    but is slower than FunctionProperty. If set method is not specified, 
    then the property is considered locked and cannot be set. 
    
    Examples
    --------
    """

    def __init__(self, fget, fset=None, **kwargs):
        self.fget = fget
        if fset is None:
            self.locked = True
        else:
            self.fset = fset
            self.locked = False
        BaseField.__init__(self, **kwargs)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return self.fget(obj)

    def __set__(self, obj, value):
        if not self.locked:
            return self.fset(obj, value)
        else:
            raise ValueError('Cannot assign property')


class DataField(DataFieldDescriptor):
    pass




