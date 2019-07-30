from spira.core.parameters.variables import DictParameter
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import Parameter
from spira.yevon.process.all import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['MapGdsiiToPhysical', 'MapPhysicalToGdsii']


class MapGdsiiToPhysical(ParameterInitializer):
    """ Map the GDSII Layers onto ProcessLayers, and the Datatypes onto PurposeLayers. """

    process_layer_map = DictParameter()
    purpose_datatype_map = DictParameter()

    @property
    def layer_process_map(self):
        return dict([(v, k) for k, v in self.process_layer_map.items()]) 

    @property
    def datatype_purpose_map(self):
        return dict([(v, k) for k, v in self.purpose_datatype_map.items()]) 

    def __getitem__(self, key, default=None):
        if isinstance(key, PhysicalLayer):
            return key
        elif isinstance(key, Layer):
            # print(key)
            # print(self.layer_process_map.keys())
            # FIXME: Implement error checking for if layer number is not found in RDD.
            if key.number in self.layer_process_map:
                pc = self.layer_process_map[key.number]
                pp = self.datatype_purpose_map[key.datatype]
                return PhysicalLayer(process=pc, purpose=pp)
            raise ValueError('Layer number not found in {}.'.format(RDD))
            # return PhysicalLayer(process=RDD.PROCESS.VIRTUAL, purpose=RDD.PURPOSE.TEXT)
        else:
            raise Exception("Key should be of type PhysicalLayer, but is of type %s." %type(key))

    def get(self, key, default):
        return self.__getitem__(key, default)


class MapPhysicalToGdsii(ParameterInitializer):
    """  """

    process_layer_map = DictParameter()
    purpose_datatype_map = DictParameter() 

    def __getitem__(self, key, default=None):
        if isinstance(key, PhysicalLayer):
            ln = self.process_layer_map[key.process]
            dt = self.purpose_datatype_map[key.purpose]
            return Layer(number=ln, datatype=dt)
        elif isinstance(key, Layer):
            return key
        else:
            raise Exception("Key should be of type PhysicalLayer, but is of type %s." %type(key))

    def get(self, key, default):
        return self.__getitem__(key, default)
