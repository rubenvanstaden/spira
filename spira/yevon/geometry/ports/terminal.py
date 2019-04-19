import spira.all as spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import utils

from spira.core import param
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.rdd import get_rule_deck

from spira.core.param.variables import *
from spira.yevon.layer import LayerField
from spira.core.descriptor import DataField
from spira.yevon.geometry.coord import CoordField
from spira.core.descriptor import DataField, FunctionField
from spira.yevon.geometry.ports.base import __HorizontalPort__
from spira.yevon.gdsii.group import Group


RDD = get_rule_deck()


class Terminal(Group, __HorizontalPort__):
    """  """

    width = NumberField(default=2*1e6)
    
    edgelayer = LayerField(name='Edge', number=63)
    arrowlayer = LayerField(name='Arrow', number=77)

    edge = DataField(fdef_name='create_edge')
    arrow = DataField(fdef_name='create_arrow')

    def get_length(self):
        if not hasattr(self, '__length__'):
            key = self.gds_layer.name
            if key in RDD.keys:
                if RDD.name == 'MiTLL':
                    self.__length__ = RDD[key].MIN_SIZE * 1e6
                elif RDD.name == 'AiST':
                    self.__length__ = RDD[key].WIDTH * 1e6
            else:
                self.__length__ = RDD.GDSII.TERM_WIDTH
        return self.__length__

    def set_length(self, value):
        self.__length__ = value

    length = FunctionField(get_length, set_length, doc='Set the width of the terminal edge equal to a 3rd of the minimum metal width.')

    def __init__(self, port=None, elementals=None, polygon=None, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return ("[SPiRA: Terminal] (name {}, midpoint {})").format(self.name, self.midpoint)

    def __str__(self):
        return self.__repr__()

    def create_edge(self):
        from spira.yevon.geometry import shapes
        dx = self.length
        dy = self.width - dx
        rect_shape = shapes.RectangleShape(p1=[0, 0], p2=[dx, dy])
        tf = spira.Translation(self.midpoint) + spira.Rotation(self.orientation)
        # ply = spira.Polygon(shape=rect_shape, gds_layer=self.edgelayer, direction=90, transformation=tf)
        ply = spira.Polygon(shape=rect_shape, gds_layer=self.edgelayer)
        ply.center = (0,0)
        ply.transform(tf)
        return ply

    def create_arrow(self):
        from spira.yevon.geometry import shapes
        arrow_shape = shapes.ArrowShape(a=self.length, b=self.length/2, c=self.length*2)
        arrow_shape.apply_merge
        tf = spira.Translation(self.midpoint) + spira.Rotation(self.orientation + 90)
        # ply = spira.Polygon(shape=arrow_shape, gds_layer=self.arrowlayer, transformation=tf)
        ply = spira.Polygon(shape=arrow_shape, gds_layer=self.arrowlayer)
        ply.center = (0,0)
        ply.transform(tf)
        return ply

    def encloses(self, points):
        if pyclipper.PointInPolygon(self.endpoints[0], points) != 0:
            return True
        elif pyclipper.PointInPolygon(self.endpoints[1], points) != 0:
            return True

    def encloses_midpoint(self, points):
        return pyclipper.PointInPolygon(self.midpoint, points) != 0

    @property
    def endpoints(self):
        dx = self.length/2*np.cos((self.orientation - 90)*np.pi/180)
        dy = self.length/2*np.sin((self.orientation - 90)*np.pi/180)
        left_point = self.midpoint - np.array([dx,dy])
        right_point = self.midpoint + np.array([dx,dy])
        return np.array([left_point, right_point])

    @endpoints.setter
    def endpoints(self, points):
        p1, p2 = np.array(points[0]), np.array(points[1])
        self.midpoint = (p1+p2)/2
        dx, dy = p2-p1
        self.orientation = np.arctan2(dx,dy)*180/np.pi
        self.width = np.sqrt(dx**2 + dy**2)

    def create_elementals(self, elems):
        elems += self.edge
        elems += self.arrow
        elems += self.label
        return elems


