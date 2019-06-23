import gdspy
import numpy as np
import spira.all as spira

from numpy.linalg import norm
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.ports.port_list import PortList
from spira.yevon.utils.geometry import distance
from spira.yevon.utils import geometry as ug
from spira.yevon.geometry.route.route_shaper import *
from spira.core.parameters.restrictions import RestrictTypeList
from spira.yevon.geometry import shapes
from spira.yevon import constants
from spira.yevon.utils import clipping
from spira.core.parameters.descriptor import FunctionField
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Route', 'RouteStraight', 'RoutePath', 'Route90', 'RouteShape', 'Route180', 'RouteManhattan']


class RouteShape(shapes.Shape):

    path = spira.DataField()

    def create_points(self, points):
        if isinstance(self.path, gdspy.Path):
            points = clipping.boolean(subj=self.path.polygons, clip_type='or')[0]
        elif isinstance(self.path, gdspy.FlexPath):
            points = self.path.get_polygons()[0]
        return points


class Route(spira.Polygon):
    """  """

    p1 = spira.PortField()
    p2 = spira.PortField()

    port_labels = spira.ListField(
        allow_none=True,
        restriction=RestrictTypeList(str),
        doc="labels of ports to be processes. Set to None to process all ports"
    )

    def __init__(self, shape, layer, **kwargs):
        super().__init__(shape=shape, layer=layer, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Route is None!'
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        class_string = "[SPiRA: Route {}] (center {}, vertices {}, process {}, purpose {})"
        return class_string.format(self.alias, self.center, self.count, self.process, self.purpose)

    def __str__(self):
        return self.__repr__()

    def create_ports(self, ports):

        from copy import deepcopy
        port1 = deepcopy(self.p1)
        port1.purpose = RDD.PURPOSE.ROUTE

        port2 = deepcopy(self.p2)
        port2.purpose = RDD.PURPOSE.ROUTE

        ports += port1
        ports += port2

        return ports


def RouteStraight(p1, p2, layer, path_type='straight', width_type='straight'):
    """ Routes a straight polygon between two ports.

    Example
    -------
    >>> R = RouteStraight()
    """

    point_a = p1.midpoint
    point_b = p2.midpoint
    width_input = p1.width
    width_output = p2.width

    if ug.angle_diff(p2.orientation, p1.orientation) != 180:
        raise ValueError('Ports do not face eachother.')

    separation = np.array([point_b[0], point_b[1]]) - np.array([point_a[0], point_a[1]])
    distance = norm(separation)
    rotation = np.arctan2(separation[1], separation[0]) * constants.RAD2DEG
    angle = rotation - p1.orientation
    xf = distance * np.cos(angle*constants.DEG2RAD)
    yf = distance * np.sin(angle*constants.DEG2RAD)

    if path_type == 'straight':
        curve_fun = lambda t: [xf*t, yf*t]
        curve_deriv_fun = lambda t: [xf + t*0, 0 + t*0]
    if path_type == 'sine':
        curve_fun = lambda t: [xf*t, yf*(1-np.cos(t*np.pi))/2]
        curve_deriv_fun = lambda t: [xf + t*0, yf*(np.sin(t*np.pi)*np.pi)/2]

    if width_type == 'straight':
        width_fun = lambda t: (width_output - width_input)*t + width_input
    if width_type == 'sine':
        width_fun = lambda t: (width_output - width_input)*(1-np.cos(t*np.pi))/2 + width_input

    route_path = gdspy.Path(width=width_input, initial_point=(0,0))
    route_path.parametric(curve_fun, curve_deriv_fun, final_width=width_fun)

    port1 = spira.Port(midpoint=(0,0), width=width_input, orientation=180)
    port2 = spira.Port(midpoint=(xf,yf), width=width_output, orientation=0)

    route_shape = RouteShape(path=route_path)
    R = Route(shape=route_shape, p1=port1, p2=port2, layer=layer)
    T = vector_match_transform(v1=R.ports[0], v2=p1)
    R.transform(T)
    return R


def RoutePath(port1, port2, start_straight, end_straight, path, width, layer):

    pts = []

    p1 = port1.midpoint.to_numpy_array()
    p2 = port2.midpoint.to_numpy_array()

    if port1.orientation == 0:
        c1 = p1 + [start_straight, 0]
    if port2.orientation == 180:
        c2 = p2 - [start_straight, 0]

    pts.append(p1)
    pts.append(c1)
    pts.extend(path)
    pts.append(c2)
    pts.append(p2)

    # path = gdspy.FlexPath(points=pts, width=1, corners='circular bend', bend_radius=1)
    path = gdspy.FlexPath(points=pts, width=1, corners='miter')
    route_shape = RouteShape(path=path)
    R = Route(shape=route_shape, p1=port1, p2=port2, layer=RDD.PLAYER.M6.METAL)

    return R


def Route90(port1, port2, layer, width=None, corners='miter', bend_radius=1):
    """  """

    if port1.orientation == 0:
        p1 = [port1.midpoint[0], port1.midpoint[1]]
        p2 = [port2.midpoint[0], port2.midpoint[1]]
    if port1.orientation == 90:
        p1 = [port1.midpoint[1], -port1.midpoint[0]]
        p2 = [port2.midpoint[1], -port2.midpoint[0]]
    if port1.orientation == 180:
        p1 = [-port1.midpoint[0], -port1.midpoint[1]]
        p2 = [-port2.midpoint[0], -port2.midpoint[1]]
    if port1.orientation == 270:
        p1 = [-port1.midpoint[1], port1.midpoint[0]]
        p2 = [-port2.midpoint[1], port2.midpoint[0]]

    if width is None:
        width = port1.width

    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])

    p3 = np.array(p2) - np.array(p1)

    path = gdspy.FlexPath([(0,0), (dx, 0)], width=width, corners=corners, bend_radius=bend_radius)
    path.segment(end_point=p3)

    pl = PortList()
    pl += spira.Port(name='T1', midpoint=(0,0), width=port1.width, orientation=180)
    pl += spira.Port(name='T2', midpoint=list(np.subtract(p2, p1)), width=port2.width, orientation=90)

    shape = RouteShape(path=path)
    # points = path.get_polygons()[0]
    # R = Route(shape=points, ports=pl, layer=layer)
    R = Route(shape=shape, ports=pl, layer=layer)
    T = vector_match_transform(v1=R.ports[0], v2=port1)
    R.transform(T)

    return R


def Route180(port1, port2, layer, width=None, corners='miter', bend_radius=1):
    """  """

    if port1.orientation == 0:
        p1 = [port1.midpoint[0], port1.midpoint[1]]
        p2 = [port2.midpoint[0], port2.midpoint[1]]
    if port1.orientation == 90:
        p1 = [port1.midpoint[1], -port1.midpoint[0]]
        p2 = [port2.midpoint[1], -port2.midpoint[0]]
    if port1.orientation == 180:
        p1 = [-port1.midpoint[0], -port1.midpoint[1]]
        p2 = [-port2.midpoint[0], -port2.midpoint[1]]
    if port1.orientation == 270:
        p1 = [-port1.midpoint[1], port1.midpoint[0]]
        p2 = [-port2.midpoint[1], port2.midpoint[0]]

    if width is None:
        width = port1.width

    dx = (p2[0] - p1[0])/2
    
    p3 = np.array(p2) - np.array(p1) - np.array([dx,0])
    p4 = np.array(p2) - np.array(p1)

    path = gdspy.FlexPath([(0,0), (dx, 0)], width=width, corners=corners, bend_radius=bend_radius)
    path.segment(end_point=p3)
    path.segment(end_point=p4)

    if ug.angle_diff(port2.orientation, port1.orientation) != 180:
        raise ValueError("Route error: Ports do not face each other (orientations must be 180 apart)")
    else:
        pl = PortList()
        pl += spira.Port(name='T1', midpoint=(0,0), width=port1.width, orientation=180)
        pl += spira.Port(name='T2', midpoint=list(np.subtract(p2, p1)), width=port2.width, orientation=0)

    shape = RouteShape(path=path)
    # points = path.get_polygons()[0]
    # R = Route(shape=points, ports=pl, layer=layer)
    R = Route(shape=shape, ports=pl, layer=layer)
    T = vector_match_transform(v1=R.ports[0], v2=port1)
    R.transform(T)

    return R


def RouteManhattan(ports, layer, width=None, corners='miter', bend_radius=1):
    from spira.yevon.utils import geometry

    elems = spira.ElementalList()

    if isinstance(ports, list):
        list1 = [p for p in ports if isinstance(p, spira.DummyPort)]
    else:
        list1 = ports.get_dummy_ports()
    list2 = [p.flip() for p in list1]

    n = 2
    iter1 = iter(list1)
    pl = []
    for x in list2:
        pl.extend([next(iter1) for _ in range(n - 1)])
        pl.append(x)
    pl.extend(iter1)

    pl.insert(0, ports[0])
    pl.append(ports[-1])

    for x in range(len(pl)-1):
        p1, p2 = pl[x], pl[x+1]
        angle = ug.angle_diff(p2.orientation, p1.orientation)
        
        print(angle)
        if angle not in [90, 180, 270]:
            raise ValueError('Angle must be in 90 degree angles.')

        if (angle == 180) and (p1.midpoint != p2.midpoint):
            elems += Route180(port1=p1, port2=p2, width=width, layer=layer, corners=corners, bend_radius=bend_radius)
        elif (angle == 90) or (angle == 270):
            elems += Route90(port1=p1, port2=p2, width=width, layer=layer, corners=corners, bend_radius=bend_radius)
    return elems


if __name__ == '__main__':

    # --------------------- 90 Degree Turns -------------------------

    # Q1
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=0)
    # port2 = spira.Port(name='P2', midpoint=(20,10), orientation=-90)
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=90)
    # port2 = spira.Port(name='P2', midpoint=(20,10), orientation=180)
    # port1 = spira.Port(name='P1', midpoint=(5,-25), orientation=90)
    # port2 = spira.Port(name='P2', midpoint=(10,-20), orientation=180)

    # Q2
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=180)
    # port2 = spira.Port(name='P2', midpoint=(-20,10), orientation=-90)
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=90)
    # port2 = spira.Port(name='P2', midpoint=(-20,10), orientation=0)

    # Q3
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=180)
    # port2 = spira.Port(name='P2', midpoint=(-20,-10), orientation=90)
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=-90)
    # port2 = spira.Port(name='P2', midpoint=(-20,-10), orientation=0)

    # Q4
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=0)
    # port2 = spira.Port(name='P2', midpoint=(20,-10), orientation=90)
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=270)
    # port2 = spira.Port(name='P2', midpoint=(20,-10), orientation=180)
    
    # port1 = spira.Port(name='P1', midpoint=(10,0), orientation=270)
    # port2 = spira.Port(name='P2', midpoint=(30,-10), orientation=180)

    # D = spira.Cell(name='Route')
    # D += Route90(port1, port2, width=1, layer=spira.Layer(1))
    
    # --------------------- 90 Degree Turns -------------------------

    # # Q1
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=0)
    # port2 = spira.Port(name='P2', midpoint=(20,10), orientation=180)
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=90)
    # port2 = spira.Port(name='P2', midpoint=(20,10), orientation=270)

    # # Q2
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=180)
    # port2 = spira.Port(name='P2', midpoint=(-20,10), orientation=0)
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=90)
    # port2 = spira.Port(name='P2', midpoint=(-20,10), orientation=270)

    # # Q3
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=180)
    # port2 = spira.Port(name='P2', midpoint=(-20,-10), orientation=0)
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=90)
    # port2 = spira.Port(name='P2', midpoint=(-20,10), orientation=270)
    
    # # Q4
    # port1 = spira.Port(name='P1', midpoint=(0,0), orientation=0)
    # port2 = spira.Port(name='P2', midpoint=(20,-10), orientation=180)
    port1 = spira.Port(name='P1', midpoint=(0,0), orientation=270)
    port2 = spira.Port(name='P2', midpoint=(20,-10), orientation=90)

    D = spira.Cell(name='Route')
    D += Route180(port1, port2, width=1, layer=spira.Layer(1))

    D.gdsii_output()

