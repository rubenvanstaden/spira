import spira.all as spira

from spira.core.transformable import Transformable
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.initializer import MetaInitializer
from spira.core.parameters.descriptor import FunctionField
from spira.yevon.process.gdsii_layer import LayerField
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class MetaElemental(MetaInitializer):
    """  """

    def __call__(cls, *params, **keyword_params):
        kwargs = cls.__map_parameters__(*params, **keyword_params)
        instance = super().__call__(**kwargs)
        instance.__keywords__ = kwargs
        return instance


class __Elemental__(Transformable, FieldInitializer, metaclass=MetaElemental):
    """ Base class for all transformable elementals. """

    def get_node_id(self):
        if self.__id__:
            return self.__id__
        else:
            return self.__str__()

    def set_node_id(self, value):
        self.__id__ = value

    node_id = FunctionField(get_node_id, set_node_id)

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)

    def __add__(self, other):
        if isinstance(other, list):
            l = spira.ElementalList([self])
            l.extend(other)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementalList([self, other])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))

    def __radd__(self, other):
        if isinstance(other, list):
            l = spira.ElementalList(other)
            l.append(self)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementalList([other, self])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))

    def flatten(self):
        return [self]

    def dependencies(self):
        return None


class __LayerElemental__(__Elemental__):
    """  """

    layer = LayerField()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def __init__(self, layer=0, transformation=None, **kwargs):
        super().__init__(layer=layer, transformation=transformation, **kwargs)

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, __LayerElemental__):
            return False
        if other.layer.key != self.layer.key:
            return False                
        if self.shape.transform_copy(self.transformation) != other.shape.transform_copy(other.transformation):
            return False
        return True

    def __ne__(self,other):
        return not self.__eq__(other)      
