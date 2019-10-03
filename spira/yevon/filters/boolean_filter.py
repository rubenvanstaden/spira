from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.geometry.ports.port_list import PortList
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'ProcessBooleanFilter',
    'SimplifyFilter',
    'ElectricalAttachFilter',
    'ContactAttachFilter',
    'PinAttachFilter',
]


# FIXME: Maybe use derived layers directly?
class ProcessBooleanFilter(Filter):
    """
    Applies boolean merge operations on all metal
    layer polygons in the cell.

    Notes
    -----
    Derived merge boolean polygons is added as a filter, 
    since we want to apply this operation on all elements.
    """
    from spira.yevon.process.purpose_layer import PurposeLayerParameter

    metal_purpose = PurposeLayerParameter(default=RDD.PURPOSE.METAL)

    def filter_Cell(self, item):
        from spira.yevon.gdsii.cell import Cell

        ports = PortList()
        elems = ElementList()

        for e in item.derived_merged_elements:
            elems += e
        for e in item.elements.sref:
            elems += e
        for e in item.elements.labels:
            elems += e
        for p in item.ports:
            if p.purpose.symbol == 'P':
                ports += p
            if p.purpose.symbol == 'T':
                ports += p

        cell = Cell(elements=elems, ports=ports)
        return cell

    def __repr__(self):
        return "<ProcessBooleanFilter: \'{}\'>".format(self.name)


class SimplifyFilter(Filter):
    """ 
    Simplify all curved shapes in the cell.
    
    Notes
    -----
    Add shape simplifying algorithm as a filter, since
    we only want to apply shape simplification is certain
    circumstances. Other shape operations, such as
    reversing points are typically applied algorithmically.
    """

    def filter_Cell(self, item):
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
        return cell

    def __repr__(self):
        return "<SimplifyFilter: \'{}\'>".format(self.name)


class ElectricalAttachFilter(Filter):
    """
    
    """

    def filter_Cell(self, item):
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
                    derived_edges=v_model.derived_edges)
                D.elements[i].ports = D.elements[i].ports.transform_copy(e1.transformation)
                D.elements[i].transformation = None

        return item

    def __repr__(self):
        return "<ElectricalAttachFilter: \'{}\'>".format(self.name)


class ContactAttachFilter(Filter):
    """
    Adds contact ports to each metal polygon connected by a
    contact layer and return a list of the updated elements.
    """

    def filter_Cell(self, item):
        from spira.yevon.utils import clipping
        from spira.yevon.gdsii.cell import Cell
        from spira.yevon.geometry.ports import Port
        from spira.yevon.vmodel.virtual import virtual_connect
        from shapely.geometry import Polygon as ShapelyPolygon

        # ports = PortList()
        elems = ElementList()

        v_model = virtual_connect(device=item)

        for e1 in v_model.derived_contacts:
            ps = e1.layer.process.symbol
            for e2 in item.elements:
                for m in ['BOT_LAYER', 'TOP_LAYER']:
                    if ps in RDD.VIAS.keys:
                        if e2.layer == RDD.VIAS[ps].LAYER_STACK[m]:
                            if e2.encloses(e1.center):
                                port = Port(
                                    name='{}:Cv'.format(ps),
                                    midpoint=e1.center,
                                    process=e1.layer.process)
                                e2.ports += port
        elems += item.elements

        for e in item.elements.sref:
            elems += e
        for e in item.elements.labels:
            elems += e
        # for p in item.ports:
        #     ports += p

        # cell = Cell(elements=elems, ports=ports)
        cell = Cell(elements=elems)
        return cell

    def __repr__(self):
        return "<ContactAttachFilter: \'{}\'>".format(self.name)


class PinAttachFilter(Filter):
    """
    Adds contact ports to each metal polygon connected by a
    contact layer and return a list of the updated elements.
    """

    def filter_Cell(self, item):

        D = item.expand_flat_copy()

        for e in D.elements.polygons:
            for p in item.ports:
                # if p.purpose.symbol == 'P':
                if p.purpose.symbol == 'T':

                    # if p.encloses(e.shape.points):
                    #     e.ports += p

                    # c_port= p.transform_copy(e.transformation)
                    shape = e.shape.transform_copy(e.transformation).snap_to_grid()
                    if p.encloses(shape.points):
                        e.ports += p

        return item

        # for e in item.elements.sref:
        #     elems += e
        # for e in item.elements.labels:
        #     elems += e

        # # cell = Cell(elements=elems, ports=ports)
        # cell = Cell(elements=elems)
        # return cell

    def __repr__(self):
        return "<ContactAttachFilter: \'{}\'>".format(self.name)



