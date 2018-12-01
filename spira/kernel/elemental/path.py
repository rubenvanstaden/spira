import gdspy

import spira.kernel.parameters as param

from spira.kernel.parameters.initializer import BaseElement

from spira.kernel.elemental.polygons import Polygons


class __Path__(gdspy.Path, BaseElement):
    pass


class Path(__Path__):
    """

    """

    _ID = 0

    number_of_paths = param.IntegerField(default=1)
    distance = param.IntegerField()
    corners = param.IntegerField()
    ends = param.IntegerField()
    max_points = param.IntegerField(default=99)
    gdslayer = param.LayerField()

    def __init__(self, points, width, **kwargs):

        self.width = width
        self.points = [[c for c in p] for p in points]

        BaseElement.__init__(self, **kwargs)

        gdspy.PolyPath.__init__(self, self.points, self.width,
                                distance=self.distance,
                                corners=self.corners,
                                ends=self.ends,
                                max_points=self.max_points,
                                layer=self.gdslayer.number,
                                datatype=self.gdslayer.datatype)

        Path._ID += 1

    def __repr__(self):
        if self is None:
            return 'Path is None!'
        return ("[SPiRA: Path] ({} vertices, layer {}, datatype {})").format(self.number_of_paths, self.gdslayer.number, self.gdslayer.datatype)

    def __str__(self):
        return self.__repr__()

    @property
    def polygon(self):
        pp = Polygons(polygons=self.polygons,
                      gdslayer=self.gdslayer)
        # pp.simplify_polygons()
        pp.scale_up()
        return pp

    def add_to_gdspycell(self, cell):
        polypath = gdspy.PolyPath(self.points,
                                  self.width,
                                  number_of_paths=self.number_of_paths,
                                  distance=self.distance,
                                  layer=self.layers)
        cell.add(polypath)

    def transform(self, transform):
        return self

    def flat_copy(self, level=-1):
        return self

    def flatten(self):
        return [self]
