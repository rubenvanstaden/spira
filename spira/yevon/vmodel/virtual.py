import spira.all as spira

from copy import deepcopy
from spira.yevon import filters
from spira.yevon import constants
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
    """  """

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
                # mapping[RDD.PLAYER[k].CLAYER_M1] = RDD.VIAS[k].LAYER_STACK['BOT_LAYER']
                # mapping[RDD.PLAYER[k].CLAYER_M2] = RDD.VIAS[k].LAYER_STACK['TOP_LAYER']

            # print('\nMapping:')
            # for k, v in mapping.items():
            #     print(k, v)
            # print('')
            # print(self.device.elements)

            # print(deepcopy(self.device).elements)

            el = get_derived_elements(elements=deepcopy(self.device).elements, mapping=mapping)
            # el = get_derived_elements(elements=self.device.elements, mapping=mapping)
            for e in el:
                if e.purpose in ['JJ', 'VIA']:
                    elems += e
        else:
            pass
        return elems

    def create_connected_elements(self):
        """ Adds contact ports to each metal polygon connected by a
        contact layer and return a list of the updated elements. """
        index = 0
        for e1 in self.__make_polygons__():
            for e2 in self.device.elements:
                for m in ['BOT_LAYER', 'TOP_LAYER']:
                    if e2.layer == RDD.VIAS[e1.process].LAYER_STACK[m]:
                        if e2.encloses(e1.center):
                            e2.ports += spira.Port(
                                name='Cv_{}'.format(e1.process),
                                midpoint=e1.center,
                                process=e1.layer.process)
                            index += 1
        return self.device.elements

    def _map_derived_edges(self):
        """ Map the derived edge layers in the RDD to a physical layer. """
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
        return mapping

    def _connect_overlap_edges(self, D, edges, overlap_edges):
        """ Connect edges to the overlapping polygon. """
        for j, e in enumerate(D.overlap_elements):
            overlap_edges[e] = []
            for i, edge in enumerate(edges):
                if len(edge.shape.intersections(e.shape)) != 0:
                    edge.external_pid = e.id_string()
                    edge.layer.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
                    overlap_edges[e].append(edge)
        return overlap_edges

    def _connect_boundary_edges(self, D, edges, overlap_edges):
        """ Connect the edges that falls on a shape boudnary,
        since there is no overlapping polygon in this case. """
        for i, edge in enumerate(edges):
            if edge.layer.purpose == RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED:
                c_edge = deepcopy(edge)
                edge.external_pid = edge.id_string()
                edge.layer.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
                overlap_edges[c_edge] = [edge]

    def create_connected_edges(self):
        """  """
        from spira.yevon.gdsii.elem_list import ElementList
        from spira.yevon.vmodel.derived import get_derived_elements

        EF = filters.EdgeFilter(edge_type=constants.EDGE_TYPE_OUTSIDE)
        el = EF(self.device).elements

        mapping = self._map_derived_edges()
        edges = get_derived_elements(elements=el, mapping=mapping, store_as_edge=True)

        overlap_edges = {}
        self._connect_overlap_edges(self.device, edges, overlap_edges)
        self._connect_boundary_edges(self.device, edges, overlap_edges)

        return overlap_edges

    def gdsii_output_virtual_connect(self, **kwargs):

        elems = spira.ElementList()

        # elems += self.device.elements

        # for e in self.__make_polygons__():
        #     elems += e

        for ply_overlap, edges in self.connected_edges.items():
            if ply_overlap.is_empty() is False:
                elems += ply_overlap

        elems += self.device.elements

        # for e in self.device.elements:
        #     elems += e

        D = spira.Cell(name='_VIRTUAL_CONNECT', elements=elems)
        D.gdsii_output()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)


def virtual_connect(device):
    # D = deepcopy(device)
    D = deepcopy(device).expand_flat_copy()
    # D = device
    # D = device.expand_flat_copy()
    return VirtualConnect(device=D)

