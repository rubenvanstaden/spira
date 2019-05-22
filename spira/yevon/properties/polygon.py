import gdspy
import numpy as np
from spira.yevon.properties.geometry import __GeometryProperties__


class PolygonProperties(__GeometryProperties__):

    @property
    def points(self):
        return self.shape.points

    @property
    def ply_area(self):
        ply = gdspy.PolygonSet(self.shape.points, verbose=False)
        return ply.area()

    @property
    def bbox(self):
        # self.polygons = np.array([self.points])
        # return self.get_bounding_box()
        return self.bbox_info().bounding_box


