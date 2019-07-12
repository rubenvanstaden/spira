from spira.core.transforms.translation import Translation
from spira.core.transforms.rotation import Rotation
from spira.core.transforms.magnification import Magnification
from spira.yevon.geometry.coord import Coord
from spira.core.transforms.generic import __ConvertableTransform__


__all__ = ['IdentityTransform']


class IdentityTransform(Translation, Rotation, Magnification, __ConvertableTransform__):
    """ Transform that leaves an object unchanged. """

    def __init__(self, **kwargs):
        kwargs['rotation_center'] = (0.0, 0.0)
        kwargs['magnification_center'] = (0.0, 0.0)
        super().__init__(**kwargs)

    def apply(self, item):
        if isinstance(item, list):
            raise TypeError("Cannot add object of type " + str(type(other)) + " to transform")
            # return shape.Shape(item)
        else:
            return item

    def reverse(self, shape):
        if isinstance(item, list):
            pass
            # return shape.Shape(item)
        else:
            return item

    def apply_to_coord(self, coord):
        return coord

    def reverse_on_coord(self, coord):
        return coord

    def apply_to_coord3(self, coord):
        return coord

    def reverse_on_coord3(self, coord):
        return coord

    def apply_to_array(self, coords):
        return coords

    def reverse_on_array(self, coords):
        return coords

    def __neg__(self):
        return IdentityTransform()

    def __add__(self, other):
        if other is None:
            return IdentityTransform()
        elif isinstance(other, IdentityTransform):
            return IdentityTransform()
        elif isinstance(other, Translation):
            return Translation(other.translation)
        elif isinstance(other, Rotation):
            return Rotation(other.rotation, other.rotation_center)
        elif isinstance(other, Magnification):
            return Magnification(other.magnification, other.magnification_center)
        else:
            return __ConvertableTransform__.__add__(self, other)

    def __iadd__(self, other):
        if other is None:
            return self
        elif isinstance(other, IdentityTransform):
            return self
        else:
            return __ConvertableTransform__.__iadd__(self, other)

    def is_identity(self):
        return True


