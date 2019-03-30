import spira
import pyclipper
import numpy as np

from spira import param
from copy import copy, deepcopy
from spira.visualization import color
from spira.gdsii.elemental.port import PortAbstract, __Port__
from spira.core.initializer import ElementalInitializer
from spira.gdsii.group import GroupElementals


RDD = spira.get_rule_deck()


class Term(PortAbstract):
    """ Terminals are horizontal ports that connect SRef 
    instances in the horizontal plane. They typcially 
    represents the i/o ports of a components.

    Examples
    --------
    >>> term = spira.Term()
    """

    edgelayer = param.LayerField(name='Edge', number=63)
    arrowlayer = param.LayerField(name='Arrow', number=77)
    color = param.ColorField(default=color.COLOR_GRAY)

    # connections = param.ElementalListField()
    connections = param.ListField(default=[])

    local_connect = param.StringField()
    external_connect = param.StringField()

    width = param.NumberField(default=2*1e6)

    layer1 = param.LayerField()
    layer2 = param.LayerField()

    is_edge = param.BoolField(default=False)

    port1 = param.DataField(fdef_name='create_port1')
    port2 = param.DataField(fdef_name='create_port2')

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

    length = param.FunctionField(get_length, set_length, doc='Set the width of the terminal edge equal to a 3rd of the minimum metal width.')

    def __init__(self, port=None, elementals=None, polygon=None, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)
        if elementals is not None:
            self.elementals = elementals

    def __repr__(self):
        return ("[SPiRA: Term] (name {}, lock {}, number {}, midpoint {}, " +
            "width {}, orientation {}, length {}, edgelayer {}, arrowlayer {})").format(
                self.name, self.locked, self.gds_layer.number, self.midpoint, self.width, 
                self.orientation, self.length, self.edgelayer, self.arrowlayer
        )

    def __str__(self):
        return self.__repr__()

    def create_port1(self):
        port = spira.Port(name='P1', midpoint=self.midpoint, gds_layer=self.layer1)
        return port

    def create_port2(self):
        port = spira.Port(name='P2', midpoint=self.midpoint, gds_layer=self.layer2)
        return port

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

    @property
    def edge(self):
        from spira import shapes
        dx = self.length
        dy = self.width - dx
        # dy = self.width
        rect_shape = shapes.RectangleShape(p1=[0, 0], p2=[dx, dy])
        ply = spira.Polygons(shape=rect_shape, gds_layer=self.edgelayer, direction=90)
        if self.reflection:
            ply.reflect()
        ply.rotate(angle=self.orientation)
        ply.move(midpoint=ply.center, destination=self.midpoint)
        return ply

    @property
    def arrow(self):
        from spira import shapes
        arrow_shape = shapes.ArrowShape(a=self.length, b=self.length/2, c=self.length*2)
        arrow_shape.apply_merge
        ply = spira.Polygons(shape=arrow_shape, gds_layer=self.arrowlayer)
        if self.reflection:
            ply.reflect()
        ply.rotate(angle=self.orientation)
        ply.move(midpoint=ply.center, destination=self.midpoint)
        return ply

    def commit_to_gdspy(self, cell):
        if self.__repr__() not in list(__Port__.__committed__.keys()):
            self.edge.commit_to_gdspy(cell=cell)
            # self.arrow.commit_to_gdspy(cell=cell)
            self.label.commit_to_gdspy(cell=cell)
            __Port__.__committed__.update({self.__repr__(): self})
        else:
            p = __Port__.__committed__[self.__repr__()]
            p.edge.commit_to_gdspy(cell=cell)
            # p.arrow.commit_to_gdspy(cell=cell)
            p.label.commit_to_gdspy(cell=cell)

    def _copy(self):
        new_port = Term(
            parent=self.parent,
            name=self.name,
            midpoint=deepcopy(self.midpoint),
            orientation=deepcopy(self.orientation),
            reflection=self.reflection,
            width=deepcopy(self.width),
            length=deepcopy(self.length),
            gds_layer=deepcopy(self.gds_layer),
            edgelayer=deepcopy(self.edgelayer),
            arrowlayer=deepcopy(self.arrowlayer),
            local_connect=self.local_connect,
            external_connect=self.external_connect,
            color=self.color,
            is_edge=self.is_edge
        )
        return new_port


class EdgeTerm(Term):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.

    Examples
    --------
    >>> term = spira.Term()
    """

    def __repr__(self):
        return ("[SPiRA: EdgeTerm] (name {}, number {}, datatype {}, midpoint {}, " +
            "width {}, orientation {})").format(self.name,
            self.gds_layer.number, self.gds_layer.datatype, self.midpoint,
            self.width, self.orientation
        )

    def reflect(self):
        """ Do not reflect EdgeTerms when reference is reflected. """
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = 180 - self.orientation
        self.orientation = np.mod(self.orientation, 360)
        return self


class Dummy(Term):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.

    Examples
    --------
    >>> term = spira.Term()
    """

    def __repr__(self):
        return ("[SPiRA: Dummy] (name {}, number {}, midpoint {}, " +
            "width {}, orientation {})").format(self.name,
            self.gds_layer.number, self.midpoint,
            self.width, self.orientation
        )


if __name__ == '__main__':

    cell = spira.Cell('Terminal Test')
    term = Term()
    cell += term
    cell.output()









