from copy import deepcopy
from spira.core.parameters.descriptor import DataField
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.cell import Cell
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.gdsii.containers import __CellContainer__
from spira.yevon.vmodel.derived import get_derived_elementals
from spira.yevon.geometry.shapes.modifiers import ShapeConnected
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['MutualConnection', 'ElectricalConnection']


class __Connection__(__CellContainer__):
    """ Base class for establishing current connections. """
    pass


class MutualConnection(__Connection__):
    """ Mutual coupling connection between different inductive branches. """
    pass


class ElectricalConnections(__Connection__):
    """

    """

    edges = DataField(fdef_name='create_edges')

    def create_elementals(self, elems):
        overlap_elems, edges = self.edges
        # for p in self.cell.elementals:
        for i, p in enumerate(self.cell.elementals):
            
            # shape = deepcopy(p.shape).transform(p.transformation).snap_to_grid()
            # cs = ShapeConnected(original_shape=shape, edges=edges)
            # elems += Polygon(shape=cs, layer=p.layer)
            
            # cs = ShapeConnected(original_shape=shape, edges=edges)
            # # p.shape = cs
            # self.cell.elementals[i].shape = cs

            if i == 2:
                shape = deepcopy(p.shape).transform(p.transformation).snap_to_grid()
                # shape = p.shape
                # print(shape.points)
                cs = ShapeConnected(original_shape=shape, edges=edges)
                # print(cs.points)
                # self.cell.elementals[i].shape = cs
                p.shape = cs
                # elems += Polygon(shape=cs, layer=p.layer)
                # elems += p

        return elems

    def create_edges(self):
        el = ElementalList()
        for p1 in deepcopy(self.cell.elementals):
            el += p1
            for edge in p1.edges:
                el += edge.outside.transform(edge.transformation)

        map1 = {RDD.PLAYER.M5.EDGE_CONNECTED : RDD.PLAYER.M5.INSIDE_EDGE_ENABLED}

        pg_overlap = self.cell.overlap_elementals
        edges = get_derived_elementals(el, mapping=map1, store_as_edge=True)

        for j, pg in enumerate(pg_overlap):
            for e in pg.elementals:
                for i, edge in enumerate(edges):
                    if edge.overlaps(e):
                        # FIXME: Cannot use this, since Gmsh seems to crach due to the hashing string.
                        # edges[i].pid = p.id_string()
                        # edges[i].pid = '{}_{}'.format(p.__repr__(), p.uid)
                        edges[i].pid = '{}'.format(e.shape.hash_string)

        return pg_overlap, edges

    def gdsii_output_electrical_connection(self):

        elems = ElementalList()
        overlap_elems, edges = self.edges
        for e in overlap_elems:
            elems += e
        for edge in edges:
            elems += edge.outside
        for e in self.cell.elementals:
            elems += e

        D = Cell(name='_ELECTRICAL_CONNECT', elementals=elems)
        D.gdsii_output()


