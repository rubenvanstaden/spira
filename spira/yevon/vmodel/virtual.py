import spira.all as spira
from spira.yevon.vmodel.elementals import union_process_polygons
from spira.core.parameters.initializer import FieldInitializer
from .geometry import GmshGeometry


__all__ = ['VirtualProcessModel', 'virtual_process_model']


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
        for e in self.device.block_elementals:
            el += e

        process_polygons = {}
        for process in self.process_flow.active_processes:
            plys = union_process_polygons(el, process=process)
            if len(plys) > 0:
                process_polygons[process] = plys
        return process_polygons

    def create_geometry(self):
        process_geom = {}
        process_polygons = self.__make_polygons__()
        for k, v in process_polygons.items():
            process_geom[k] = GmshGeometry(process=k, process_polygons=v)
        print(process_geom)
        return process_geom

    def write_gdsii_vmodel(self, **kwargs):
        D = spira.Cell(name='_VMODEL', elementals=self.__make_polygons__())
        D.output()


def virtual_process_model(device, process_flow):
    return VirtualProcessModel(device=device, process_flow=process_flow)



