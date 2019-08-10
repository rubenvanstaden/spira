import gdspy
import inspect
import collections
import numpy as np
from copy import copy, deepcopy

from spira.core.mixin import MetaMixinBowl, MixinBowl
from spira.core.parameters.descriptor import __Parameter__
from spira.core.parameters.descriptor import Parameter
from spira.core.parameters.descriptor import EXTERNAL_VALUE, CACHED_VALUE


__all__ = ['ParameterInitializer']


SUPPRESSED = (None,)
REGISTERED_CLASSES = set()


def is_suppressed(propvalue):
    if isinstance(propvalue, tuple):
        return SUPPRESSED == propvalue
    else:
        return False


class MetaBase(MetaMixinBowl):
    """ ProcessLayer Metaclass to register and bind class to property
    functions. All elements connect to this metaclass. """

    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return collections.OrderedDict()

    def __init__(cls, name, bases, attrs):
        cls.bind_parameters()
        super().__init__(name, bases, attrs)
        REGISTERED_CLASSES.add(cls)

    def bind_parameters(cls):
        cls.__params__ = {}
        cls.__props__ = ['__name_prefix__']

        locked_parameters = []
        unlocked_parameters = []

        for k, v in cls.__get_parameters__():
            if not k in cls.__props__:

                if hasattr(v, 'bind_parameter'):
                    v.bind_parameter(cls, k)
                v.validate_binding(cls, k)

                if v.locked:
                    locked_parameters.append(k)
                else:
                    unlocked_parameters.append(k)

                cls.__params__[k] = v
                cls.__props__.append(k)

        cls.__locked_parameters__ = locked_parameters
        cls.__unlocked_parameters__ = unlocked_parameters
        cls.__generate_docs__()

    def mixin(cls, mixin_class):
        super().mixin(mixin_class)
        cls.bind_parameters()
        for c in REGISTERED_CLASSES:
            if issubclass(c, cls):
                c.bind_parameters()


class MetaInitializer(MetaBase):
    """
    Metaclass that initiates spira classes for
    meta-configuring classes and parameters.
    """

    MODULES = ['gdspy', 'meshio', 'pygmsh']
    SECTIONS = ['Desc', 'Parameters', 'Examples', 'Notes', 'Returns']

    def __map_parameters__(cls, *params, **keyword_params):
        f = inspect.getfullargspec(cls.__init__)
        p, d = f.args, f.defaults
        if d is None: d = []
        kwargs = {}
        for k, v in zip(p[-len(d):], d):
            kwargs[k] = v
        kwargs.update(keyword_params)
        for k, v in zip(p[1:len(params)+1], params):
            kwargs[k] = v
        return kwargs

    def __generate_docs__(cls):

        output = []
        output.extend(cls.__get_class_docs__())
        output.extend(cls.__get_function_docs__())

        cls.__doc__ = '\n'.join(output)

    def __get_class_docs__(cls):

        output = list()

        class_docs = {}
        if cls.__doc__:
            lines = inspect.getdoc(cls).split('\n')

            lines = list(filter(lambda x: len(x.strip()) > 0, lines))

            section = 'Desc'
            class_docs[section] = []

            for i in range(len(lines)):
                if '---' in lines[i]:
                    del class_docs[section][-1]
                    section = lines[i-1].strip()
                    class_docs[section] = []
                line = lines[i].strip()
                class_docs[section].append(line)

        class_docs['Parameters'] = []

        docparam = ''
        for key in cls.SECTIONS:
            if key in class_docs.keys():
                value = class_docs[key]
                if key == 'Desc':
                    docparam += '\n'.join(value)
                elif key == 'Parameters':
                    params = cls.__parameters__()
                    if len(params) > 0:
                        docparam += '\nParameters\n'
                        docparam += '---------\n'
                        for p in params:
                            docparam += p + ' : ' + str(type(p)) + '\n'
                            if hasattr(cls, p):
                                param_attr = getattr(cls, p)
                                if hasattr(param_attr, '__doc__'):
                                    docparam += '\t' + param_attr.__doc__ + '\n'
                else:
                    docparam += '{}\n{}\n'.format(key, '\n'.join(value))
                docparam += '\n'

        from sphinxcontrib.napoleon import Config
        config = Config(napoleon_use_param=True, napoleon_use_rtype=True)
        from sphinxcontrib.napoleon.docstring import NumpyDocstring
        lines = NumpyDocstring(docparam, config).lines()

        output.extend(lines)

        return output

    def __get_function_docs__(cls):

        prefix = '.. function:: '

        output = list()

        def _functions(module, cdef_name):
            functions = list()
            for f in inspect.getmembers(cdef_name[1], inspect.isfunction):
                functions.append(f)
            return functions

        def _ignore_module(module, fdef_name):
            remove = False
            for c in inspect.getmembers(module, inspect.isclass):
                functions = _functions(module, c)
                for f in functions:
                    if f[0] == fdef_name:
                        remove = True
            return remove

        cls_dir = dir(cls)
        for a in dir(MetaInitializer):
            if a in cls_dir:
                cls_dir.remove(a)
        for a in cls_dir:
            for module in cls.MODULES:
                if _ignore_module(module, a):
                    cls_dir.remove(a)

        for attr_name in cls_dir:
            if attr_name.find('__') < 0:
                attr = getattr(cls, attr_name)
                if inspect.isfunction(attr):
                    sig = inspect.signature(attr)

                    if len(dict(sig.parameters)) > 1:
                        fargs = prefix + attr_name + str(sig)
                        output.append(fargs)

                    if inspect.getdoc(attr) is not None:
                        output.append('\n' + inspect.getdoc(attr))
                    output.append('\n')
        return output


# class __ParameterInitializer__(MixinBowl, metaclass=MetaInitializer):
class __ParameterInitializer__(metaclass=MetaInitializer):
    """ This is the ParameterConstructor """

    def __init__(self, **kwargs):
        self.flag_busy_initializing = True

        if not hasattr(self, '__store__'):
            self.__store__ = dict()

        for key, value in kwargs.items():
            if not is_suppressed(value):
                setattr(self, key, value)

        self.flag_busy_initializing = False

    @classmethod
    def __unlocked_parameter_params__(cls):
        return cls.__unlocked_parameters__

    @classmethod
    def __locked_parameters_params__(cls):
        return cls.__locked_parameters__

    @classmethod
    def __parameters__(cls):
        return cls.__props__

    @classmethod
    def __get_parameters__(cls):
        prop = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, __Parameter__):
                prop.append([attr_name, attr])
        return prop

    def __clear_cached_values_in_store__(self):
        if not self.flag_busy_initializing:
            store_content_flattened = self.__store__.items()
            for (key, item) in list(store_content_flattened):
                origin = item[1]
                if origin == CACHED_VALUE:
                    del self.__store__[key]
            if hasattr(self, '__SPIRA_CACHE__'):
                self.__SPIRA_CACHE__.clear()

    def __external_parameters__(self):
        ex_parameters = []
        for i in self.__unlocked_parameter_params__():
            parameter = getattr(self.__class__, i)
            if isinstance(parameter, Parameter):
                if parameter.__parameter_was_stored__(self):
                    if parameter.__get_parameter_status__(self) == EXTERNAL_VALUE:
                        ex_parameters.append(i)
            else:
                ex_parameters.append(i)
        return ex_parameters

    def _copy__(self):
        kwargs = {}
        for p in self.__external_parameters__():
            kwargs[p] = getattr(self, p)
        return self.__class__(**kwargs)

    def __deepcopy__(self, memo):
        from copy import deepcopy
        kwargs = {}
        for p in self.__external_parameters__():
            kwargs[p] = deepcopy(getattr(self, p), memo)
        return self.__class__(**kwargs)

    def copy(self, **override_kwargs):
        """ Returns a copy, but where the user can
        override properties using. """
        kwargs = {}
        for p in self.__external_parameters__():
            kwargs[p] = getattr(self, p)
            # kwargs[p] = deepcopy(getattr(self, p))
            # kwargs[p] = copy(getattr(self, p))
        kwargs.update(override_kwargs)
        return self.__class__(**kwargs)


class ParameterInitializer(__ParameterInitializer__):
    """ Set the keyword arguments of the class and
    bind geometric property operations to the
    object for API usage. """

    __id__ = ''

    def __init__(self, **kwargs):

        self.flag_busy_initializing = True

        if not hasattr(self, '__store__'):
            self.__store__ = dict()
        self.__store_parameters__(kwargs)
        self.__validation_check__()
        self.__determine_type__()

        self.flag_busy_initializing = False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        class_string = '[SPiRA: {}]'.format(self.__class__.__name__)
        if hasattr(self, '__keywords__'):
            _repr = list()
            for k, v in self.__keywords__.items():
                if ('__' not in k) and (v is not None):
                    _repr.append('{} {}'.format(k, v))
            c = ', '.join(_repr)
            class_string = '{} ({})'.format(class_string, c)
        return class_string

    def __store_parameters__(self, kwargs):
        props = self.__parameters__()
        for key, value in kwargs.items():
            if key == 'doc':
                self.__doc__ = value
            else:
                if key not in props:
                    v = "Keyword argument \'{}\' does not match any parameters of type {}."
                    raise ValueError(v.format(key, type(self)))
                if not is_suppressed(value):
                    setattr(self, key, value)

    def __validation_check__(self):
        if not self.validate_parameters():
            raise AttributeError('Invalid parameter!')

    def __determine_type__(self):
        self.determine_type()

    def determine_type(self):
        self.__type__ = None

    def validate_parameters(self):
        return True

    def set(self, **override_kwargs):
        """
        Used to update the value of a parameter inline.

        Example
        -------
        >>> ports += port.set(width=2.0)
        """
        for key, value in override_kwargs.items():
            if key not in self.__parameters__():
                v = "Keyword argument \'{}\' does not match any parameters of type {}."
                raise ValueError(v.format(key, type(self)))
            setattr(self, key, value)
        return self


