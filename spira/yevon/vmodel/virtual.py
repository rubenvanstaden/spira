import spira.all as spira
from spira.yevon.vmodel.elementals import union_process_polygons
from spira.core.parameters.initializer import FieldInitializer
from .geometry import GmshGeometry


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

    # def __make_polygons__(self):
    #     el = spira.ElementalList()
    #     for e in self.device.process_elementals:
    #         el += e
    #     for e in self.device.block_elementals:
    #         el += e
    #     elems = spira.ElementalList()
    #     for process in self.process_flow.active_processes:
    #         for e in union_process_polygons(el, process=process):
    #             elems += e
    #     return elems

    def __make_polygons__(self):
        el = spira.ElementalList()
        for e in self.device.process_elementals:
            el += e
        # for e in self.device.block_elementals:
        #     el += e

        process_polygons = {}
        for process in self.process_flow.active_processes:
            plys = union_process_polygons(el, process=process)
            if len(plys) > 0:
                process_polygons[process] = plys
        print(process_polygons)
        return process_polygons

    def create_geometry(self):
        process_geom = {}
        process_polygons = self.__make_polygons__()
        for k, v in process_polygons.items():
            process_geom[k] = GmshGeometry(process=k, process_polygons=v)
        # print(process_geom)
        return process_geom

    def write_gdsii_vmodel(self, **kwargs):
        elems = spira.ElementalList()
        for k, v in self.__make_polygons__().items(): elems += v
        D = spira.Cell(name='_VMODEL', elementals=elems)
        D.output()


class VirtualProcessIntersection(__VirtualModel__):

    # expanded_elementals = spira.ElementalListField()

    # def create_expanded_elementals(self, elems):
    #     D = self.device.flat_expand_transform_copy()
    #     elems = D.elementals
    #     return elems

    def __make_polygons__(self):
        from spira.yevon.utils import clipping
        D = self.device.flat_expand_transform_copy()
        elems = clipping.intersection_polygons(D.elementals)
        return elems

    def __make_contact_ports__(self):
        from spira.yevon.geometry.ports.port_list import PortList
        ports = PortList()
        for i, e in enumerate(self.__make_polygons__()):
            ports += spira.Port(name='C{}'.format(i), midpoint=e.center)
        return ports

    def write_gdsii_vinter(self, **kwargs):
        D = spira.Cell(name='_VINTER',
            elementals=self.__make_polygons__(),
            ports=self.__make_contact_ports__())
        D.output()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)


def virtual_process_intersection(device, process_flow):
    return VirtualProcessIntersection(device=device, process_flow=process_flow)


