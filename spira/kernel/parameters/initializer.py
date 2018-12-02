import inspect
import collections
import numpy as np
from copy import copy, deepcopy
from spira.kernel.utils import scale_coord_up as scu


class GeometryMixin(object):

    @property
    def bbox(self):
        import spira
        if isinstance(self, spira.Cell):
            c_copy = deepcopy(self)
            # c_copy.to_gdspy
            c_copy = c_copy.commit_to_gdspy()
            # c_copy = c_copy.construct_gdspy_tree(gdspy_commit=False)
            box = c_copy.get_bounding_box()
            [a,b], [c,d] = scu(box)
            points = [[[a,b], [c,b], [c,d], [a,d]]]
            ply = spira.Polygons(polygons=points)
            return ply
        return None

    @property
    def box(self):
        import spira
        if isinstance(self, spira.Cell):
            self.to_gdspy
        box = self.get_bounding_box()
        return box

    @property
    def center(self):
        # print(np.sum(self.bbox.center, 0)/2)
        # return np.sum(self.bbox.center, 0)/2
        return self.bbox.center

    @center.setter
    def center(self, destination):
        self.move(destination=destination, origin=self.center)

    @property
    def x(self):
        return np.sum(self.bbox, 0)[0]/2

    @x.setter
    def x(self, destination):
        destination = (destination, self.center[1])
        self.move(destination = destination, origin=self.center, axis='x')

    @property
    def y(self):
        return np.sum(self.bbox,0)[1]/2

    @y.setter
    def y(self, destination):
        destination = ( self.center[0], destination)
        self.move(destination=destination, origin=self.center, axis='y')

    @property
    def xmax(self):
        return self.bbox[1][0]

    @xmax.setter
    def xmax(self, destination):
        self.move(destination=(destination, 0), origin=self.bbox[1], axis='x')

    @property
    def ymax(self):
        return self.bbox[1][1]

    @ymax.setter
    def ymax(self, destination):
        self.move(destination=(0, destination), origin=self.box[1], axis='y')
        # self.move(destination=(0, destination), origin=self.bbox[1], axis='y')

    @property
    def xmin(self):
        return self.bbox[0][0]

    @xmin.setter
    def xmin(self, destination):
        self.move(destination=(destination, 0), origin=self.box[0], axis='x')
        # self.move(destination=(destination, 0), origin=self.bbox[0], axis='x')

    @property
    def ymin(self):
        return self.bbox[0][1]

    @ymin.setter
    def ymin(self, destination):
        self.move(destination=(0, destination), origin=self.box[0], axis='y')
        # self.move(destination=(0, destination), origin=self.bbox[0], axis='y')

    @property
    def size(self):
        bbox = self.bbox
        return bbox[1] - bbox[0]

    @property
    def xsize(self):
        bbox = self.bbox
        return bbox[1][0] - bbox[0][0]

    @property
    def ysize(self):
        bbox = self.bbox
        return bbox[1][1] - bbox[0][1]

    @property
    def topcenter(self):
        bb = self.bbox
        x = bb[0][0] + self.xsize/2
        y = bb[0][1] + self.ysize
        return [x, y]

    @property
    def botcenter(self):
        bb = self.bbox
        x = bb[0][0] + self.xsize/2
        y = bb[1][1] - self.ysize
        return [x, y]

    @property
    def topleft(self):
        bb = self.bbox
        return [bb[0][0], bb[1][1]]

    @property
    def botleft(self):
        bb = self.bbox
        return [bb[0][0], bb[0][1]]

    def movex(self, origin = 0, destination = None):
        if destination is None:
            destination = origin
            origin = 0
        self.move(origin=(origin,0), destination=(destination,0))
        return self

    def movey(self, origin=0, destination=None):
        if destination is None:
            destination = origin
            origin = 0
        self.move(origin=(0,origin), destination=(0,destination))
        return sel


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


from spira.kernel.parameters.descriptor import BaseField
from spira.kernel.parameters.descriptor import DataField
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
            # kwargs[p] = getattr(self, p)
            kwargs[p] = deepcopy(getattr(self, p))
        kwargs.update(override_kwargs)
        return self.__class__(**kwargs)


class FieldInitializer(GeometryMixin, __Field__):
    """
    Set the keyword arguments of the class and
    bind geometric property operations to the
    object for API usage.
    """

    def __init__(self, **kwargs):
        if not hasattr(self, '__store__'):
            self.__store__ = dict()
        self.__store_fields__(kwargs)

    def __store_fields__(self, kwargs):
        props = self.__fields__()
        for key, value in kwargs.items():
            if key not in props:
                raise ValueError("Keyword argument \'{}\' " + 
                                 "does not match any properties " + 
                                 "of {}.".format(key, type(self)))
            setattr(self, key, value)


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

        if 'library' in kwargs:
            pass

        if kwargs['name'] is None:
            kwargs['name'] = '{}-{}'.format(cls.__name__, cls._ID)

        # if kwargs['name'] is None:
        #     kwargs['name'] = cls.__name__
        # else:
        #     n = kwargs['name']
        #     cls.__name__ = n[0].upper() + n[1:]
        #     kwargs['name'] = '{}-{}'.format(cls.__name__, cls._ID)

        cls = super().__call__(**kwargs)

        return cls


class BaseLibrary(FieldInitializer, metaclass=MetaBase):
    pass


class BaseCell(FieldInitializer, metaclass=MetaCell):
    pass


class BaseLayer(FieldInitializer, metaclass=MetaElemental):
    pass


from spira.kernel import parameters as param
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
