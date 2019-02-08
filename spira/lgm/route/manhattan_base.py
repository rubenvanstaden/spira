import spira
import numpy as np
from spira import param, shapes
from spira.lgm.route.manhattan import __Manhattan__
from spira.lgm.route.manhattan90 import RouteManhattan90
from spira.lgm.route.manhattan180 import RouteManhattan180


class RouteManhattan(__Manhattan__):

    cell = param.CellField()

    metals = param.DataField(fdef_name='create_flatten_metals')
    merged_layers = param.DataField(fdef_name='create_merged_layers')

    def create_flatten_metals(self):
        flat_elems = self.cell.flat_copy()
        # metal_elems = flat_elems.get_polygons(layer=self.player.layer)
        return flat_elems

    def create_merged_layers(self):
        points = []
        elems = spira.ElementList()
        for p in self.metals:
            assert isinstance(p, spira.Polygons)
            for pp in p.polygons:
                points.append(pp)
        if points:
            shape = shapes.Shape(points=points)
            shape.apply_merge
            for pts in shape.points:
                elems += spira.Polygons(shape=[pts], gdslayer=self.gdslayer)
        return elems

    def create_elementals(self, elems):

        # p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]

        # if p2[1] == p1[1] or p2[0] == p1[0]:
        #     raise ValueError('Error - ports must be at different x AND y values.')

        angle_diff = self.port1.orientation - self.port2.orientation
        angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)
        # print(angle)
        if (angle == 180) or (angle == 0):
            R1 = RouteManhattan180(
                port1=self.port1,
                port2=self.port2,
                radius=self.radius,
                length=self.length,
                gdslayer=self.gdslayer
            )
        else:
            R1 = RouteManhattan90(
                port1=self.port1,
                port2=self.port2,
                radius=self.radius,
                length=self.length,
                gdslayer=self.gdslayer
            )

        for p in R1.ports:
            self.ports += p

        for e in R1.elementals:
        # for e in R1.flat_copy():
        # for e in R1.flatten():
            elems += e

        # self.cell = R1
        # for e in self.merged_layers:
        #     elems += e

        return elems

