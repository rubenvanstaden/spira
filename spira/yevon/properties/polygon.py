import gdspy
import numpy as np
from spira.yevon.properties.clipper import __ClipperAspects__
from spira.yevon.properties.geometry import __GeometryAspects__


class PolygonAspects(__GeometryAspects__):

    @property
    def points(self):
        return self.shape.points

    @property
    def ply_area(self):
        ply = gdspy.Polygon(self.shape.points, verbose=False)
        return ply.area()

    @property
    def bbox(self):
        return self.bbox_info.bounding_box


class PolygonClipperAspects(__ClipperAspects__):

    def __add__(self, other):
        polygons = []
        assert isinstance(other, Polygon)
        if self.layer == other.layer:
            for points in self.shape.points:
                polygons.append(np.array(points))
            for points in other.polygons:
                polygons.append(np.array(points))
            self.shape.points = polygons
        else:
            raise ValueError("To add masks the polygon layers \
                              must be the same.")
        return self

    def __sub__(self, other):
        points = clipping.boolean(
            subj=self.shape.points,
            clip=other.shape.points,
            method='not'
        )
        return points

    def __and__(self, other):
        pp = clipping.boolean(
            subj=[other.shape.points],
            clip=[self.shape.points],
            method='and'
        )
        if len(pp) > 0:
            return Polygon(shape=np.array(pp), layer=self.layer)
        else:
            return None

    def __or__(self, other):
        pp = clipping.boolean(
            subj=other.shape.points,
            clip=self.shape.points,
            method='or'
        )
        if len(pp) > 0:
            return Polygon(shape=pp, layer=self.layer)
        else:
            return None

    def union(self, other):
        return self.__or__(self, other)

    def intersection(self, other):
        return self.__and__(self, other)

    def difference(self, other):
        return self.__sub__(self, other)

