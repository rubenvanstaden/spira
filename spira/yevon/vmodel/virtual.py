import spira.all as spira
# from spira.yevon.vmodel.elementals import union_process_polygons
from spira.core.parameters.initializer import FieldInitializer
from .geometry import GmshGeometry
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'VirtualProcessModel',
    'virtual_process_model',
    'virtual_process_intersection'
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

    # def write_gdsii_vmodel(self, **kwargs):
    #     elems = spira.ElementalList()
    #     # for k, v in self.__make_polygons__().items(): elems += v
    #     for process, 
    #     D = spira.Cell(name='_VMODEL', elementals=elems)
    #     D.output()


from spira.yevon.filters.layer_filter import LayerFilterAllow
class VirtualProcessIntersection(__VirtualModel__):

    contact_ports = spira.DataField(fdef_name='create_contact_ports')

    def __make_polygons__(self):

        pcell = self.device

        # D = pcell.expand_flat_copy()
        D = self.device.expand_flat_no_jj_copy()

        elems = spira.ElementalList()
        for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
            for layer in RDD.get_physical_layers_by_process(processes=process):
                LF = LayerFilterAllow(layers=[layer])
                el = LF(D.elementals.polygons)
                elems += spira.PolygonGroup(elementals=el, layer=layer).intersect
        return elems

    def create_contact_ports(self):
        from spira.yevon.geometry.ports.port_list import PortList
        ports = PortList()
        for i, pg in enumerate(self.__make_polygons__()):
            for e in pg.elementals:
                ports += spira.Port(
                    name='C{}'.format(i),
                    midpoint=e.center,
                    process=pg.process,
                    port_type='contact'
                )
        return ports

    def write_gdsii_vinter(self, **kwargs):

        elems = spira.ElementalList()
        for pg in self.__make_polygons__():
            for e in pg.elementals:
                elems += e

        D = spira.Cell(name='_AND', elementals=elems)
        D.output()

        # D = spira.Cell(name='_VINTER',
        #     elementals=self.__make_polygons__(),
        #     ports=self.__make_contact_ports__())
        # D.output()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)


def virtual_process_intersection(device, process_flow):
    return VirtualProcessIntersection(device=device, process_flow=process_flow)


