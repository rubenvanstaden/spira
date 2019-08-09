import numpy as np
from numpy.linalg import norm

from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.core.parameters.processors import ProcessorTypeCast


class Transform(ParameterInitializer):
    """ Abstract base class for generic transform. """

    _ID = 0

    def __call__(self, item):
        """ Apply the transform on the object, after having made a copy. """
        if item is None:
            return self
        if isinstance(item, Transform):
            return item + self
        else:
            return self.apply_to_copy(item)

    def __add__(self, other):
        if other is None:
            return CompoundTransform([self])
        return CompoundTransform([self, other])

    def __sub__(self, other):
        if other is None:
            return CompoundTransform([self])
        if isinstance(other, ReversibleTransform):
            return CompoundTransform([self, -other])
        else:
            raise TypeError("Cannot subtract an irreversible transform")

    def apply(self, item):
        """ Apply the transform directly on the
        object, without making a copy. """
        if isinstance(item, list):
            from spira.yevon.geometry.shapes import Shape
            return Shape(item).transform(self)
        else: 
            return item.transform(self)

    def apply_to_copy(self, item):
        if isinstance(item, list):
            from spira.yevon.geometry.shapes import Shape
            return Shape(item).transform_copy(self)
        else:
            return item.transform_copy(self)

    def is_identity(self):
        return True


class ReversibleTransform(Transform):
    """ Base class for a transformation that can be reversed. """

    def __add__(self, other):
        if other is None:
            return ReversibleCompoundTransform([self])
        if isinstance(other, ReversibleTransform):
            return ReversibleCompoundTransform([self, other])
        else:
            return CompoundTransform([self, other])

    def __sub__(self, other):
        if other is None:
            return ReversibleCompoundTransform([self])
        if isinstance(other, ReversibleTransform):
            return ReversibleCompoundTransform([self, -other])
        else:
            raise TypeError("Cannot subtract an irreversible transform")

    def __neg__(self):
        pass
        # T = ReversibleCompoundTransform()
        # T.reverse(self)

    def reverse(self, item):
        if isinstance(item, list):
            from spira.yevon.geometry.shapes import Shape
            return Shape(item).reverse_transform(self)
        else:
            return item.reverse_transform(self)


class CompoundTransform(Transform):
    """ A store for the concatenation of transforms. """

    def __init__(self, transforms=[], **kwargs):
        if isinstance(transforms, list):
            self.__subtransforms__ = transforms
        elif isinstance(transforms, CompoundTransform):
            self.__subtransforms__ = []
            self.__subtransforms__.extend(transforms)
        else:
            self.__subtransforms__ = [transforms]
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.__subtransforms__)

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        return self.__subtransforms__[key]

    def __add__(self, other):
        T = CompoundTransform(self)
        T.add(other)
        return T

    def __iadd__(self, other):
        self.add(other)
        return self

    def apply(self, item):
        """ Apply the transform to the transformable item. """
        if isinstance(item, list):
            from spira.yevon.geometry.shapes import Shape
            shape = Shape(item)
            for c in self.__subtransforms__:
                shape = c.apply(shape)
            return shape
        else:
            for c in self.__subtransforms__:
                item = c.apply(item)

    # FIXME: This is required for transforming polygon ports.
    # This is currently just a temporary fix.
    def apply_to_angle(self, angle):
        return angle

    def add(self, other):
        if other is None:
            return
        if isinstance(other, CompoundTransform):
            for c in other.__subtransforms__:
                self.add(other)
        elif isinstance(other, Transform):
            self.__subtransforms__.append(other)
        else:
            raise TypeError("Cannot add object of type " + str(type(other)) + " to transform")

    def apply_to_coord(self, coord):
        for c in self.__subtransforms__:
            coord = c.apply_to_coord(coord)
        return coord

    def apply_to_array(self, coords):
        for c in self.__subtransforms__:
            coords = c.apply_to_array(coords)
        return coords

    def is_identity(self):
        for c in self.__subtransforms__:
            if not c.is_identity(): 
                return False
        return True

    def id_string(self):
        return self.__repr__()


class ReversibleCompoundTransform(CompoundTransform, ReversibleTransform):
    """ A store for the concatenation of reversible transformas. """

    def __make_irreversible__(self):
        self.__class__ = CompoundTransform

    def __add__(self, other):
        T = ReversibleCompoundTransform(self)
        if other != None: 
            T.add(other)
        return T

    def __iadd__(self, other):
        self.add(other)
        return self

    def __sub__(self, other):
        T = ReversibleCompoundTransform(self)
        T.add(-other)
        return T

    def __isub__(self, other):
        self.add(-other)
        return self

    def __neg__(self):
        T = ReversibleCompoundTransform()
        for c in reversed(self):
            T.add(-c)
        return T

    def add(self, other):
        if isinstance(other, CompoundTransform):
            for c in other.__subtransforms__:
                self.add(other)
        if isinstance(other, ReversibleTransform):
            self.__subtransforms__.append(other)
        elif isinstance(other, Transform):
            self.__make_irreversible__()
            self.__subtransforms__.append(other)
        else:
            raise TypeError("Cannot add object of type " + str(type(other)) + " to transform")

    def reverse(self, item):
        if isinstance(item, list):
            from spira.yevon.geometry.shapes import Shape
            shape = Shape(item)
            for c in reversed(self.__subtransforms__):
                shape = c.reverse(shape)
            return shape
        else:
            for c in reversed(self.__subtransforms__):
                item = c.reverse(item)

    def reverse_on_coord(self, coord):
        for c in reversed(self.__subtransforms__):
            coord = c.reverse_on_coord(coord)
        return coord

    def reverse_on_array(self, coords):
        for c in reversed(self.__subtransforms__):
            coords = c.reverse_on_array(coords)
        return coords


class ProcessoTransformation(ProcessorTypeCast):
    def __init__(self):
        ProcessorTypeCast.__init__(self, Transform)
        # ProcessorTypeCast.__init__(self, ReversibleTransform)
        # super().__init__(ReversibleTransform)

    def process(self, value, obj=None):
        from spira.core.transforms.identity import IdentityTransform
        if value is None:
            return IdentityTransform()
        else:
            return ProcessorTypeCast.process(self, value=value, obj=obj)


def TransformationParameter(restriction=None, preprocess=None, **kwargs):
    from spira.core.transformation import Transform
    if 'default' in kwargs:
        default = kwargs['default']
    else:
        default = None
    R = RestrictType(Transform) & restriction
    P = ProcessoTransformation() + preprocess
    return ParameterDescriptor(default=default, restrictions=R, preprocess=P, **kwargs)

