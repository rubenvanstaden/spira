import spira.all as spira

from copy import deepcopy
from spira.yevon import filters
from spira.yevon import constants
from spira.log import SPIRA_LOG as LOG
from spira.yevon.vmodel.derived import get_derived_elements
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.vmodel.geometry import GmshGeometry
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'VirtualProcessModel',
    'VirtualConnect',
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
        for pg in self.device.derived_merged_elements:
            if RDD.ENGINE.GEOMETRY == 'GMSH_ENGINE':
                process_geom[pg.process] = GmshGeometry(process=pg.process, process_polygons=pg.elements)
            else:
                raise ValueError('Geometry engine type not specificied in RDD.')
        return process_geom


class VirtualConnect(__VirtualModel__):
    """  """

    derived_edges = spira.DictParameter(fdef_name='create_derived_edges')
    derived_contacts = spira.Parameter(fdef_name='create_derived_contacts')
    attached_contacts = spira.Parameter(fdef_name='create_attached_contacts')

    def create_derived_contacts(self):
        """  """

        mapping = {}
        for k in RDD.VIAS.keys:
            mapping[RDD.PLAYER[k].CLAYER_CONTACT] = RDD.VIAS[k].LAYER_STACK['VIA_LAYER']
            mapping[RDD.PLAYER[k].CLAYER_M1] = RDD.VIAS[k].LAYER_STACK['BOT_LAYER']
            mapping[RDD.PLAYER[k].CLAYER_M2] = RDD.VIAS[k].LAYER_STACK['TOP_LAYER']

        return get_derived_elements(elements=deepcopy(self.device).elements, mapping=mapping)

    def create_derived_edges(self):
        """ Detect connecting and overlapping layer edges. Returns
        the derived merged polygons and derived intersection edges. """

        purposes = [RDD.PURPOSE.METAL, RDD.PURPOSE.DEVICE_METAL, RDD.PURPOSE.CIRCUIT_METAL]
        EF = filters.EdgeShapeFilter(edge_type=constants.EDGE_TYPE_OUTSIDE, width=0.3, purposes=purposes)
        edge_elems = EF(self.device).elements

        mapping = self._derived_edges_mapping()
        derived_edges = get_derived_elements(elements=edge_elems, mapping=mapping, store_as_edge=True)

        overlap_edges = {}
        self._connect_overlap_edges(self.device, derived_edges, overlap_edges)
        self._connect_boundary_edges(self.device, derived_edges, overlap_edges)

        return overlap_edges

    def _derived_edges_mapping(self):
        """ Map the derived edge layers in the RDD to a physical layer. """
        mapping = {}
        purposes = ['METAL', 'DEVICE_METAL', 'CIRCUIT_METAL']
        for pl in RDD.get_physical_layers_by_purpose(purposes=purposes):
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

    def _connect_overlap_edges(self, D, derived_edges, overlap_edges):
        """ Connect edges to the overlapping polygon. """
        for j, e in enumerate(D.derived_overlap_elements):
            overlap_edges[e] = []
            for i, edge in enumerate(derived_edges):
                if len(edge.shape.intersections(e.shape)) != 0:
                    edge.external_pid = e.id_string()
                    edge.layer.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
                    overlap_edges[e].append(edge)
        return overlap_edges

    def _connect_boundary_edges(self, D, derived_edges, overlap_edges):
        """ Connect the edges that falls on a shape boudnary,
        since there is no overlapping polygon in this case. """
        for i, edge in enumerate(derived_edges):
            if edge.layer.purpose == RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED:
                c_edge = deepcopy(edge)
                edge.external_pid = edge.id_string()
                edge.layer.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
                overlap_edges[c_edge] = [edge]

    def view_virtual_connect(self, show_layers=False, write=False, **kwargs):
        """ View that contains all derived connections (attached contacts, derived edges). """

        elems = spira.ElementList()

        if show_layers is True:
            el = self.derived_contacts
            F = filters.PurposeFilterAllow(purposes=['JJ', 'VIA'])
            elems += F(el)
            elems += self.device.elements
        else:
            elems += self.derived_contacts

        for ply_overlap, edges in self.derived_edges.items():
            if ply_overlap.is_empty() is False:
                for e in edges:
                    EF = filters.EdgeToPolygonFilter()
                    elems += EF(e)
                if not isinstance(ply_overlap, spira.Edge):
                    elems += ply_overlap

        name = self.device.name + '_VConnect'
        D = spira.Cell(name=name, elements=elems, ports=self.device.ports, transformation=self.device.transformation)
        D.gdsii_view()
        if write is True:
            D.gdsii_output(file_name=name)

    def view_derived_contacts(self, show_layers=False, **kwargs):

        elems = spira.ElementList()

        # if show_layers is True:
        #     elems += self.device.elements

        # el = self.derived_contacts
        # F = filters.PurposeFilterAllow(purposes=['JJ', 'VIA'])
        # elems += F(el)

        el = self.derived_contacts

        elems += el

        D = spira.Cell(name='_DERIVED_CONTACTS', elements=elems)
        D.gdsii_view()

    def view_derived_edges(self, show_layers=False, **kwargs):

        elems = spira.ElementList()

        if show_layers is True:
            elems += self.device.elements

        for ply_overlap, edges in self.derived_edges.items():
            if ply_overlap.is_empty() is False:
                for e in edges:
                    EF = filters.EdgeToPolygonFilter()
                    elems += EF(e)

        D = spira.Cell(name='_DERIVED_EDGES', elements=elems)
        D.gdsii_view()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)


def virtual_connect(device):
    D = deepcopy(device).expand_flat_copy()
    return VirtualConnect(device=D)

