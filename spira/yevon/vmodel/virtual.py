import spira.all as spira

from spira.yevon.utils.elementals import get_derived_elementals
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
    # connect_type = spira.StringField(default='metal_layer')
    # contact_ports = spira.DataField(fdef_name='create_contact_ports')
    connected_elementals = spira.DataField(fdef_name='create_connected_elementals')
    # connected_elementals = spira.ElementalListField()

    def __make_polygons__(self):

        elems = spira.ElementalList()
        if self.connect_type == 'contact_layer':
            
            mapping = {}
            for k in RDD.VIAS.keys:
                mapping[RDD.PLAYER[k].CLAYER_CONTACT] = RDD.VIAS[k].LAYER_STACK['VIA_LAYER']
                mapping[RDD.PLAYER[k].CLAYER_M1] = RDD.VIAS[k].LAYER_STACK['BOT_LAYER']
                mapping[RDD.PLAYER[k].CLAYER_M2] = RDD.VIAS[k].LAYER_STACK['TOP_LAYER']

            print('\nMapping:')
            for k, v in mapping.items():
                print(k, v)
            print('')

            print(self.device.elementals)

            el = get_derived_elementals(elements=self.device.elementals, mapping=mapping)
            for e in el:
                if e.purpose == 'METAL': 
                    pass
                else: 
                    elems += e
        else:
            pass
            # # D = self.device.expand_flat_copy()
            # D = self.device.expand_flat_no_jj_copy()

            # elems = spira.ElementalList()
            # for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
            #     for layer in RDD.get_physical_layers_by_process(processes=process):
            #         LF = LayerFilterAllow(layers=[layer])
            #         el = LF(D.elementals.polygons)
            #         elems += spira.PolygonGroup(elementals=el, layer=layer).intersect
        return elems

    def create_connected_elementals(self):
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
        for e in self.__make_polygons__():
            elems += e

        D = spira.Cell(name='_VIRTUAL_CONNECT', elementals=elems)
        D.gdsii_output()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)


# def virtual_process_intersection(device, process_flow):
#     return VirtualProcessIntersection(device=device, process_flow=process_flow)


def virtual_connect(device):
    return VirtualConnect(device=device)

