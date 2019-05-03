import numpy as np
from spira.yevon.properties.base import __Properties__


class __GeometryProperties__(__Properties__):

    @property
    def xmax(self):
        return self.bbox[1][0]

    @property
    def ymax(self):
        return self.bbox[1][1]

    @property
    def xmin(self):
        return self.bbox[0][0]

    @property
    def ymin(self):
        return self.bbox[0][1]

    @property
    def dx(self):
        return (self.xmax - self.xmin)

    @property
    def dy(self):
        return (self.ymax - self.ymin)

    @property
    def pbox(self):
        (a,b), (c,d) = self.bbox
        points = [[[a,b], [c,b], [c,d], [a,d]]]
        return points

    @property
    def center(self):
        return np.sum(self.bbox, 0)/2

    @center.setter
    def center(self, destination):
        self.move(midpoint=self.center, destination=destination)

    @property
    def xpos(self):
        return self.center[0]

    @property
    def ypos(self):
        return self.center[1]
