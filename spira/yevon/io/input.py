from spira.core.parameters.variables import *
from spira.core.parameters.descriptor import Parameter
from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.process.gdsii_layer import __Layer__, Layer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class __InputBasic__(ParameterInitializer):
    """  """

    file_name = StringParameter()
    cell_name = StringParameter(allow_none=True, default=None)

    def __init__(self, file_name, **kwargs):
        super().__init__(file_name=file_name, **kwargs)

    def read(self):
        raise NotImplementedError('Must provide implementation in subclass.')

    def parse(self, item):
        raise NotImplementedError('Must provide implementation in subclass.')


class InputBasic(__InputBasic__):
    """  """

    prefix = StringParameter(default='')
    flatten = BoolParameter()
    layer_map = Parameter(default=RDD.GDSII.IMPORT_LAYER_MAP)

    def __init__(self, file_name, **kwargs):
        super().__init__(file_name=file_name, **kwargs)
        self.library = None

    def read(self):
        self.library = Library('Imported')
        for cell in self.parse.dependencies():
            self.library += cell
        return self.library

    def map_layer(self, layer):
        L = self.layer_map.get(layer, None)
        if isinstance(L, __Layer__):
            return L
        elif L is None:
            return L
        else:
            return Layer(L)



