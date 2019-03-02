import spira
import numpy as np
from spira import param, shapes
from demo.pdks import ply
from spira.lgm.route.manhattan import __Manhattan__
from spira.lgm.route.manhattan90 import Route90
from spira.lgm.route.manhattan180 import Route180
from spira.lgm.route.basic import RouteShape, RouteBasic, RoutePointShape
from spira.visualization import color
from spira.lpe.pcells import Structure


RDD = spira.get_rule_deck()


class Route(Structure, __Manhattan__):

    path = param.NumpyArrayField()
    width = param.FloatField(default=1*1e8)

    # FIXME!
    player = param.PhysicalLayerField()
    angle = param.DataField(fdef_name='create_angle')

    route_90 = param.DataField(fdef_name='create_route_90')
    route_180 = param.DataField(fdef_name='create_route_180')
    route_path = param.DataField(fdef_name='create_route_path')
    route_straight = param.DataField(fdef_name='create_route_straight')

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
        if self.cell is not None:
            self.__type__ = 'layout'
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

    def create_route_90(self):
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
        r = spira.SRef(R)
        return r

    def create_route_180(self):
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
        r = spira.SRef(R)
        return r

    def create_route_path(self):
        route_shape = RoutePointShape(
            path=self.path,
            width=self.width
        )
        R = RouteBasic(
            route=self.route_shape, 
            connect_layer=self.player.layer
        )
        r = spira.SRef(R)
        r.connect(port=r.ports['TERM1'], destination=self.port1)
        return r

    def create_route_straight(self):
        route_shape = RouteShape(
            port1=self.port1,
            port2=self.port2,
            path_type='straight',
            width_type='straight'
        )
        R = RouteBasic(
            route=route_shape, 
            connect_layer=self.player.layer
        )
        r = spira.SRef(R1)
        r.rotate(angle=self.port2.orientation-180, center=R.port1.midpoint)
        r.move(midpoint=(0,0), destination=self.port1.midpoint)
        return r

    def create_metals(self, elems):
        for e in self.cell.elementals:
            if issubclass(type(e), spira.Polygons):
                for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
                    if player.layer.number == e.gdslayer.number:
                        elems += ply.Polygon(points=e.shape.points, player=player)
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
        if self.__type__ == 'layout':
            R = RouteBasic(elementals=self.merged_layers)
            r1 = spira.SRef(R)

        elems += r1

        return elems


