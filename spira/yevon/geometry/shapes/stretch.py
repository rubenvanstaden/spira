import spira
from spira.core import param
from spira.core.initializer import FieldInitializer


class Stretch(FieldInitializer):

    center = param.ListField(default=[0,0])
    vector = param.ListField(default=[1,1])

    def apply(self, point):
        if isinstance(point, list):
            p = [self.vector[0] * point[0] + (1 - self.vector[0]) * self.center[0],
                 self.vector[1] * point[1] + (1 - self.vector[1]) * self.center[1]]
        else:
            raise ValueError('Stretch not implemented!')
        return p

    def apply_to_polygon(self, coords):
        polygons = []
        for point in coords:
            e = [self.vector[0] * point[0] + (1 - self.vector[0]) * self.center[0],
                 self.vector[1] * point[1] + (1 - self.vector[1]) * self.center[1]]
            polygons.append(e)
        return polygons