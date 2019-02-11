import spira
import pyclipper
import numpy as np

from spira import param
from copy import copy, deepcopy
from spira.gdsii.elemental.port import PortAbstract
from spira.core.initializer import ElementalInitializer


class Term(PortAbstract):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.

    Examples
    --------
    >>> term = spira.Term()
    """

    width = param.FloatField(default=2*1e6)
    length = param.FloatField(default=0.1*1e6)

    layer1 = param.LayerField()
    layer2 = param.LayerField()

    port1 = param.DataField(fdef_name='create_port1')
    port2 = param.DataField(fdef_name='create_port2')

    def __init__(self, port=None, polygon=None, **kwargs):
        super().__init__(port=port, polygon=polygon, **kwargs)

        from spira import shapes
        if polygon is None:
            rect_shape = shapes.RectangleShape(
                p1=[0, 0],
                p2=[self.width, self.length]
            )
            pp = spira.Polygons(
                shape=rect_shape,
                gdslayer=spira.Layer(number=63)
            )
            pp.rotate(angle=self.orientation, center=self.midpoint)
            # pp.rotate(angle=90-self.orientation, center=self.midpoint)
            pp.move(midpoint=pp.center, destination=self.midpoint)
            self.polygon = pp
        else:
            self.polygon = polygon

        arrow_shape = shapes.ArrowShape(
            a = self.width/10,
            b = self.width/20,
            c = self.width/5
        )

        arrow_shape.apply_merge
        # arrow_shape.rotate(angle=self.orientation)

        self.arrow = spira.Polygons(
            shape=arrow_shape,
            gdslayer=spira.Layer(number=77)
        )

        self.arrow.rotate(angle=self.orientation)
        # self.arrow.rotate(angle=90-self.orientation)

    def __repr__(self):
        return ("[SPiRA: Term] (name {}, number {}, midpoint {}, " +
            "width {}, orientation {})").format(self.name,
            self.gdslayer.number, self.midpoint,
            self.width, self.orientation
        )

    def _copy(self):
        new_port = Term(parent=self.parent,
            name=self.name,
            midpoint=self.midpoint,
            width=self.width,
            length=self.length,
            gdslayer=deepcopy(self.gdslayer),
            orientation=self.orientation)
        return new_port

    def create_port1(self):
        port = spira.Port(name='P1', midpoint=self.midpoint, gdslayer=self.layer1)
        return port

    def create_port2(self):
        port = spira.Port(name='P2', midpoint=self.midpoint, gdslayer=self.layer2)
        return port

    def point_inside(self, polygon):
        if pyclipper.PointInPolygon(self.endpoints[0], polygon) != 0:
            return True
        elif pyclipper.PointInPolygon(self.endpoints[1], polygon) != 0:
            return True

    @property
    def endpoints(self):
        dx = self.width/2*np.cos((self.orientation - 90)*np.pi/180)
        dy = self.width/2*np.sin((self.orientation - 90)*np.pi/180)
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
            self.gdslayer.number, self.midpoint,
            self.width, self.orientation
        )

    def _copy(self):
        new_port = Dummy(parent=self.parent,
            name=self.name,
            midpoint=self.midpoint,
            width=self.width,
            length=self.length,
            gdslayer=deepcopy(self.gdslayer),
            orientation=self.orientation)
        return new_port









