import spira.all as spira
from spira.yevon.geometry.coord import CoordField
from spira.core.transformable import Transformable
from spira.core.transforms.generic import GenericTransform


class Rotation(GenericTransform):

    def __init__(self, rotation=0, center=(0,0), **kwargs):
        super().__init__(rotation=rotation, center=center, **kwargs)

    rotation = getattr(GenericTransform, 'rotation')
    center = CoordField(default=(0,0))

    def __neg__(self):
        return Rotation(rotation=-self.rotation, center=self.center)

    def apply_to_object(self, item):
        item = item.__rotate__(rotation=self.rotation, center=self.center)
        return item


class __RotationMixin__(object):

    def _rotate(self, rotation=0, center=(0,0)):
        return self.transform(Rotation(rotation, center))

    def rotate_copy(self, rotation=0, center=(0,0)):
        return self.transform_copy(Rotation(rotation, center))


Transformable.mixin(__RotationMixin__)


 