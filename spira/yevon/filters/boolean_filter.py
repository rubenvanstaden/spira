from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.geometry.ports.port_list import PortList


__all__ = [
    'ProcessBooleanFilter',
    'SimplifyFilter',
    'ViaConnectFilter',
    'MetalConnectFilter'
]


class ProcessBooleanFilter(Filter):
    """  """

    def filter___Cell__(self, item):
        from spira.yevon.gdsii.cell import Cell

        ports = PortList()
        elems = ElementList()

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

    def filter___Cell__(self, item):
        from spira.yevon.utils import clipping
        from spira.yevon.gdsii.cell import Cell

        ports = PortList()
        elems = ElementList()

        for e in item.elements.polygons:
            e.shape = clipping.simplify_points(e.points)
            elems += e

        for e in item.elements.sref:
            elems += e
        for e in item.elements.labels:
            elems += e
        for p in item.ports:
            ports += p

        cell = Cell(elements=elems, ports=ports)
        # cell = item.__class__(elements=elems, ports=ports)
        return cell

    def __repr__(self):
        return "<SimplifyFilter: \'{}\'>".format(self.name)


class MetalConnectFilter(Filter):
    """  """

    def filter___Cell__(self, item):
        from copy import deepcopy
        from spira.yevon.vmodel.virtual import virtual_connect
        from spira.yevon.geometry.shapes.adapters import ShapeConnected
        from spira.yevon.geometry.shapes.shape import Shape

        v_model = virtual_connect(device=item)

        D = item.expand_flat_copy()

        for i, e1 in enumerate(D.elements):
            clip_shape = Shape()
            for e2 in D.elements:
                shape1 = e1.shape.transform_copy(e1.transformation).snap_to_grid()
                shape2 = e2.shape.transform_copy(e2.transformation).snap_to_grid()
                if (shape1 != shape2) and (e1.layer == e2.layer):
                    overlap_shape = shape1.intersections(shape2)
                    if isinstance(overlap_shape, Shape):
                        if overlap_shape.is_empty() is False:
                            clip_shape.extend(overlap_shape.points.tolist())

            if clip_shape.is_empty() is False:
                original_shape = e1.shape.transform_copy(e1.transformation).snap_to_grid()
                D.elements[i].shape = ShapeConnected(
                    original_shape=original_shape,
                    clip_shape=clip_shape,
                    edges=v_model.connected_edges)
                D.elements[i].ports = D.elements[i].ports.transform_copy(e1.transformation)
                D.elements[i].transformation = None

        return item

    def __repr__(self):
        return "<MetalConnectFilter: \'{}\'>".format(self.name)


class ViaConnectFilter(Filter):
    """  """

    def filter___Cell__(self, item):
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

        # item.elements = elems
        # item.ports = ports
        # return item
        cell = Cell(elements=elems, ports=ports)
        return cell
        # return item.__class__(elements=elems)
        # return [cell]

    def __repr__(self):
        return "<ViaConnectFilter: \'{}\'>".format(self.name)


