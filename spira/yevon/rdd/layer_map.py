from spira.core.parameters.variables import DictField
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.descriptor import DataField
from spira.yevon.rdd.all import *


__all__ = ['UnconstrainedGdsiiPPLayerInputMap', 'UnconstrainedGdsiiPPLayerOutputMap']


class UnconstrainedGdsiiPPLayerInputMap(FieldInitializer):
    """ Map the GDSII Layers onto ProcessLayers, and the Datatypes onto PurposeLayers. """

    process_layer_map = DictField()
    purpose_datatype_map = DictField()
    layer_process_map = DataField(fdef_name='create_layer_process_map')
    datatype_purpose_map = DataField(fdef_name='create_datatype_purpose_map')
    layer_map = DictField(default = {}, doc = "Additional layer map, to be used complementarily to the 'process_layer_map' and 'purpose_datatype_map'.")

    def create_layer_process_map(self):
        lpm = {}
        for k, v in self.process_layer_map.items():
            lpm[v] = k
        return lpm

    def create_datatype_purpose_map(self):
        dpm = {}
        for k, v in self.purpose_datatype_map.items():
            dpm[v] = k
        return dpm

    def __getitem__(self, key, default=None):
        if isinstance(key, Layer):
            pr = self.layer_process_map.get(key.number, None)
            pu = self.datatype_purpose_map.get(key.datatype, None)
            if pr is None or pu is None:
                for gdsiilayer, pplayer  in self.layer_map.items():
                    if (key.number == gdsiilayer.number) and (key.datatype == gdsiilayer.datatype):
                        return pplayer
                return default
            else:
                return PhysicalLayer(process = pr, purpose = pu)
        else:
            raise Exception("Key should be of type PhysicalLayer, but is of type %s." %type(key))

    def get(self, key, default):
        return self.__getitem__(key, default)


class UnconstrainedGdsiiPPLayerOutputMap(FieldInitializer):
    process_layer_map = DictField()
    purpose_datatype_map = DictField() 
    layer_map = DictField(default={}, doc="Additional layer map, to be used complementarily to the 'process_layer_map' and 'purpose_datatype_map'.")

    def __getitem__(self, key, default = None):
        if isinstance(key, PhysicalLayer):
            ln = self.process_layer_map.get(key.process, None)
            dt = self.purpose_datatype_map.get(key.purpose, None)
            if ln is None or dt is None: 
                for pplayer, gdsiilayer in self.layer_map.items():
                    if (key.process == pplayer.process) and (key.purpose == pplayer.purpose):
                        return gdsiilayer
                return default
            else:
                return Layer(ln, dt)
        elif isinstance(key, Layer):
            return key
        else:
            raise Exception("Key should be of type PhysicalLayer, but is of type %s." %type(key))

    def get(self, key, default):
        return self.__getitem__(key, default)

