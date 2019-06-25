import spira.all as spira

from spira.log import SPIRA_LOG as LOG
from spira.yevon.vmodel.derived import get_derived_elementals
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.core.parameters.initializer import FieldInitializer
from spira.yevon.vmodel.geometry import GmshGeometry
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'VirtualProcessModel',
    'virtual_process_model',
    'virtual_connect'
]


class __VirtualModel__(FieldInitializer):

    device = spira.CellField(doc='The device from which a virtual model will be constructed.')
    geometry = spira.DataField(fdef_name='create_geometry')
    process_flow = spira.VModelProcessFlowField()


class VirtualProcessModel(__VirtualModel__):

    def create_geometry(self):
        process_geom = {}
        for pg in self.device.process_elementals:
            if RDD.ENGINE.GEOMETRY == 'GMSH_ENGINE':
                process_geom[pg.process] = GmshGeometry(process=pg.process, process_polygons=pg.elementals)
            else:
                raise ValueError('Geometry engine type not specificied in RDD.')
        return process_geom


class VirtualConnect(__VirtualModel__):

    # FIXME: Add a string list restriction.
    connect_type = spira.StringField(default='contact_layer')
    connected_edges = spira.DataField(fdef_name='create_connected_edges')
    connected_elementals = spira.DataField(fdef_name='create_connected_elementals')

    def __make_polygons__(self):

        elems = spira.ElementalList()
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
            # print(self.device.elementals)

            el = get_derived_elementals(elements=self.device.elementals, mapping=mapping)
            for e in el:
                if e.purpose == 'METAL': 
                    pass
                else:
                    elems += e
        else:
            pass
            # # D = self.device.expand_flatcopy()
            # D = self.device.expand_flat_no_jjcopy()

            # elems = spira.ElementalList()
            # for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
            #     for layer in RDD.get_physical_layers_by_process(processes=process):
            #         LF = LayerFilterAllow(layers=[layer])
            #         el = LF(D.elementals.polygons)
            #         elems += spira.PolygonGroup(elementals=el, layer=layer).intersect
        return elems

    def create_connected_edges(self):
        from copy import deepcopy
        from spira.yevon.gdsii.elem_list import ElementalList
        from spira.yevon.vmodel.derived import get_derived_elementals
        el = ElementalList()
        for p1 in deepcopy(self.device.elementals):
            if p1.layer.purpose == RDD.PURPOSE.METAL:
                el += p1
                for edge in p1.edges:
                    el += edge.outside.transform(edge.transformation)
                    # el += edge.outside
                    # el += edge
                # print('')

        # FIXME!!!
        # map1 = {RDD.PLAYER.M2.EDGE_CONNECTED : RDD.PLAYER.M2.EDGE_PORT_ENABLED}
        mapping = {}
        for pl in RDD.get_physical_layers_by_purpose(purposes=['METAL']):
            key = pl.process.symbol
            if hasattr(RDD.PLAYER[key], 'EDGE_CONNECTED'):
                derived_layer = RDD.PLAYER[key].EDGE_CONNECTED
                ps_1 = derived_layer.layer1.process.symbol
                ps_2 = derived_layer.layer2.process.symbol
                if ps_1 == ps_2:
                    mapping[derived_layer] = RDD.PLAYER[key].EDGE_PORT_ENABLED
                else:
                    raise ValueError('Error in RDD: Edge process \'{}\' not the same as metal process \'{}\'.'.format(ps_2, ps_1))
            else:
                LOG.warning('Edge detection for METAL layer {} ignored.'.format(key))

        pg_overlap = self.device.overlap_elementals
        edges = get_derived_elementals(el, mapping=mapping, store_as_edge=True)

        overlap_edges = {}

        # print(pg_overlap)
        # print(edges)

        for j, pg in enumerate(pg_overlap):
            for e in pg.elementals:
                e = deepcopy(e)
                overlap_edges[e] = []
                for i, edge in enumerate(edges):
                    if edge.overlaps(e):
                        # FIXME: Cannot use this, since Gmsh seems to crach due to the hashing string.
                        # edges[i].pid = p.id_string()
                        # edges[i].pid = '{}_{}'.format(p.__repr__(), p.uid)
                        edges[i].pid = '{}'.format(e.shape.hash_string)
                        overlap_edges[e].append(edges[i])

        # # NOTE: Testing generated edges via viewer.
        # # --------------------------------------------------------------------
        # if (len(edges) > 0) and (len(overlap_edges) == 0):
        # # if (len(el) > 0) and (len(overlap_edges) == 0):
        #     e = spira.Polygon(alias='NoPG', shape=[], layer=spira.Layer(1))
        #     overlap_edges[e] = []
        #     for i, edge in enumerate(edges):
        #     # for i, edge in enumerate(el):
        #         edges[i].pid = '{}'.format(e.shape.hash_string)
        #         overlap_edges[e].append(edges[i])
        # # --------------------------------------------------------------------

        # print('[--] Overlapping Edges:')
        # for k, v in overlap_edges.items():
        #     print(k)
        #     for e in v:
        #         print(e)
        #         print(e.pid)
        #     print('')
        # print('')

        return overlap_edges

    def create_connected_elementals(self):
        """ Adds contact ports to each metal polygon connected by a 
        contact layer and return a list of the updated elementals. """
        for e1 in self.__make_polygons__():
            for e2 in self.device.elementals:
                for m in ['BOT_LAYER', 'TOP_LAYER']:
                    if e2.layer == RDD.VIAS[e1.process].LAYER_STACK[m]:
                        if e2.encloses(e1.center):
                            e2.ports += spira.Port(
                                name=e1.process,
                                midpoint=e1.center,
                                process=e1.layer.process,
                                purpose=e1.layer.purpose,
                                port_type='contact')
        return self.device.elementals

    # def create_contact_ports(self):
    #     from spira.yevon.geometry.ports.port_list import PortList
    #     ports = PortList()
    #     for i, pg in enumerate(self.__make_polygons__()):
    #         for e in pg.elementals:
    #             ports += spira.Port(
    #                 name='C{}'.format(i),
    #                 midpoint=e.center,
    #                 process=pg.process,
    #                 port_type='contact'
    #             )
    #     return ports

    def gdsii_output_virtual_connect(self, **kwargs):

        elems = spira.ElementalList()
        # for e in self.__make_polygons__():
        #     elems += e

        for o, edges in self.connected_edges.items():
            elems += o
            for e in edges:
                # elems += e
                elems += e.outside
                # elems += e.outside.transform(e.transformation)
        for e in self.device.elementals:
            elems += e

        D = spira.Cell(name='_VIRTUAL_CONNECT', elementals=elems)
        D.gdsii_output()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)


def virtual_connect(device):
    return VirtualConnect(device=device)

