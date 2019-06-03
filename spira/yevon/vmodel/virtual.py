import spira.all as spira
from spira.core.parameters.initializer import FieldInitializer


__all__ = ['VirtualProcessModel', 'virtual_process_model']


class __VirtualModel__(FieldInitializer):
    device = spira.CellField(doc='The device from which a virtual model will be constructed.')
    geometry = spira.DataField(fdef_name='create_geometry')


class VirtualProcessModel(__VirtualModel__):

    def create_geometry(self):

        for e in self.device.process_elementals:
            print(e)

        print('\n[*] Reference blocks')
        for e in self.device.block_elementals:
            print(e)


def virtual_process_model(device):
    return VirtualProcessModel(device=device)



