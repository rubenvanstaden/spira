from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.geometry.ports.port_list import PortList
# from spira.yevon.geometry.edges.edge_list import EdgeListField


__all__ = [
    'ProcessBooleanFilter',
    'SimplifyFilter',
    'ViaConnectFilter',
    'MetalConnectFilter'
]


class ProcessBooleanFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        ports = PortList()
        elems = ElementalList()
        for pg in item.process_elementals:
            for e in pg.elementals:
                elems += e
        for e in item.elementals.sref:
            elems += e
        for e in item.elementals.labels:
            elems += e
        for p in item.ports:
            ports += p
        return item.__class__(elementals=elems, ports=ports)

    def __repr__(self):
        return "<ProcessBooleanFilter: \'{}\'>".format(self.name)


class SimplifyFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        from spira.yevon.utils import clipping
        from shapely.geometry import Polygon as ShapelyPolygon

        elems = ElementalList()
        for e in item.elementals.polygons:
            points = clipping.simplify_points(e.points)
            elems += e.__class__(shape=points, layer=e.layer, transformation=e.transformation)
        return item.__class__(elementals=elems)

    def __repr__(self):
        return "<SimplifyFilter: \'{}\'>".format(self.name)


class ViaConnectFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        from spira.yevon.utils import clipping
        from spira.yevon.vmodel.virtual import virtual_connect
        from shapely.geometry import Polygon as ShapelyPolygon

        elems = ElementalList()
        v_model = virtual_connect(device=item)
        for e in v_model.connected_elementals:
            elems += e
        return item.__class__(elementals=elems)

    def __repr__(self):
        return "<ViaConnectFilter: \'{}\'>".format(self.name)


class MetalConnectFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        from spira.yevon.vmodel.virtual import virtual_connect
        from spira.yevon.geometry.shapes.modifiers import ShapeConnected

        D = item.expand_flat_copy()
        v_model = virtual_connect(device=D)
        for i, p in enumerate(D.elementals):
            p.shape = ShapeConnected(original_shape=p.shape, edges=v_model.connected_edges)
        return item
        
    def __repr__(self):
        return "<ViaConnectFilter: \'{}\'>".format(self.name)


