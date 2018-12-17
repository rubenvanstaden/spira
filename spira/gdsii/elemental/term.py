import spira
import numpy as np

from spira import param
from copy import copy, deepcopy
from spira.gdsii.elemental.port import __Port__
from spira.core.initializer import BaseElement


class Shape(BaseElement):
    points = param.PointArrayField(fdef_name='create_points')

    def create_points(self, points):
        return points


class Arrow(Shape):

    midpoint = param.PointField()
    rotation = param.FloatField()

    wh = param.FloatField(default=0.2)
    wb = param.FloatField(default=0.1)
    hh = param.FloatField(default=0.6)
    hb = param.FloatField(default=1)

    arrow_head = param.PointField()

    endpoints = param.DataField(fdef_name='create_endpoints')

    def create_endpoints(self):
        return (self.arrow_head, [self.wb/2, 0])

    def create_points(self, points):

        # pts = [ [[0,0], [0.1,0], [0.1,1], [0.2,1], [0.05,1.7], [-0.1,1], [0,1]] ]
        self.arrow_head = [self.wb/2, self.hb+self.hh]
        pts = [[0,0], [self.wb,0], [self.wb,self.hb], [self.wh,self.hb], self.arrow_head, [-self.wb,self.hb], [0,self.hb]]
        # ply = spira.Polygons(polygons=[pts], gdslayer=spira.Layer(number=88))

        # ply.rotate(angle=self.rotation, center=self.midpoint)
        # ply.move(origin=self.arrow.center, destination=self.midpoint)

        # elems += ply

        points += [pts]

        return points


class Term(__Port__):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.
    """

    width = param.FloatField(default=2)
    length = param.FloatField(default=0.1)

    def __init__(self, port=None, polygon=None, **kwargs):
        from spira import shapes

        __Port__.__init__(self, port=port, polygon=polygon, **kwargs)

        rect_shape = shapes.RectangleShape(p1=[0, 0],
                                          p2=[self.width, self.length],
                                          gdslayer=spira.Layer(number=65))
        pp = shapes.Rectangle(shape=rect_shape)

        pp.rotate(angle=90-self.orientation, center=self.midpoint)
        pp.move(origin=pp.center, destination=self.midpoint)

        arrow = Arrow(midpoint=self.midpoint, rotation=self.orientation)

        self.arrow = spira.Polygons(polygons=arrow.points, gdslayer=spira.Layer(number=88))

        self.arrow.move(origin=arrow.endpoints[1], destination=self.midpoint)
        self.arrow.rotate(angle=90-self.orientation, center=self.midpoint)

        self.label = spira.Label(position=self.midpoint,
                                 text=self.name,
                                 gdslayer=self.gdslayer,
                                 texttype=self.text_layer.number)

        if polygon is None:
            self.polygon = pp
        else:
            self.polygon = polygon

    def __repr__(self):
        return ("[SPiRA: Term] (name {}, number {}, midpoint {}, " +
                "width {}, orientation {})").format(self.name, self.gdslayer.number, self.midpoint,
                                                    self.width, self.orientation)

    def __str__(self):
        return self.__repr__()

    def _copy(self):
        new_port = Term(parent=self.parent,
                        name=self.name,
                        midpoint=self.midpoint,
                        width=self.width,
                        length=self.length,
                        gdslayer=deepcopy(self.gdslayer),
                        poly_layer=deepcopy(self.poly_layer),
                        text_layer=deepcopy(self.text_layer),
                        orientation=self.orientation)
        return new_port











