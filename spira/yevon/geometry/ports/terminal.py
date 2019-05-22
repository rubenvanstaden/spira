import gdspy
import pyclipper
import numpy as np
import spira.all as spira
from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import utils

from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.rdd import get_rule_deck

from spira.core.parameters.variables import *
from spira.yevon.layer import LayerField
from spira.core.parameters.descriptor import DataField
from spira.yevon.geometry.coord import CoordField
from spira.core.parameters.descriptor import DataField, FunctionField
from spira.yevon.geometry.ports.base import __HorizontalPort__
from spira.yevon.gdsii.group import Group
from spira.yevon.geometry.coord import Coord


RDD = get_rule_deck()


class Terminal(__HorizontalPort__):
    """  """

    local_pid = StringField()
    bbox = BoolField(default=False)

    width = NumberField(default=2*1e6)

    edgelayer = LayerField(name='Edge', number=63)
    unlocked_layer = LayerField(name='Unlocked', number=100)
    arrowlayer = LayerField(name='Arrow', number=77)

    edge = DataField(fdef_name='create_edge')
    arrow = DataField(fdef_name='create_arrow')
    
    # def __deepcopy__(self, memo):
    #     ply = self.modified_copy(
    #         midpoint=deepcopy(self.midpoint),
    #         orientation=deepcopy(self.orientation),
    #         gds_layer=deepcopy(self.gds_layer)
    #     )
    #     return ply

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

    length = FunctionField(get_length, set_length, doc='Set the width of the terminal edge.')

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.gds_layer.name
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return ("[SPiRA: Terminal] (name {}, alias {}, locked {}, midpoint {} orientation {} width {})").format(self.name, self.alias, self.locked, self.midpoint, self.orientation, self.width)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, str):
            return (self.name == other)
        else:
            if not isinstance(self.midpoint, Coord):
                self.midpoint = Coord(self.midpoint[0], self.midpoint[1])
            if not isinstance(other.midpoint, Coord):
                other.midpoint = Coord(other.midpoint[0], other.midpoint[1])
            return ((self.name == other.name) and (self.midpoint == other.midpoint) and (self.orientation == other.orientation))

    def __ne__(self, other):
        return (self.midpoint != other.midpoint or (self.orientation != other.orientation)) 
        
    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(deepcopy(self.midpoint))
        self.orientation = transformation.apply_to_angle(deepcopy(self.orientation))
        return self

    def transform_copy(self, transformation):
        port = Terminal(
            name=self.name,
            # alias = self.name + transformation.id_string(),
            midpoint=transformation.apply_to_coord(deepcopy(self.midpoint)),
            orientation=transformation.apply_to_angle(deepcopy(self.orientation)),
            # midpoint=transformation.apply_to_coord(self.midpoint),
            # orientation=transformation.apply_to_angle(self.orientation),
            # gds_layer=self.gds_layer,
            # text_type=self.text_type,
            locked=deepcopy(self.locked),
            width=self.width,
            local_pid=self.local_pid
        )
        return port

    def commit_to_gdspy(self, cell=None):
        if self.__repr__() not in list(Terminal.__committed__.keys()):
            self.edge.commit_to_gdspy(cell=cell)
            # self.arrow.commit_to_gdspy(cell=cell)
            self.label.commit_to_gdspy(cell=cell)
            Terminal.__committed__.update({self.__repr__(): self})
        else:
            p = Terminal.__committed__[self.__repr__()]
            p.edge.commit_to_gdspy(cell=cell)
            # p.arrow.commit_to_gdspy(cell=cell)
            p.label.commit_to_gdspy(cell=cell)

    @property
    def label(self):
        if self.locked is True:
            layer = self.gds_layer
            text_type = self.text_type
        else:
            layer = self.unlocked_layer
            text_type = self.unlocked_layer
        lbl = spira.Label(
            position=self.midpoint,
            text=self.name,
            # text=self.alias,
            gds_layer=layer,
            # texttype=text_type,
            texttype=33,
            orientation=self.orientation,
            # color=color.COLOR_GHOSTWHITE
        )
        # lbl.__rotate__(angle=self.orientation)
        # lbl.move(midpoint=lbl.position, destination=self.midpoint)
        return lbl

    def create_edge(self):
        from spira.yevon.rdd.layer import PhysicalLayer
        from spira.yevon.geometry import shapes
        dx = self.length
        dy = self.width - dx
        rect_shape = shapes.RectangleShape(p1=[0, 0], p2=[dx, dy])
        # if self.locked is True:
        #     ply = spira.Polygon(shape=rect_shape, gds_layer=self.edgelayer, enable_edges=False)
        # else:
        #     ply = spira.Polygon(shape=rect_shape, gds_layer=self.unlocked_layer, enable_edge=False)
        ps1 = PhysicalLayer(layer=self.edgelayer)
        ps2 = PhysicalLayer(layer=self.unlocked_layer)
        if self.locked is True:
            ply = spira.Polygon(shape=rect_shape, ps_layer=ps1, enable_edges=False)
        else:
            ply = spira.Polygon(shape=rect_shape, ps_layer=ps2, enable_edges=False)
        ply.center = (0,0)
        angle = self.orientation
        T = spira.Rotation(rotation=angle)
        ply.transform(T)
        ply.move_new(self.midpoint)
        # ply.move(midpoint=rect_shape.center_of_mass, destination=self.midpoint)
        return ply

    def create_arrow(self):
        from spira.yevon.geometry import shapes
        arrow_shape = shapes.ArrowShape(a=self.length, b=self.length/2, c=self.length*2)
        # arrow_shape.apply_merge
        ply = spira.Polygon(shape=arrow_shape, gds_layer=self.arrowlayer, enable_edges=False)
        ply.center = (0,0)
        angle = self.orientation - 90
        T = spira.Rotation(rotation=angle)
        ply.transform(T)
        ply.move_new(self.midpoint)
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


class EdgeTerminal(Terminal):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.

    Examples
    --------
    >>> term = spira.Terminal()
    """

    # def __repr__(self):
    #     return ("[SPiRA: spira.EdgeTerminal] (name {}, number {}, datatype {}, midpoint {}, " +
    #         "width {}, orientation {})").format(self.name,
    #         self.gds_layer.number, self.gds_layer.datatype, self.midpoint,
    #         self.width, self.orientation
    #     )
        
    def __repr__(self):
        return ("[SPiRA: Terminal] (name {}, locked {}, midpoint {} orientation {} width {})").format(self.name, self.locked, self.midpoint, self.orientation, self.width)

    def __reflect__(self):
        """ Do not reflect EdgeTerms when reference is reflected. """
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = 180 - self.orientation
        self.orientation = np.mod(self.orientation, 360)
        return self


