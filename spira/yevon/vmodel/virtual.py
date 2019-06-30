import spira.all as spira

from spira.log import SPIRA_LOG as LOG
from spira.yevon.vmodel.derived import get_derived_elements
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.vmodel.geometry import GmshGeometry
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'VirtualProcessModel',
    'virtual_process_model',
    'virtual_connect'
]


class __VirtualModel__(ParameterInitializer):

    device = spira.CellParameter(doc='The device from which a virtual model will be constructed.')
    geometry = spira.Parameter(fdef_name='create_geometry')
    process_flow = spira.VModelProcessFlowParameter()


class VirtualProcessModel(__VirtualModel__):

    def create_geometry(self):
        process_geom = {}
        for pg in self.device.process_elements:
            if RDD.ENGINE.GEOMETRY == 'GMSH_ENGINE':
                process_geom[pg.process] = GmshGeometry(process=pg.process, process_polygons=pg.elements)
            else:
                raise ValueError('Geometry engine type not specificied in RDD.')
        return process_geom


class VirtualConnect(__VirtualModel__):

    # FIXME: Add a string list restriction.
    connect_type = spira.StringParameter(default='contact_layer')
    connected_edges = spira.DictParameter(fdef_name='create_connected_edges')
    connected_elements = spira.Parameter(fdef_name='create_connected_elements')

    def __make_polygons__(self):

        elems = spira.ElementList()
        if self.connect_type == 'contact_layer':

            mapping = {}
            for k in RDD.VIAS.keys:
                mapping[RDD.PLAYER[k].CLAYER_CONTACT] = RDD.VIAS[k].LAYER_STACK['VIA_LAYER']
                mapping[RDD.PLAYER[k].CLAYER_M1] = RDD.VIAS[k].LAYER_STACK['BOT_LAYER']
                mapping[RDD.PLAYER[k].CLAYER_M2] = RDD.VIAS[k].LAYER_STACK['TOP_LAYER']

            # print('\nMapping:')
            # for k, v in mapping.items():
            #     print(k, v)
            # print('')
            # print(self.device.elements)

            el = get_derived_elements(elements=self.device.elements, mapping=mapping)
            for e in el:
                if e.purpose == 'METAL':
                    pass
                else:
                    elems += e
        else:
            pass
            # # D = self.device.expand_flatcopy()
            # D = self.device.expand_flat_no_jjcopy()

            # elems = spira.ElementList()
            # for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
            #     for layer in RDD.get_physical_layers_by_process(processes=process):
            #         LF = LayerFilterAllow(layers=[layer])
            #         el = LF(D.elements.polygons)
            #         elems += spira.PolygonGroup(elements=el, layer=layer).intersect
        return elems

    def create_connected_elements(self):
        """ Adds contact ports to each metal polygon connected by a 
        contact layer and return a list of the updated elements. """
        for e1 in self.__make_polygons__():
            for e2 in self.device.elements:
                for m in ['BOT_LAYER', 'TOP_LAYER']:
                    if e2.layer == RDD.VIAS[e1.process].LAYER_STACK[m]:
                        if e2.encloses(e1.center):
                            e2.ports += spira.Port(
                                name=e1.process,
                                midpoint=e1.center,
                                process=e1.layer.process,
                                purpose=e1.layer.purpose,
                                port_type='contact')
        return self.device.elements

    def create_connected_edges(self):
        from copy import deepcopy
        from spira.yevon.gdsii.elem_list import ElementList
        from spira.yevon.vmodel.derived import get_derived_elements
        el = ElementList()
        for p1 in deepcopy(self.device.elements):
            if p1.layer.purpose == RDD.PURPOSE.METAL:
                el += p1
                for edge in p1.edges:
                    el += edge.outside.transform(edge.transformation)

        # FIXME !!!
        # map1 = {RDD.PLAYER.M2.EDGE_CONNECTED : RDD.PLAYER.M2.INSIDE_EDGE_ENABLED}
        mapping = {}
        for pl in RDD.get_physical_layers_by_purpose(purposes=['METAL']):
            key = pl.process.symbol
            if hasattr(RDD.PLAYER[key], 'EDGE_CONNECTED'):
                derived_layer = RDD.PLAYER[key].EDGE_CONNECTED
                ps_1 = derived_layer.layer1.process.symbol
                ps_2 = derived_layer.layer2.process.symbol
                if ps_1 == ps_2:
                    mapping[derived_layer] = RDD.PLAYER[key].OUTSIDE_EDGE_DISABLED
                else:
                    es = "Error in RDD: Edge process \'{}\' not the same as metal process \'{}\'."
                    raise ValueError(es.format(ps_2, ps_1))
            else:
                LOG.warning('Edge detection for METAL layer {} ignored.'.format(key))

        pg_overlap = self.device.overlap_elements
        edges = get_derived_elements(el, mapping=mapping, store_as_edge=True)

        overlap_edges = {}

        # print(pg_overlap)
        # print(edges)
        # print('----------------')

        for j, pg in enumerate(pg_overlap):
            for e in pg.elements:
                overlap_edges[e] = []
                for i, edge in enumerate(edges):
                    if len(edge.outside.shape.intersections(e.shape)) != 0:
                        edges[i].pid = '{}'.format(e.shape.hash_string)
                        edges[i].outside.layer.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
                        overlap_edges[e].append(edges[i])

                        # edge.pid = '{}'.format(e.shape.hash_string)
                        # edge.elements[0].layer.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
                        # overlap_edges[e].append(edge)

        # print('----------------')
        # print(edges)

        # NOTE: To detect single edges that 
        # falls on shape boundary edges.
        if len(edges) > 0:
            e = spira.Polygon(alias='Dummy', shape=[], layer=RDD.PLAYER.METAL)
            overlap_edges[e] = []
            for i, edge in enumerate(edges):
                if edge.outside.layer.purpose == RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED:
                    edge.pid = '{}'.format(e.shape.hash_string)
                    edge.outside.layer.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
                    overlap_edges[e].append(edge)

        return overlap_edges

    def gdsii_output_virtual_connect(self, **kwargs):

        elems = spira.ElementList()

        # for e in self.__make_polygons__():
        #     elems += e

        for ply_overlap, edges in self.connected_edges.items():
            if len(ply_overlap.points) > 0:
                elems += ply_overlap
            for e in edges:
                # elems += e.outside
                elems += e.elements[0]

        for e in self.device.elements:
            elems += e

        D = spira.Cell(name='_VIRTUAL_CONNECT', elements=elems)
        D.gdsii_output()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)


def virtual_connect(device):
    return VirtualConnect(device=device)

