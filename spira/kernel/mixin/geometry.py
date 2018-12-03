import spira
import numpy as np
from copy import copy, deepcopy
from spira.kernel.utils import scale_coord_up as scu


class GeometryMixin(object):

    @property
    def bbox(self):
        import spira
        if isinstance(self, spira.Cell):
            c_copy = deepcopy(self)
            c_copy = c_copy.commit_to_gdspy()
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

    @property
    def xmin(self):
        return self.bbox[0][0]

    @xmin.setter
    def xmin(self, destination):
        self.move(destination=(destination, 0), origin=self.box[0], axis='x')

    @property
    def ymin(self):
        return self.bbox[0][1]

    @ymin.setter
    def ymin(self, destination):
        self.move(destination=(0, destination), origin=self.box[0], axis='y')

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
        return self

