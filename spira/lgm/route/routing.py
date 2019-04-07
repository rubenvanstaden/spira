import spira
import numpy as np
from spira.core import param
from spira import shapes
from spira import pc
from spira.lgm.route.manhattan import __Manhattan__
from spira.lgm.route.manhattan90 import Route90
from spira.lgm.route.manhattan180 import Route180
from spira.lgm.route.route_shaper import RouteSimple, RouteGeneral, RoutePointShape
from spira.visualization import color
from spira.lpe.structure import Structure


RDD = spira.get_rule_deck()


class Route(Structure, __Manhattan__):

    path = param.NumpyArrayField()
    width = param.NumberField(default=1*1e8)
    port_list = param.ListField(allow_none=True)

    # FIXME!
    angle = param.DataField(fdef_name='create_angle', allow_none=True)

    route_90 = param.DataField(fdef_name='create_route_90')
    route_180 = param.DataField(fdef_name='create_route_180')
    route_path = param.DataField(fdef_name='create_route_path')
    route_straight = param.DataField(fdef_name='create_route_straight')
    route_auto = param.DataField(fdef_name='create_route_auto')
    
    route_transformation = param.TransformationField(allow_none=True, default=None)

    def create_angle(self):
        if self.port1 and self.port2:
            angle_diff = self.port1.orientation - self.port2.orientation
            angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)
            return angle
        return None

    def determine_type(self):
        if self.cell is not None:
            self.__type__ = 'layout'
        if self.angle is not None:
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

        # print(self.angle)
        # print(self.port_list)
        # if self.port_list is not None:
        if len(self.port_list) > 0:
            self.__type__ = 'auto'

    def create_route_90(self):
        R1 = Route90(
            port1=self.port1,
            port2=self.port2,
            radius=self.radius,
            length=self.length,
            ps_layer=self.ps_layer,
            gds_layer=self.gds_layer
        )
        R = spira.Cell(
            name='M90',
            elementals=R1.elementals,
            ports=R1.ports
        )
        r = spira.SRef(R)
        return r

    def create_route_180(self):
        R1 = Route180(
            port1=self.port1,
            port2=self.port2,
            radius=self.radius,
            length=self.length,
            ps_layer=self.ps_layer,
            gds_layer=self.gds_layer
        )
        R = spira.Cell(
            name='M180',
            elementals=R1.elementals,
            ports=R1.ports
        )
        r = spira.SRef(R)
        return r

    def create_route_path(self):
        route_shape = RoutePointShape(
            path=self.path,
            width=self.width
        )
        route_shape.apply_merge
        R = RouteGeneral(
            route_shape=route_shape, 
            connect_layer=self.ps_layer
        )
        r = spira.SRef(R)
        # r.connect(port=r.ports['P1'], destination=self.port1)
        return r

    def create_route_straight(self):
        route_shape = RouteSimple(
            port1=self.port1,
            port2=self.port2,
            # path_type='sine',
            # width_type='sine'
            path_type='straight',
            width_type='straight'
        )
        route_shape.apply_merge
        R = RouteGeneral(
            route_shape=route_shape,
            connect_layer=self.ps_layer
        )
        r = spira.SRef(R)
        if self.route_transformation is not None:
            r.transform(transform=self.route_transformation.apply())
        r.connect(port=r.ports['P1'], destination=self.port1)
        return r

    # def create_route_auto(self):
    #     R = spira.Cell(name='Auto Router')
    #     for x in range(0, len(self.port_list), 2):
    #         route_cell = Route(
    #             port1=self.port_list[x],
    #             port2=self.port_list[x+1],
    #             ps_layer=self.ps_layer,
    #             radius=0.1*1e6
    #         )
    #         R += spira.SRef(route_cell)
    #     D = spira.Cell(name='Device Router')
    #     points = []
    #     for e in R.flatten():
    #         if isinstance(e, spira.Polygons):
    #             for p in e.points:
    #                 points.append(p)
    #     route_shape = shapes.Shape(points=points)
    #     route_shape.apply_merge
    #     D += pc.Polygon(points=route_shape.points, ps_layer=self.ps_layer, enable_edges=False) 
    #     return spira.SRef(D)

    def create_route_auto(self):
        R = spira.Cell(name='Auto Router')

        term_list = []
        for x in range(0, len(self.port_list)):
            p = self.port_list[x]
            if isinstance(p, spira.Term):
                term_list.append(p)
            elif isinstance(p, spira.Connector):
                for c in p.ports:
                    term_list.append(c)

        for x in range(0, len(term_list), 2):
            route_cell = Route(
                port1=term_list[x],
                port2=term_list[x+1],
                ps_layer=self.ps_layer, 
                radius=0.1*1e6)
            R += spira.SRef(route_cell)
        D = spira.Cell(name='Device Router')
        points = []
        for e in R.flatten():
            if isinstance(e, spira.Polygons):
                for p in e.points:
                    points.append(p)
        route_shape = shapes.Shape(points=points)
        route_shape.apply_merge
        D += pc.Polygon(points=route_shape.points, ps_layer=self.ps_layer, enable_edges=False) 
        return spira.SRef(D)

    def create_metals(self, elems):
        if self.cell is not None:
            for e in self.cell.elementals:
                if issubclass(type(e), spira.Polygons):
                    for ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
                        if ps_layer.layer.number == e.gds_layer.number:
                            elems += pc.Polygon(points=e.shape.points, ps_layer=ps_layer)
        elif self.__type__ == '90':
            r1 = self.route_90
            for e in r1.polygons:
                elems += e
        elif self.__type__ == '180':
            r1 = self.route_180
            for e in r1.polygons:
                elems += e
        elif self.__type__ == 'path':
            r1 = self.route_path
            for e in r1.polygons:
                elems += e
        elif self.__type__ == 'straight':
            r1 = self.route_straight
            for e in r1.polygons:
                elems += e
        elif self.__type__ == 'auto':
            r1 = self.route_auto
            for e in r1.polygons:
                elems += e
        return elems

    def create_elementals(self, elems):

        if self.__type__ == '90':
            r1 = self.route_90
        if self.__type__ == '180':
            r1 = self.route_180
        if self.__type__ == 'path':
            r1 = self.route_path
        if self.__type__ == 'straight':
            r1 = self.route_straight
        if self.__type__ == 'auto':
            r1 = self.route_auto
        if self.__type__ == 'layout':
            R = RouteGeneral(elementals=self.merged_layers, ports=[])
            r1 = spira.SRef(R)

        elems += r1

        return elems


