import numpy as np
import spira.all as spira

from copy import deepcopy
from spira.yevon import constants
from spira.yevon.geometry import shapes
from spira.yevon.gdsii.elem_list import ElementalList, ElementalListField
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.descriptor import DataField
from spira.yevon.geometry.ports.port_list import PortList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.utils import clipping
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.yevon.structure.edges import Edge
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

    if isinstance(generated_layer, Layer):
        LF = LayerFilterAllow(layers=[generated_layer])
        el = LF(elems.polygons)
        # pg = spira.PolygonGroup(elementals=el, layer=generated_layer).merge
        pg = spira.PolygonGroup(elementals=el, layer=generated_layer)
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


def get_generated_elementals(elements, mapping, store_as_edge=False):
    """
    Given a list of elements and a list of tuples (GeneratedLayer, PPLayer), create new elements according to the boolean
    operations of the GeneratedLayer and place these elements on the specified PPLayer.
    """
    generated_layers = mapping.keys()
    export_layers = mapping.values()
    elems = ElementalList()
    for generated_layer, export_layer in zip(generated_layers, export_layers):
        pg = _generated_elementals(elems=elements, generated_layer=generated_layer)
        for p in pg.elementals:
            ply = spira.Polygon(shape=p.shape, layer=export_layer)
            if store_as_edge is True:
                elems += Edge(outside=ply, layer=export_layer)
            else: elems += ply
    return elems


def get_overlaping_metals(elements):
    elems = spira.ElementalList()
    for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
        for layer in RDD.get_physical_layers_by_process(processes=process):
            LF = LayerFilterAllow(layers=[layer])
            el = LF(elements.polygons)
            pg = spira.PolygonGroup(elementals=el, layer=layer).intersect
            elems += pg.elementals
    return elems


# --------------------------------- Derived Edges ------------------------------------


from spira.yevon.utils import clipping
from spira.yevon.vmodel.geometry import GmshGeometry
from spira.yevon.geometry.ports.port_list import PortList
from spira.yevon.structure.containers import __CellContainer__
from spira.yevon.geometry.shapes.modifiers import ShapeConnected

class ElectricalConnections(__CellContainer__):
    """

    """

    edges = DataField(fdef_name='create_edges')
    geometry = DataField(fdef_name='create_geometry')
    connected_elementals = ElementalListField()

    def create_elementals(self, elems):
        overlap_elems, edges = self.edges
        # elems += el_edges
        elems += overlap_elems
        return elems

    def create_edges(self):
        el = spira.ElementalList()
        for p1 in deepcopy(self.cell.elementals):
            el += p1
            for edge in p1.edges:
                el += edge.outside.transform(edge.transformation)

        map1 = {RDD.PLAYER.M5.EDGE_CONNECTED : RDD.PLAYER.M5.EDGE_PORT_ENABLED}

        overlap_elems = get_overlaping_metals(self.cell.elementals)
        edges = get_generated_elementals(el, mapping=map1, store_as_edge=True)

        for j, p in enumerate(overlap_elems):
            for i, edge in enumerate(edges):
                if edge.overlaps(p):
                    # FIXME: Cannot use this, since Gmsh seems to crach due to the hashing string.
                    # edges[i].pid = p.id_string()
                    # edges[i].pid = '{}_{}'.format(p.__repr__(), p.uid)
                    edges[i].pid = '{}'.format(p.shape.hash_string)

        return overlap_elems, edges

    def create_connected_elementals(self, elems):
        overlap_elems, edges = self.edges
        # for p in self.cell.elementals:
        for i, p in enumerate(self.cell.elementals):
            if i == 1:
                shape = deepcopy(p.shape).transform(p.transformation).snap_to_grid()
                cs = ShapeConnected(original_shape=shape, edges=edges)
                elems += spira.Polygon(shape=cs, layer=p.layer)
        return elems

    # def create_geometry(self):

    #     for i, ply in enumerate(self.connected_elementals):
    #         geom = GmshGeometry(filename=str(i), process_polygons=[ply], process=RDD.PROCESS.M6)
    #         geom.mesh_data
    #         print(ply.nets())

    def gdsii_output_electrical_connection(self):

        elems = spira.ElementalList()
        # for e in self.__make_polygons__():
        overlap_elems, edges = self.edges
        for e in overlap_elems:
            elems += e
        for edge in edges:
            # elems += edge.outside.transform(edge.transformation)
            elems += edge.outside
        for e in self.cell.elementals:
            elems += e

        D = spira.Cell(name='_ELECTRICAL_CONNECT', elementals=elems)
        D.gdsii_output()


    # elems = ElementalList()

    # for i, p1 in enumerate(elementals):
    #     if i == 0:
    #         new_shape = deepcopy(p1.shape).transform(p1.transformation).snap_to_grid()
    #         for p2 in elementals:
    #             if p1.shape != p2.shape:
                    
    #                 for edge in p1.edges:
            
    #                     outside_edge = edge.outside.transform(edge.transformation)
                        
    #                     for p in outside_edge.intersection(p2):
    #                         elems += p
                            
    #                         for i, s in enumerate(new_shape.segments):
    #                             line = line_from_two_points(s[0], s[1])
    #                             for c in p.bbox_info.bounding_box().snap_to_grid():
    #                                 if line.is_on_line(coordinate=c):
    #                                     if c not in new_shape:
    #                                         new_shape.insert(i=i+1, item=c)
    
    #                 # ec = ElectricalConnections(polyA=deepcopy(p1), polyB=deepcopy(p2))
    #                 # elems = ec.get_A_edge_from_B_region()
                    
    #         ply = spira.Polygon(shape=new_shape.clockwise(), layer=RDD.PLAYER.M6.METAL)
    #         # print(ply.nets())

    #         geom = GmshGeometry(process_polygons=[ply], process=RDD.PROCESS.M6)
    #         geom.mesh_data

    # elems += elementals

    # return elems


def old_derived_edges(elementals):

    elems = ElementalList()

    for i, p1 in enumerate(elementals):
        if i == 0:
            new_shape = deepcopy(p1.shape).transform(p1.transformation).snap_to_grid()
            for p2 in elementals:
                if p1.shape != p2.shape:
                    
                    for edge in p1.edges:
            
                        outside_edge = edge.outside.transform(edge.transformation)

                        for p in outside_edge.intersection(p2):
                            elems += p
                            
                            for i, s in enumerate(new_shape.segments):
                                line = line_from_two_points(s[0], s[1])
                                for c in p.bbox_info.bounding_box().snap_to_grid():
                                    if line.is_on_line(coordinate=c):
                                        if c not in new_shape:
                                            new_shape.insert(i=i+1, item=c)
    
                    # ec = ElectricalConnections(polyA=deepcopy(p1), polyB=deepcopy(p2))
                    # elems = ec.get_A_edge_from_B_region()
                    
            ply = spira.Polygon(shape=new_shape.clockwise(), layer=RDD.PLAYER.M6.METAL)
            # print(ply.nets())

            geom = GmshGeometry(process_polygons=[ply], process=RDD.PROCESS.M6)
            geom.mesh_data

    elems += elementals

    return elems


def get_derived_edges(elementals, mapping):

    generated_layers = mapping.keys()
    export_layers = mapping.values()
    elems = ElementalList()
    for generated_layer, export_layer in zip(generated_layers, export_layers):

        for i, subj_polygon in enumerate(elementals):
            if i == 0:
                subj_polygon = deepcopy(subj_polygon)

                edges = subj_polygon.edges
                new_shape = deepcopy(subj_polygon.shape).transform(subj_polygon.transformation).snap_to_grid()

                for clip_polygon in elementals:
                    if subj_polygon.shape != clip_polygon.shape:
                        cp = deepcopy(clip_polygon)
                        offset_layer = RDD.GDSII.IMPORT_LAYER_MAP[cp.layer]
                        offset_layer.purpose = RDD.PURPOSE.ROUTE
                        e3 = spira.Polygon(shape=cp.points, layer=offset_layer)
                        elems += e3
    
                        # TODO: Make me a derived layer.
                        layer = spira.Layer(number=i)

                        # pg_edges = spira.PolygonGroup(elementals=edges, layer=layer)
                        pg_external = spira.PolygonGroup(elementals=[e3], layer=cp.layer)

                        for edge in edges:
                            outside_edge = edge.outside.transform(edge.transformation)
                            pg_edge = spira.PolygonGroup(elementals=[outside_edge], layer=layer)

                            polygons = pg_edge & pg_external
                            for p in polygons: elems += p
                            for p in polygons:
                                for i, s in enumerate(new_shape.segments):
                                    print('segment: ({} {})'.format(s[0], s[1]))
                                    line = line_from_two_points(s[0], s[1])
                                    for c in p.bbox_info.bounding_box().snap_to_grid():
                                        if line.is_on_line(coordinate=c):
                                            if c not in new_shape:
                                                new_shape.insert(i=i+1, item=c)

                ply = spira.Polygon(shape=new_shape.clockwise(), layer=RDD.PLAYER.M6.METAL)

                # print(ply.nets())

                geom = GmshGeometry(process_polygons=[ply], process=RDD.PROCESS.M6)
                geom.mesh_data

    elems += elementals

    return elems


def generate_ports_from_derived_edges():
    pass

