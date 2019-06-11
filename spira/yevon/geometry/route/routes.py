# from spira.yevon.gdsii.polygon import Polygon
import gdspy
import spira.all as spira

# from spira.yevon.geometry.ports.port import point_in_port_polygon
from spira.core.parameters.restrictions import RestrictTypeList
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.route.route_shaper import RouteSimple
from spira.core.parameters.descriptor import FunctionField
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class Route(spira.Polygon):
    """  """

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

        # ports = super().create_ports(ports)

        # from copy import deepcopy
        # # for p in deepcopy(_ports):
        # for p in _ports:
        #     print('wenfkewfbjkwefbjkwefkwbekf')
        #     if point_in_port_polygon(p, self.shape.m1):
        #         p.locked = False
        #         # ports += p

        # p1 = spira.Port(name='P1', midpoint=self.shape.m1, width=self.shape.w1, orientation=self.shape.o1)
        # p2 = spira.Port(name='P2', midpoint=self.shape.m2, width=self.shape.w2, orientation=self.shape.o2)
        
        p1 = spira.Port(name='P1', midpoint=self.shape.m1, width=self.shape.port1.width, orientation=self.shape.o1)
        p2 = spira.Port(name='P2', midpoint=self.shape.m2, width=self.shape.port2.width, orientation=self.shape.o2)
        
        ports += p1
        ports += p2

        return ports


def RouteStraight(p1, p2, layer, path_type='straight', width_type='straight'):
    """ Routes a straight polygon between two ports.

    Example
    -------
    >>> R = RouteStraight()
    """
    shape = RouteSimple(port1=p1, port2=p2, path_type=path_type, width_type=width_type)
    R = Route(shape=shape, layer=layer)
    T = vector_match_transform(v1=R.ports[0], v2=p1)
    R.transform(T)
    return R

    # return Route(shape=shape, layer=layer, port_labels=[p1.name, p2.name])
