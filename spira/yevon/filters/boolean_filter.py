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
        from spira.yevon.gdsii.cell import Cell

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

        cell = Cell(elementals=elems, ports=ports)
        return cell
        # return [cell] # FIXME: I think I have to return a list?

    def __repr__(self):
        return "<ProcessBooleanFilter: \'{}\'>".format(self.name)


class SimplifyFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        from spira.yevon.utils import clipping
        from spira.yevon.gdsii.cell import Cell

        ports = PortList()
        elems = ElementalList()

        for e in item.elementals.polygons:
            points = clipping.simplify_points(e.points)
            elems += e.__class__(shape=points, layer=e.layer, transformation=e.transformation)

        for e in item.elementals.sref:
            elems += e
        for e in item.elementals.labels:
            elems += e
        for p in item.ports:
            ports += p

        cell = Cell(elementals=elems, ports=ports)
        return cell

        # elems = ElementalList()
        # for e in item.elementals.polygons:
        #     points = clipping.simplify_points(e.points)
        #     elems += e.__class__(shape=points, layer=e.layer, transformation=e.transformation)
        # return item.__class__(elementals=elems)

    def __repr__(self):
        return "<SimplifyFilter: \'{}\'>".format(self.name)


class ViaConnectFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        from spira.yevon.gdsii.cell import Cell
        from spira.yevon.utils import clipping
        from spira.yevon.vmodel.virtual import virtual_connect
        from shapely.geometry import Polygon as ShapelyPolygon

        ports = PortList()
        elems = ElementalList()

        v_model = virtual_connect(device=item)
        for e in v_model.connected_elementals:
            elems += e

        for e in item.elementals.sref:
            elems += e
        for e in item.elementals.labels:
            elems += e
        for p in item.ports:
            ports += p

        cell = Cell(elementals=elems, ports=ports)
        return cell
        # return item.__class__(elementals=elems)
        # return [cell]

    def __repr__(self):
        return "<ViaConnectFilter: \'{}\'>".format(self.name)


class MetalConnectFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        from copy import deepcopy
        from spira.yevon.vmodel.virtual import virtual_connect
        from spira.yevon.geometry.shapes.modifiers import ShapeConnected
        from spira.yevon.geometry.shapes.shape import Shape

        D = item.expand_flatcopy()
        v_model = virtual_connect(device=D)

        for i, e1 in enumerate(D.elementals):
            points = []
            for e2 in D.elementals:
                e1 = deepcopy(e1)
                e2 = deepcopy(e2)
                if e1 != e2:
                    overlap_shape = e1.shape.intersections(e2.shape)
                    print(overlap_shape)
                    if isinstance(overlap_shape, Shape):
                        if len(overlap_shape) > 2:
                            points.extend(overlap_shape.points.tolist())
            # print('[--] Overlapping shape points:')
            # print(points)
        
            D.elementals[i].shape = ShapeConnected(original_shape=e1.shape, overlapping_shape=Shape(points), edges=v_model.connected_edges)
        return item
        

        # D = item.expand_flatcopy()
        # v_model = virtual_connect(device=D)
        # for i, p in enumerate(D.elementals):
        #     p.shape = ShapeConnected(original_shape=p.shape, edges=v_model.connected_edges)
        # return item
        
    def __repr__(self):
        return "<MetalConnectFilter: \'{}\'>".format(self.name)


