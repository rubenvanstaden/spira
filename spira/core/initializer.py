import inspect
import collections
import numpy as np
from copy import copy, deepcopy
from spira.core.mixin.geometry import GeometryMixin


class MetaBase(type):
    """
    Base Metaclass to register and bind class to
    property functions. All elements connect to
    this metaclass.
    """

    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, attrs):
        mixins = []

        link_mixins = attrs.get('__mixins__')
        if link_mixins:
            mixins.extend(link_mixins)

        bases = list(bases)
        bases.extend(mixins)
        bases = tuple(bases)

        cls = super().__new__(cls, name, bases, dict(attrs))

        if not hasattr(cls, 'registry'):
            cls.registry = {}
        cls.registry[name] = cls

        return cls

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        cls.__props__ = []
        cls.__params__ = {}

        locked_fields = []
        unlocked_fields = []

        for k, v in cls.__get_fields__():
            if not k in cls.__props__:

                if hasattr(v, 'bind_property'):
                    v.bind_property(cls, k)
                v.validate_binding(cls, k)

                if v.locked:
                    locked_fields.append(k)
                else:
                    unlocked_fields.append(k)

                cls.__params__[k] = v
                cls.__props__.append(k)

        cls.__locked_fields__ = locked_fields
        cls.__unlocked_fields__ = unlocked_fields

        cls.format_doc()

    def format_doc(cls):
        pass


from spira.core.descriptor import BaseField
from spira.core.descriptor import DataField
class __Field__(metaclass=MetaBase):
    """ This if the FieldConstructor """

    def __init__(self, **kwargs):
        if not hasattr(self, '__store__'):
            self.__store__ = dict()

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def __get_fields__(cls):
        prop = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, BaseField):
                prop.append([attr_name, attr])
        return prop

    @classmethod
    def __unlocked_field_params__(cls):
        return cls.__unlocked_fields__

    @classmethod
    def __locked_fields_params__(cls):
        return cls.__locked_fields__

    @classmethod
    def __fields__(cls):
        return cls.__props__

    def __external_fields__(self):
        ex_fields = []
        for i in self.__unlocked_field_params__():
            field = getattr(self.__class__, i)
            if isinstance(field, DataField):
                if field.__field_was_stored__(self):
                    ex_fields.append(i)
            else:
                ex_fields.append(i)
        return ex_fields

    def __copy__(self):
        kwargs = {}
        for p in self.__external_fields__():
            kwargs[p] = getattr(self, p)
        return self.__class__(**kwargs)

    def __deepcopy__(self, memo):
        from copy import deepcopy
        kwargs = {}
        for p in self.__external_fields__():
            kwargs[p] = deepcopy(getattr(self, p), memo)
        return self.__class__(**kwargs)

    def modified_copy(self, **override_kwargs):
        """
        Returns a copy, but where the user can
        override properties using.
        """
        kwargs = {}
        for p in self.__external_fields__():
            kwargs[p] = getattr(self, p)
        kwargs.update(override_kwargs)
        return self.__class__(**kwargs)


# class FieldInitializer(GeometryMixin, __Field__):
class FieldInitializer(__Field__):
    """
    Set the keyword arguments of the class and
    bind geometric property operations to the
    object for API usage.
    """

    def __init__(self, **kwargs):
        if not hasattr(self, '__store__'):
            self.__store__ = dict()
        self.__store_fields__(kwargs)
        self.__validation_check__()

    def __store_fields__(self, kwargs):
        props = self.__fields__()
        for key, value in kwargs.items():
            if key not in props:
                raise ValueError("Keyword argument \'{}\' " +
                                 "does not match any properties " +
                                 "of {}.".format(key, type(self)))
            setattr(self, key, value)

    def __validation_check__(self):
        if not self.validate_parameters():
            raise AttributeError('Width is not large enough.')

    def validate_parameters(self):
        return True


class MetaElemental(MetaBase):

    def __call__(cls, *params, **keyword_params):
        # p, a, k, d = inspect.getfullargspec(cls.__init__)

        full_args = inspect.getfullargspec(cls.__init__)
        p = full_args.args
        a = full_args.varargs
        k = full_args.varkw
        d = full_args.defaults

        if d is None: d = []
        kwargs = {}
        for k, v in zip(p[-len(d):], d):
            kwargs[k] = v
        kwargs.update(keyword_params)
        for k, v in zip(p[1:len(params)+1], params):
            kwargs[k] = v

        cls = super().__call__(**kwargs)
        return cls


class MetaSref(MetaBase):

    def __call__(cls, *params, **keyword_params):
        # p, a, k, d = inspect.getfullargspec(cls.__init__)

        full_args = inspect.getfullargspec(cls.__init__)
        p = full_args.args
        a = full_args.varargs
        k = full_args.varkw
        d = full_args.defaults

        if d is None: d = []
        kwargs = {}
        for k, v in zip(p[-len(d):], d):
            kwargs[k] = v
        kwargs.update(keyword_params)
        for k, v in zip(p[1:len(params)+1], params):
            kwargs[k] = v

        cls = super().__call__(**kwargs)
        return cls


class MetaCell(MetaBase):
    """
    Called when an instance of a SPiRA class is
    created. Pareses all kwargs and passes it to
    the FieldInitializer for storing.

    class Via(spira.Cell):
        layer = param.LayerField()

    # Gets called here and passes
    # kwargs['layer': 50] to FieldInitializer.
    >>> via = Via(layer=50)
    """

    def __call__(cls, *params, **keyword_params):
        # p, a, k, d = inspect.getfullargspec(cls.__init__)

        full_args = inspect.getfullargspec(cls.__init__)
        p = full_args.args
        a = full_args.varargs
        k = full_args.varkw
        d = full_args.defaults

        if d is None: d = []
        kwargs = {}
        for k, v in zip(p[-len(d):], d):
            kwargs[k] = v
        kwargs.update(keyword_params)
        for k, v in zip(p[1:len(params)+1], params):
            kwargs[k] = v

        # ----------------------------- Library -------------------------------
        from spira.gdsii import library
        from spira import settings
        lib = None
        if 'library' in kwargs:
            lib = kwargs['library']
            del(kwargs['library'])
        if lib is None:
            lib = settings.get_library()

        if kwargs['name'] is None:
            kwargs['name'] = '{}-{}'.format(cls.__name__, cls._ID)
            cls._ID += 1

        name = kwargs['name']

        cls = super().__call__(**kwargs)

        retrieved_cell = lib.get_cell(cell_name=name)
        if retrieved_cell is None:
            lib += cls
            return cls
        else:
            del cls
            return retrieved_cell


class BaseLibrary(FieldInitializer, metaclass=MetaBase):
    pass


class BaseCell(FieldInitializer, metaclass=MetaCell):
    pass


class BaseLayer(FieldInitializer, metaclass=MetaElemental):
    pass


# from spira import param
class BaseElement(FieldInitializer, metaclass=MetaElemental):

    # gdspy_commit = param.BoolField()

    def flatten(self):
        return [self]

    def commit_to_gdspy(self, cell, gdspy_commit=None):
        return None

    def dependencies(self):
        return None

    @property
    def id(self):
        return self.__id__

    @id.setter
    def id(self, _id):
        self.__id__ = _id





