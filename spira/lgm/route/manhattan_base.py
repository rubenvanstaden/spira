import spira
import numpy as np
from spira import param, shapes
from spira.lgm.route.manhattan import __Manhattan__
from spira.lgm.route.manhattan90 import Route90
from spira.lgm.route.manhattan180 import Route180
from spira.lgm.route.basic import RouteShape, RouteBasic, RoutePointShape


class Route(__Manhattan__):

    cell = param.CellField()

    path = param.NumpyArrayField()
    width = param.FloatField(default=1*1e8)

    # FIXME!
    player = param.PhysicalLayerField()
    angle = param.DataField(fdef_name='create_angle')
    route_shape = param.DataField(fdef_name='create_route_shape')

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

    # def validate_parameters(self):
    #     if self.port1.width < self.player.data.WIDTH:
    #         return False
    #     if self.port2.width < self.player.data.WIDTH:
    #         return False
    #     return True

    def create_angle(self):
        if self.port1 and self.port2:
            angle_diff = self.port1.orientation - self.port2.orientation
            angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)
            return angle
        return None

    def determine_type(self):
        if self.angle:
            if (self.angle == 0) or (self.angle == 180):
                if (self.p2[1] != self.p1[1]) or (self.p2[0] != self.p1[0]):
                    self.__type__ = '180'
            if (self.angle == 90) or (self.angle == 270):
                self.__type__ = '90'
            if self.angle == 180:
                if (self.p2[1] == self.p1[1]) or (self.p2[0] == self.p1[0]):
                    self.__type__ = 'straight'
            if self.path:
                self.__type__ = 'path'

    def create_route_shape(self):
        if self.__type__ == 'straight':
            route_shape = RouteShape(
                port1=self.port1,
                port2=self.port2,
                path_type='straight',
                width_type='straight'
            )
        elif self.__type__ == 'path':
            route_shape = RoutePointShape(
                path=self.path,
                width=self.width
            )
        else:
            raise ValueError('Routing type algorithm does not exist.')
        return route_shape

    def create_elementals(self, elems):

        if self.__type__ == 'straight':
            R1 = RouteBasic(route=self.route_shape, connect_layer=self.player.layer)
            r1 = spira.SRef(R1)
            r1.rotate(angle=self.port2.orientation-180, center=R1.port1.midpoint)
            r1.move(midpoint=(0,0), destination=self.port1.midpoint)

        if self.__type__ == 'path':
            R1 = RouteBasic(route=self.route_shape, connect_layer=self.player.layer)
            r1 = spira.SRef(R1)
            r1.connect(port=r1.ports['TERM1'], destination=self.port1)

        if self.__type__ == '180':
            R1 = Route180(
                port1=self.port1,
                port2=self.port2,
                radius=self.radius,
                length=self.length,
                gdslayer=self.gdslayer
            )
            R = spira.Cell(name='M180')
            for e in R1.flatten():
                R += e
            for e in R1.ports:
                R += e
            r1 = spira.SRef(R)

        if self.__type__ == '90':
            R1 = Route90(
                port1=self.port1,
                port2=self.port2,
                radius=self.radius,
                length=self.length,
                gdslayer=self.gdslayer
            )
            R = spira.Cell(name='M90')
            for e in R1.flatten():
                R += e
            for e in R1.ports:
                R += e
            r1 = spira.SRef(R)

        elems += r1

        # # for e in r1.flatten():
        # #     elems += e


        # # ----------------------------------------


        # for p in R1.ports:
        #     self.ports += p

        # # for e in R1.elementals:
        # # for e in R1.flat_copy():
        # for e in R1.flatten():
        #     elems += e

        # # self.cell = R1
        # # for e in self.merged_layers:
        # #     elems += e

        return elems



    # def create_elementals(self, elems):

    #     if (angle == 0) or (angle == 180):
    #         if (self.p2[1] != self.p1[1]) or (self.p2[0] != self.p1[0]):
    #             R1 = Route180(
    #                 port1=self.port1,
    #                 port2=self.port2,
    #                 radius=self.radius,
    #                 length=self.length,
    #                 gdslayer=self.gdslayer
    #             )

    #     if angle == 180:
    #         if (self.p2[1] == self.p1[1]) or (self.p2[0] == self.p1[0]):
    #             R1 = Route(
    #                 port1=self.port1,
    #                 port2=self.port2,
    #                 player=self.player
    #             )

    #     if (angle == 90) or (angle == 270):
    #         R1 = Route90(
    #             port1=self.port1,
    #             port2=self.port2,
    #             radius=self.radius,
    #             length=self.length,
    #             gdslayer=self.gdslayer
    #         )

    #     # if (self.p2[1] == self.p1[1]) or (self.p2[0] == self.p1[0]):
    #     #     R1 = Route(
    #     #         port1=self.port1,
    #     #         port2=self.port2,
    #     #         player=self.player
    #     #     )
    #     # else:
    #     #     if (angle == 180) or (angle == 0):
    #     #         R1 = Route180(
    #     #             port1=self.port1,
    #     #             port2=self.port2,
    #     #             radius=self.radius,
    #     #             length=self.length,
    #     #             gdslayer=self.gdslayer
    #     #         )
    #     #     else:
    #     #         R1 = Route90(
    #     #             port1=self.port1,
    #     #             port2=self.port2,
    #     #             radius=self.radius,
    #     #             length=self.length,
    #     #             gdslayer=self.gdslayer
    #     #         )

    #     for p in R1.ports:
    #         self.ports += p

    #     # for e in R1.elementals:
    #     # for e in R1.flat_copy():
    #     for e in R1.flatten():
    #         elems += e

    #     # self.cell = R1
    #     # for e in self.merged_layers:
    #     #     elems += e

    #     return elems

