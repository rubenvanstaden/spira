import numpy as np

from spira.yevon.process.gdsii_layer import Layer
from spira.yevon.process.gdsii_layer import __DerivedDoubleLayer__
from spira.yevon.process.gdsii_layer import __DerivedLayerAnd__
from spira.yevon.process.gdsii_layer import __DerivedLayerXor__

from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.polygon_group import PolygonGroup
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.yevon.geometry.edges.edges import Edge
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'get_derived_elementals',
]


def derived_elementals(elems, generated_layer):
    """  """
    if isinstance(generated_layer, Layer):
        LF = LayerFilterAllow(layers=[generated_layer])
        el = LF(elems.polygons)
        pg = PolygonGroup(elementals=el, layer=generated_layer)
        return pg
    elif isinstance(generated_layer, __DerivedDoubleLayer__):
        p1 = derived_elementals(elems, generated_layer.layer1)
        p2 = derived_elementals(elems, generated_layer.layer2)
        if isinstance(generated_layer, __DerivedLayerAnd__):
            pg = p1 & p2
        elif isinstance(generated_layer, __DerivedLayerXor__):
            pg = p1 ^ p2
        return pg
    else:
        raise Exception("Unexpected type for parameter 'generated_layer' : %s" % str(type(generated_layer)))


def get_derived_elementals(elements, mapping, store_as_edge=False):
    """
    Given a list of elements and a list of tuples (DerivedLayer, PPLayer), 
    create new elements according to the boolean operations of the 
    DerivedLayer and place these elements on the specified PPLayer.
    """
    derived_layers = mapping.keys()
    export_layers = mapping.values()
    elems = ElementalList()
    for generated_layer, export_layer in zip(derived_layers, export_layers):
        pg = derived_elementals(elems=elements, generated_layer=generated_layer)
        for p in pg.elementals:
            ply = Polygon(shape=p.shape, layer=export_layer)
            if store_as_edge is True:
                elems += Edge(outside=ply, layer=export_layer)
            else: elems += ply
    return elems


def get_derived_edge_ports():
    """ Generate ports from the derived edge polygons. """
    pass





