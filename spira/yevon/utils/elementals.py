import spira.all as spira
import numpy as np

from spira.yevon.geometry import shapes
from spira.yevon.rdd import get_rule_deck
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.geometry.ports.port_list import PortList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.utils import clipping


RDD = get_rule_deck()


__all__ = [
    'convert_polygons_to_processlayers',
    'connect_processlayer_edges'
]


def get_polygon_by_physical_layer(elems, ps_layer):
    el = ElementalList()
    for e in elems.polygons:
        if isinstance(e, pc.Polygon):
            if e.ps_layer == ps_layer:
                el += e
        elif isinstance(e, Polygon):
            if e.gds_layer == ps_layer.layer:
                el += e
        else:
            raise ValueError('Elemental is not a polygon.')
    return el


def convert_polygons_to_processlayers(polygon_elems):
    R = polygon_elems.flat_copy()
    elems = ElementalList()
    for ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
        Rm = R.get_polygons(layer=ps_layer.layer)
        for i, e in enumerate(Rm):
            # alias = 'ply_{}_{}_{}'.format(ps_layer.layer.number, self.__class__.__name__, i)
            alias = 'ply_{}_{}_{}'.format(ps_layer.layer.number, 'CLASS_NAME', i)
            elems += pc.Polygon(name=alias, ps_layer=ps_layer, points=e.polygons)
    return elems


def connect_processlayer_edges(elems):
    ports = PortList()
    for i in range(len(elems)):
        for j in range(len(elems)):
            if i != j:
                e1, e2 = elems[i], elems[j]
                if e1.ps_layer == e2.ps_layer:
                    if e1.ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
                        pl = elems[i].ports & elems[j]
                        for p in pl:
                            ports += p
    return ports




# def connect_processlayer_edges(E):
#     ports = PortList()
#     for ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
#         elems = R.get_polygons(layer=ps_layer.layer)
#         for i in range(len(elems)):
#             for j in range(len(elems)):
#                 if i != j:
#                     e1, e2 = elems[i], elems[j]
#                     if e1.ps_layer == e2.ps_layer:
#                         pl = elems[i].ports & elems[j]
#                         for p in pl:
#                             ports += p
#     return ports

