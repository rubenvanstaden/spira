import numpy as np
from spira.core.parameters.restrictions import RestrictNothing
from spira.core.parameters.processors import ParameterProcessor


__all__ = ['ParameterDescriptor', 'FunctionParameter', 'Parameter']


EXTERNAL_VALUE = 0
CACHED_VALUE = 1


class __Parameter__(object):
    """
    Sets the values of the Parameter when initialized.
    Binds a Parameter object with a class parameter.

    class Via(spira.Cell):
        layer = param.LayerParameter()

    >>> via = Via()
    >>> via.layer
    <spira.yevon.gdsii.ParameterDescriptor>
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

    def bind_parameter(self, cls, name):
        pass

    def validate_binding(self, host_cls, name):
        return True


class ParameterDescriptor(__Parameter__):
    __keywords__ = ['default', 'fdef_name', 'restriction', 'locked', 'preprocess']

    def __init__(self, local_name=None, **kwargs):

        self.__name__ = local_name
        self.name = local_name

        super().__init__(**kwargs)

        self.locked = False

        if 'preprocess' in kwargs:
            self.preprocess = kwargs['preprocess']
        else:
            self.preprocess = ParameterProcessor()

        if 'allow_none' in kwargs:
            self.allow_none = kwargs['allow_none']
        else:
            self.allow_none = False

        if 'restriction' in kwargs:
            self.restriction = kwargs['restriction']
        else:
            self.restriction = RestrictNothing()

        if 'fdef_name' not in kwargs:
            self.fdef_name = None

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
        if not self.__parameter_was_stored__(obj):
            f = self.get_param_function(obj)
            if f is None:
                if hasattr(self, 'default'):
                    value = self.preprocess(self.default, obj)
                else:
                    value = None
            else:
                value = self.call_param_function(obj)
        else:
            value = self.__get_parameter_value__(obj)
        if not self.restriction(value, obj):
            if value is None:
                if not self.allow_none:
                    raise ValueError("Cannot set parameter {} of {} to None.".format(self.name, obj.__class__.__name__))
            else:
                raise ValueError("Invalid parameter assignment '{}' of cell '{}' with value '{}', which is not compatible with '{}'.".format(self.name, obj.__class__.__name__, str(value), str(self.restriction)))
        return value

    def __set__(self, obj, value):
        """
        Store the value of the object keyword argument
        in the __store__ variable of the instance. This
        setter is calle from the ParameterInitializer class.
        This is called when creating a class instance:

        self -> The Parameter being set.
        obj -> Class to which value are set.

        -------------------------------------------------
        class Via(spira.Cell):
            layer = param.LayerParameter()

        via = Via(layer=50)
        -------------------------------------------------

        Information:
        >>> via.__store__['__param_layer__']
        50
        >>> obj.__class__.__name__
        Via
        """
        if self.locked:
            raise ValueError("Cannot assign to locked parameter '{}' of '{}'".format(self.name, type(obj).__name__))
        if self.preprocess is not None:
            v = self.preprocess(value, obj)
        else:
            v = value
        self.__check_restriction__(obj, v)
        self.__externally_set_parameter_value__(obj, v)

    def __externally_set_parameter_value__(self, obj, value):
        clear_cached_values_in_store = True
        if self.__parameter_was_stored__(obj):
            old_value = obj.__store__[self.__name__][0]
            try:
                clear_cached_values_in_store = (type(old_value) != type(value)) or (old_value != value)
                if type(clear_cached_values_in_store) == np.ndarray:
                    clear_cached_values_in_store = clear_cached_values_in_store.all()
            except ValueError as e:
                clear_cached_values_in_store = True
        obj.__store__[self.__name__] = (value, EXTERNAL_VALUE)
        if not obj.flag_busy_initializing:
            obj.__validation_check__()
            if clear_cached_values_in_store:
                obj.__clear_cached_values_in_store__()

    def __cache_parameter_value__(self, obj, value):
        if obj is not None:
            new_value = self.preprocess(value, obj)
            self.__check_restriction__(obj, new_value)
            obj.__store__[self.__name__] = (new_value, CACHED_VALUE)
            return new_value
        else:
            return value

    def __parameter_was_stored__(self, obj):
        return (self.__name__ in obj.__store__)

    def __get_parameter_value__(self, obj):
        return obj.__store__[self.__name__][0]

    def __get_parameter_status__(self, obj):
        return obj.__store__[self.__name__][1]

    def __check_restriction__(self, obj, value):
        if (self.allow_none is True) and (value is None):
            return True
        elif self.restriction(value, obj):
            return True
        else:
            raise ValueError("Invalid parameter assignment '{}' of cell '{}' with value '{}', which is not compatible with '{}'.".format(self.name, obj.__class__.__name__, str(value), str(self.restriction)))

    def bind_parameter(self, cls, name):
        self.name = name
        if (self.__name__ is None) or (not hasattr(self, '__name__')):
            self.__name__ = '__param_{}__'.format(name)

    def validate_binding(self, host_cls, name):
        if self.fdef_name is None:
            self.auto_fdef_name = 'create_' + name

    def get_param_function(self, obj):
        if self.fdef_name is None:
            if hasattr(self, 'auto_fdef_name') and hasattr(obj, self.auto_fdef_name):
                return getattr(obj, self.auto_fdef_name)
            else:
                return None
        else:
            return getattr(obj, self.fdef_name)

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f()
        new_value = self.__cache_parameter_value__(obj, value)
        return value


class FunctionParameter(__Parameter__):
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
        __Parameter__.__init__(self, **kwargs)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return self.fget(obj)

    def __set__(self, obj, value):
        if not self.locked:
            return self.fset(obj, value)
        else:
            raise ValueError('Cannot assign parameter.')


class SetFunctionParameter(__Parameter__):
    """
    Parameter which calls a set method to set the variables,
    but it is stored in a known attribute, so a get method
    need not be specified. A restriction can be specified.
    """

    def __init__(self, local_name, fset, **kwargs):
        self.fset = fset
        self.__name__ = local_name
        self.name = local_name
        self.locked = False
        self.allow_none = False

        if 'preprocess' in kwargs:
            self.preprocess = kwargs['preprocess']
        else:
            self.preprocess = ParameterProcessor()

        if 'restriction' in kwargs:
            self.restriction = kwargs['restriction']
        else:
            self.restriction = RestrictNothing()

        super().__init__(**kwargs)

    def __get_default__(self):
        import inspect
        if inspect.isroutine(self.default):
            return self.default()
        else:
            return self.default

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if (self.__name__ in obj.__dict__):
            return obj.__dict__[self.__name__]
        else:
            if hasattr(self, 'default'):
                d = self.__get_default__()
                if self.preprocess is None:
                    return d
                else:
                    return self.preprocess(d, obj)
            elif self.allow_none:
                return None
            else:
                raise ValueError("Attribute '%s' of '%s' is not set, and no default value is specified" (self.name, obj))

    def __set__(self, obj, value):
        new_value = self.preprocess(value, obj)
        if self.restriction(new_value, obj):
            return self.fset(obj, self.preprocess(value, obj))
        else:
            raise ValueError("%s does not match restriction %s in property %s" % (value, self.restriction, self.__name__))

    def bind_parameter(self, cls, name):
        self.name = name
        if (self.__name__ is None) or (not hasattr(self, '__name__')):
            self.__name__ = '__prop_{}__'.format(name)


import sys

def is_call_internal(obj, level=1):
    """ checks if a call to a function is done from within the object
        or from outside """
    f = sys._getframe(1 + level).f_locals
    if not "self" in f:
        return False
    return (f["self"] is obj)


class ConvertParameter(__Parameter__):

    def __init__(self, parent_class, parent_property_name, convert_method):
        self.convert_method = convert_method
        self.parent_class = parent_class
        self.parent_property_name = parent_property_name
        self.locked = True
        __Parameter__.__init__(self)

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return self.parent_property.__get__(obj, type)

    def __set__(self, obj, value):
        if not is_call_internal(obj):
            self.convert_method(obj)
        value = self.parent_property.__set__(obj, value)
        return value

    def bind_parameter(self, cls, name):
        import inspect
        self.name = name
        if self.parent_property_name is None:
            self.parent_property_name = name
        # if self.parent_class is None:
        #     mro = inspect.getmro(cls)
        #     found = False
        #     for C in mro[1:]:
        #         if name in C.__store__:
        #             if isinstance(C.__store__[name][0], DefinitionProperty):
        #                 continue
        #             self.parent_class = C
        #             found = True
        #             break
        #     if not found:
        #         raise IpcorePropertyDescriptorException("DefinitionProperty '%s' of '%s' should have a matching property in a parent class." % (name, cls))
        self.parent_property = object.__getattribute__(self.parent_class, self.parent_property_name)


class Parameter(ParameterDescriptor):
    pass


class RestrictedParameter(ParameterDescriptor):
    pass

