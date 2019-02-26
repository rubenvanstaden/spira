import spira
import numpy as np
from spira import param, shapes
from demo.pdks.ply.base import ProcessLayer


class Polygon(ProcessLayer):

    color = param.ColorField(default='#C0C0C0')
    points = param.ElementalListField()

    # def validate_parameters(self):
    #     if self.w < self.player.data.WIDTH:
    #         return False
    #     if self.h < self.player.data.WIDTH:
    #         return False
    #     return True

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: PolygonPC(\'{}\')] {} center " + 
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.player.layer.number,
                        # self.center,
                        self.polygon.center,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

    def create_polygon(self):
        ply = spira.Polygons(shape=self.points, gdslayer=self.layer)
        # print(self.center)
        # ply.move(midpoint=ply.center, destination=(14*1e6, 0))
        return ply






