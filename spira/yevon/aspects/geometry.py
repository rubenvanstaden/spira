import numpy as np
from spira.yevon.aspects.base import __Aspects__


class __GeometryAspects__(__Aspects__):

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
    def xpos(self):
        return self.center[0]

    @property
    def ypos(self):
        return self.center[1]

    @property
    def center(self):
        return self.bbox_info.center

    @center.setter
    def center(self, destination):
        self.move(midpoint=self.center, destination=destination)

