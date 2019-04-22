import numpy as np
from spira.core.transformation import ReversibleTransform

from spira.yevon import utils
from spira.core.param.variables import *
from spira.yevon.geometry.coord import CoordField, Coord


class GenericTransform(ReversibleTransform):

    translation = CoordField()
    rotation = NumberField(default=0)
    reflection = BoolField(default=False)
    magnification = NumberField(default=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        """ Gives a string representing the transform. """
        return "_M=%s-R=%s-RF=%s-MN=%s" % (
            str(self.translation),
            str(self.rotation),
            str(self.reflection),
            str(self.magnification)
        )

    def __add__(self, other):
        if issubclass(type(other), GenericTransform):
            T = GenericTransform()

            # T.rotation = self.rotation + other.rotation
            # T.translation = self.translation + other.translation

            # if other.reflection is True:
            #     p1, p2 = (0,1*1e6), (0,0)

            #     p1 = np.array(p1)
            #     p2 = np.array(p2)
            #     T.translation = np.array([T.translation[0], T.translation[1]])
        
            #     # Translate so reflection axis passes through midpoint
            #     T.translation = T.translation - p1
        
            #     # Rotate so reflection axis aligns with x-axis
            #     angle = np.arctan2((p2[1]-p1[1]), (p2[0]-p1[0]))*180 / np.pi
            #     print(angle)
            #     T.translation = utils.rotate_algorithm(T.translation, angle=-angle, center=[0,0])
            #     print(T.rotation)
            #     T.rotation -= angle
            #     print(T.rotation)
        
            #     # Reflect across x-axis
            #     T.reflection = not other.reflection
            #     T.translation = [T.translation[0], -T.translation[1]]
            #     T.rotation = -T.rotation
        
            #     # Un-rotate and un-translate
            #     T.translation = utils.rotate_algorithm(T.translation, angle=angle, center=[0,0])
            #     T.rotation += angle
            #     T.translation = T.translation + p1

            # T.translation = Coord(T.translation)

            T.reflection = (not self.reflection and other.reflection)
            # T.rotation = Rf * (self.rotation + other.rotation)
            T.rotation = self.rotation + other.rotation
            T.translation = Coord(self.translation) + other.translation
        else:
            raise ValueError('Not implemented!')
        return T

    def __iadd__(self, other):
        self.__add__(other)
        return self

    def __sub__(self, other):
        return self.__add__(-other)

    def __isub__(self, other):
        return self.__iadd__(-other)

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __neg__(self):
        pass

    def apply_to_object(self, item):
        if self.reflection is True:
            item = item.__reflect__()
        # item = item.__rotate__(angle=self.rotation, center=self.center)
        item = item.__rotate__(angle=self.rotation)
        item = item.__translate__(dx=self.translation[0], dy=self.translation[1])
        return item

    def id_string(self):
        """ Gives a hash of the transform (for naming purposes) """
        return self.__str__()

