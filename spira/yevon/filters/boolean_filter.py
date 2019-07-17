from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.geometry.ports.port_list import PortList
# from spira.yevon.geometry.edges.edge_list import EdgeListParameter


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
        elems = ElementList()

        # for pg in item.process_elements:
            # for e in pg.elements:
                # elems += e

        for e in item.process_elements:
            elems += e
        for e in item.elements.sref:
            elems += e
        for e in item.elements.labels:
            elems += e
        for p in item.ports:
            ports += p

        cell = Cell(elements=elems, ports=ports)
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
        elems = ElementList()

        for e in item.elements.polygons:
            e.shape = clipping.simplify_points(e.points)
            elems += e

            # points = clipping.simplify_points(e.points)
            # elems += e.copy(shape=points)

            # p = e.__class__(shape=points, layer=e.layer, transformation=e.transformation)
            # elems += e.__class__(shape=points, layer=e.layer, transformation=e.transformation)

        for e in item.elements.sref:
            elems += e
        for e in item.elements.labels:
            elems += e
        for p in item.ports:
            ports += p

        cell = Cell(elements=elems, ports=ports)
        # cell = item.__class__(elements=elems, ports=ports)
        return cell

        # elems = ElementList()
        # for e in item.elements.polygons:
        #     points = clipping.simplify_points(e.points)
        #     elems += e.__class__(shape=points, layer=e.layer, transformation=e.transformation)
        # return item.__class__(elements=elems)

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
        elems = ElementList()

        v_model = virtual_connect(device=item)
        for e in v_model.connected_elements:
            elems += e

        for e in item.elements.sref:
            elems += e
        for e in item.elements.labels:
            elems += e
        for p in item.ports:
            ports += p

        cell = Cell(elements=elems, ports=ports)
        return cell
        # return item.__class__(elements=elems)
        # return [cell]

    def __repr__(self):
        return "<ViaConnectFilter: \'{}\'>".format(self.name)


class MetalConnectFilter(Filter):
    """  """

    def __filter___Cell____(self, item):
        from copy import deepcopy
        from spira.yevon.vmodel.virtual import virtual_connect
        from spira.yevon.geometry.shapes.adapters import ShapeConnected
        from spira.yevon.geometry.shapes.shape import Shape

        D = item.expand_flat_copy()
        v_model = virtual_connect(device=D)

        for i, e1 in enumerate(D.elements):
            points = []
            # print('E1: {}'.format(e1))
            for e2 in D.elements:
                shape1 = deepcopy(e1).shape.transform(e1.transformation)
                shape2 = deepcopy(e2).shape.transform(e2.transformation)
                if (shape1 != shape2) and (e1.layer == e2.layer):
                    # print('E2: {}'.format(e2))
                    overlap_shape = shape1.intersections(shape2)
                    # print(overlap_shape.points)
                    if isinstance(overlap_shape, Shape):
                        if len(overlap_shape) > 0:
                            # print('YESSSS')
                            points.extend(overlap_shape.points.tolist())

            if len(points) > 0:
                # print('[--] Overlapping shape points:')
                # print(points)
                D.elements[i].shape = ShapeConnected(
                    original_shape=e1.shape,
                    overlapping_shape=Shape(points),
                    edges=v_model.connected_edges
                )
            # print('')

        return item

    def __repr__(self):
        return "<MetalConnectFilter: \'{}\'>".format(self.name)


