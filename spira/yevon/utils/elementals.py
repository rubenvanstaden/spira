import spira.all as spira
import numpy as np

from spira.yevon.geometry import shapes
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.geometry.ports.port_list import PortList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.utils import clipping
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'get_generated_elementals',
]


# from spira.yevon.process.gdsii_layer import Layer, __GeneratedDoubleLayer__, __GeneratedLayerAnd__, __GeneratedLayerXor__
# def _generated_elementals(elems, generated_layer):
#     # from spira.yevon.process.gdsii_layer import Layer, __GeneratedDoubleLayer__, 
#     from spira.yevon.gdsii.polygon import Polygon, PolygonGroup
#     from spira.yevon.filters.layer_filter import LayerFilterAllow

#     if isinstance(generated_layer, Layer):
#         LF = LayerFilterAllow(layers=[generated_layer])
#         el = LF(elems.polygons)
#         pg = PolygonGroup(elementals=el, layer=generated_layer).merge
#         return pg
#     elif isinstance(generated_layer, __GeneratedDoubleLayer__):
#         p1 = _generated_elementals(elems, generated_layer.layer1)
#         p2 = _generated_elementals(elems, generated_layer.layer2)
#         if isinstance(generated_layer, __GeneratedLayerAnd__):
#             pg = p1 & p2
#             return pg
#             # pg = p1.intersection(p2)
#         # elif isinstance(generated_layer, __GeneratedLayerOr__):
#         #     pg = p1.union(p2)
#         elif isinstance(generated_layer, __GeneratedLayerXor__):
#             pg = p1 ^ p2
#             # pg = p1.difference(p2)
#         return pg
#     else:
#         raise Exception("Unexpected type for parameter 'generated_layer' : %s" % str(type(generated_layer)))




from spira.yevon.process.gdsii_layer import Layer, __GeneratedDoubleLayer__, __GeneratedLayerAnd__, __GeneratedLayerXor__
def _generated_elementals(elems, generated_layer):
    from spira.yevon.gdsii.polygon import Polygon, PolygonGroup
    from spira.yevon.filters.layer_filter import LayerFilterAllow

    if isinstance(generated_layer, Layer):
        LF = LayerFilterAllow(layers=[generated_layer])
        el = LF(elems.polygons)
        pg = PolygonGroup(elementals=el, layer=generated_layer).merge
        return pg
    elif isinstance(generated_layer, __GeneratedDoubleLayer__):
        p1 = _generated_elementals(elems, generated_layer.layer1)
        p2 = _generated_elementals(elems, generated_layer.layer2)
        if isinstance(generated_layer, __GeneratedLayerAnd__):
            pg = p1 & p2
        elif isinstance(generated_layer, __GeneratedLayerXor__):
            pg = p1 ^ p2
        return pg
    else:
        raise Exception("Unexpected type for parameter 'generated_layer' : %s" % str(type(generated_layer)))



def get_generated_elementals(elements, mapping):
    """
    Given a list of elements and a list of tuples (GeneratedLayer, PPLayer), create new elements according to the boolean
    operations of the GeneratedLayer and place these elements on the specified PPLayer.
    """
    from spira.yevon.gdsii.polygon import Polygon

    generated_layers = mapping.keys()
    export_layers = mapping.values()
    elems = ElementalList()
    for generated_layer, export_layer in zip(generated_layers, export_layers):
        pg = _generated_elementals(elems=elements, generated_layer=generated_layer)
        # print(pg.elementals[0].points)
        for p in pg.elementals:
            elems += Polygon(shape=p.shape, layer=export_layer)
    return elems

