import spira
import numpy as np
from copy import deepcopy
from numpy.linalg import norm
# from spira.core.initializer import MetaInitializer
# from spira.core.initializer import FieldInitializer
# from spira.core import param
from spira.core.transformation import TransformationField
from spira.core.mixin import MixinBowl


class __Transformable__(MixinBowl):

    def transform(self, transformation):
        return self

    def transform_copy(self, transformation):
        T = deepcopy(self)
        T.transform(transformation)
        return T

    def reverse_transform(self, transformation):
        return self.transform(-transformation)

    def reverse_transform_copy(self, transformation):
        T = deepcopy(self)
        T.reverse_transform(transformation)
        return T

    def __reflect__(self, points, p1=(0,0), p2=(1,0)):
        points = np.array(points); p1 = np.array(p1); p2 = np.array(p2)
        if np.asarray(points).ndim == 1:
            t = np.dot((p2-p1), (points-p1))/norm(p2-p1)**2
            pts = 2*(p1 + (p2-p1)*t) - points
        if np.asarray(points).ndim == 2:
            t = np.dot((p2-p1), (p2-p1))/norm(p2-p1)**2
            pts = np.array([2*(p1 + (p2-p1)*t) - p for p in points])
        return pts

    def __rotate__(self, points, angle=45, center=(0,0)):
        angle = angle*np.pi/180
        ca = np.cos(angle)
        sa = np.sin(angle)
        sa = np.array((-sa, sa))
        c0 = np.array(center)
        if np.asarray(points).ndim == 2:
            pts = (points - c0) * ca + (points - c0)[:,::-1] * sa + c0
            pts = np.round(pts, 6)
        if np.asarray(points).ndim == 1:
            pts = (points - c0) * ca + (points - c0)[::-1] * sa + c0
            pts = np.round(pts, 6)
        return pts

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """ Moves elements of the Device from the midpoint point 
        to the destination. Both midpoint and destination can be 
        1x2 array-like, Port, or a key corresponding to one of 
        the Ports in this device """
        pass

        # # from spira.yevon.geometry.ports.port import __Port__

        # if destination is None:
        #     destination = midpoint
        #     midpoint = [0,0]

        # if issubclass(type(midpoint), __Port__):
        #     o = midpoint.midpoint
        # elif np.array(midpoint).size == 2:
        #     o = midpoint
        # elif midpoint in self.ports:
        #     o = self.ports[midpoint].midpoint
        # else:
        #     raise ValueError("[PHIDL] [DeviceReference.move()] ``midpoint`` " +
        #                      "not array-like, a port, or port name")

        # if issubclass(type(destination), __Port__):
        #     d = destination.midpoint
        # elif np.array(destination).size == 2:
        #     d = destination
        # elif destination in self.ports:
        #     d = self.ports[destination].midpoint
        # else:
        #     raise ValueError("[PHIDL] [DeviceReference.move()] ``destination`` " +
        #                      "not array-like, a port, or port name")

        # if axis == 'x':
        #     d = (d[0], o[1])
        # if axis == 'y':
        #     d = (o[0], d[1])

        # return d, o


class Transformable(__Transformable__):
    """ Object that can be transformed. """

    from spira.core.transformation import Transform

    __type__ = Transform

    # transformation = param.TransformationField(allow_none=True, default=None)
    transformation = TransformationField(allow_none=True, default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def __init__(self, transformation=None, **kwargs):
    #     if (not 'transformation' in kwargs) or (transformation != None):
    #         kwargs['transformation'] = transformation
    #     super().__init__(self, **kwargs)

    def transform(self, transformation=None):
        if isinstance(transformation, self.__type__):
            self.transformation = self.transformation + transformation
        elif transformation is None:
            return
        else:
            raise TypeError("Wrong type " + str(type(transformation)) + " for transformation in Transformable")
        return self

    def expand_transform(self):
        """ Tries to propagate the transformation as deep 
        as possible in the hierarchy. """
        return self




