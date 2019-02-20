import spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy

from spira import param
from spira.core.initializer import ElementalInitializer
from spira.core.mixin.transform import TranformationMixin
from spira.gdsii.group import GroupElementals


class __Port__(ElementalInitializer):

    __mixins__ = [TranformationMixin]

    __committed__ = {}

    def __add__(self, other):
        if other is None:
            return self
        p1 = np.array(self.midpoint) + np.array(other)
        return p1


class PortAbstract(__Port__):

    name = param.StringField()
    parent = param.DataField()
    midpoint = param.MidPointField()
    orientation = param.IntegerField(default=0)
    reflection = param.BoolField(default=False)
    gdslayer = param.LayerField(name='PortLayer', number=64)
    color = param.StringField(default='#000000')

    __mixins__ = [GroupElementals]

    def encloses(self, polygon):
        return pyclipper.PointInPolygon(self.midpoint, polygon) != 0

    def flat_copy(self, level=-1):
        c_port = self.modified_copy(
            midpoint=self.midpoint,
            orientation=self.orientation
        )
        return c_port

    def commit_to_gdspy(self, cell):
        if self.__repr__() not in list(__Port__.__committed__.keys()):

            # from spira import shapes
            # rect_shape = shapes.RectangleShape(
            #     p1=[0, 0],
            #     p2=[self.length, self.width]
            # )

            # ply_edge = spira.Polygons(
            #     shape=rect_shape,
            #     gdslayer=self.edgelayer,
            #     direction=90
            # )

            # if self.reflection:
            #     ply_edge.reflect()
            #     # ply_edge.rotate(angle=180)
            # ply_edge.rotate(angle=self.orientation)
            # ply_edge.move(midpoint=ply_edge.center, destination=self.midpoint)

            # ply_edge.commit_to_gdspy(cell=cell)

            # for e in self.elementals:
            #     # if isinstance(e, spira.Polygons) and (e.direction == 0):
            #     #     e.rotate(angle=self.orientation)
            #     # else:
            #     #     e.rotate(angle=self.orientation)

            #     # e.rotate(angle=self.orientation)
            #     # if self.reflection:
            #     #     e.reflect()
            #     #     # e.rotate(angle=self.orientation+90)
            #     e.move(midpoint=e.center, destination=self.midpoint)
            #     e.commit_to_gdspy(cell=cell)

            __Port__.__committed__.update({self.__repr__(): self})
        else:
            p = __Port__.__committed__[self.__repr__()]

            # for e in p.elementals:
            #     # if isinstance(e, spira.Polygons) and (e.direction == 0):
            #     #     e.rotate(angle=self.orientation)
            #     # else:
            #     #     e.rotate(angle=self.orientation)

            #     # e.rotate(angle=self.orientation)
            #     # if self.reflection:
            #     #     e.reflect()
            #     #     # e.rotate(angle=self.orientation+90)
            #     e.move(midpoint=e.center, destination=self.midpoint)
            #     e.commit_to_gdspy(cell=cell)

    # @property
    # def label(self):
    #     for e in self.elementals:
    #         if isinstance(e, spira.Label):
    #             return e
    #     return None

    @property
    def label(self):
        lbl = spira.Label(
            position=self.midpoint,
            text=self.name,
            gdslayer=self.gdslayer,
            texttype=64,
            color='#808080'
        )
        return lbl

    def reflect(self):
        """ Reflect around the x-axis. """
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = -self.orientation
        # self.orientation = np.mod(self.orientation, 360)
        self.reflection = True

        for e in self.elementals:
            e.reflect()
            e.rotate(angle=180)
            e.move(midpoint=e.position, destination=self.midpoint)

            # if isinstance(e, spira.Label):
            #     e.reflect()
            #     e.rotate(angle=180)
            #     # e.rotate(angle=self.orientation)
            #     e.move(midpoint=e.position, destination=self.midpoint)
            # else:
            #     e.reflect()
            #     e.rotate(angle=180)
            #     # e.rotate(angle=self.orientation)
            #     e.move(midpoint=e.center, destination=self.midpoint)

        return self

    def rotate(self, angle=45, center=(0,0)):
        """ Rotate port around the center with angle. """

        self.midpoint = self.__rotate__(self.midpoint, angle=angle, center=center)
        self.orientation += angle
        self.orientation = np.mod(self.orientation, 360)

        for e in self.elementals:
            if isinstance(e, spira.Polygons) and (e.direction == 0):
                e.rotate(angle=angle-90)
            else:
                e.rotate(angle=angle)

            # e.rotate(angle=self.orientation)
            # e.rotate(angle=angle)
            # if isinstance(e, spira.Label):
            #     e.move(midpoint=e.position, destination=self.midpoint)
            # elif isinstance(e, spira.Polygons) and (e.direction == 0):
            #     e.move(midpoint=e.center, destination=self.midpoint)
            # else:
            #     e.move(midpoint=e.center, destination=self.midpoint)

        return self

    def translate(self, dx, dy):
        """ Translate port by dx and dy. """
        self.midpoint = self.midpoint + np.array([dx, dy])
        for e in self.elementals:
            if isinstance(e, spira.Label):
                e.move(midpoint=e.position, destination=self.midpoint)
            else:
                e.move(midpoint=e.center, destination=self.midpoint)
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = super().move(midpoint=midpoint, destination=destination, axis=axis)
        dx, dy = np.array(d) - o
        self.translate(dx, dy)
        return self

    def connect(self, S, P):
        """ Connects the port to a specific polygon in a cell reference. """
        self.node_id = '{}_{}'.format(S.ref.name, P.id)

    @property
    def normal(self):
        dx = np.cos((self.orientation)*np.pi/180)
        dy = np.sin((self.orientation)*np.pi/180)
        return np.array([self.midpoint, self.midpoint + np.array([dx,dy])])


class Port(PortAbstract):
    """ Ports are objects that connect different polygons
    or references in a layout. Ports represent veritical
    connection such as vias or junctions.

    Examples
    --------
    >>> port = spira.Port()
    """

    radius = param.FloatField(default=0.25*1e6)

    # surface = param.DataField(fdef_name='create_surface_polygon')

    def __init__(self, port=None, elementals=None, polygon=None, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

        if elementals is not None:
            self.elementals = elementals

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, number {}, midpoint {}, " +
            "radius {}, orientation {})").format(self.name,
            self.gdslayer.number, self.midpoint,
            self.radius, self.orientation
        )

    # def create_surface_polygon(self):
    @property
    def surface(self):
        from spira import shapes
        shape = shapes.CircleShape(
            center=self.midpoint,
            box_size=[self.radius, self.radius]
        )
        ply = spira.Polygons(shape=shape, gdslayer=self.gdslayer)
        ply.move(midpoint=ply.center, destination=self.midpoint)
        return ply

    # def create_elementals(self, elems):
    #     elems += self.create_surface_polygon()
    #     # elems += spira.Label(
    #     #     position=self.midpoint,
    #     #     text=self.name,
    #     #     gdslayer=self.gdslayer,
    #     #     texttype=64,
    #     #     color='#808080'
    #     # )
    #     return elems

    def _copy(self):
        new_port = Port(
            parent=self.parent,
            name=self.name,
            midpoint=deepcopy(self.midpoint),
            # elementals=deepcopy(self.elementals),
            gdslayer=deepcopy(self.gdslayer),
            orientation=self.orientation,
            color=self.color
        )
        return new_port


if __name__ == '__main__':

    p = Port()
    print(p)












