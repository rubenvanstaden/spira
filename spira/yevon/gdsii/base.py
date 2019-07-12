from spira.core.transformable import Transformable
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.initializer import MetaInitializer
from spira.core.parameters.descriptor import FunctionParameter
from spira.yevon.process.gdsii_layer import LayerParameter
from spira.core.parameters.variables import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class MetaElement(MetaInitializer):
    """  """

    def __call__(cls, *params, **keyword_params):
        kwargs = cls.__map_parameters__(*params, **keyword_params)
        cls = super().__call__(**kwargs)
        cls.__keywords__ = kwargs
        return cls


class __Element__(Transformable, ParameterInitializer, metaclass=MetaElement):
    """ Base class for all transformable elements. """

    def get_node_id(self):
        if self.__id__:
            return self.__id__
        else:
            return self.__str__()

    def set_node_id(self, value):
        self.__id__ = value

    node_id = FunctionParameter(get_node_id, set_node_id)

    location_name = StringParameter(default='')

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)
        # super().__init__(**kwargs)

    def __add__(self, other):
        if isinstance(other, list):
            l = spira.ElementList([self])
            l.extend(other)
            return l
        elif isinstance(other, __Element__):
            return spira.ElementList([self, other])
        else:
            raise TypeError("Wrong type of argument for addition in __Element__: " + str(type(other)))

    def __radd__(self, other):
        if isinstance(other, list):
            l = spira.ElementList(other)
            l.append(self)
            return l
        elif isinstance(other, __Element__):
            return spira.ElementList([other, self])
        else:
            raise TypeError("Wrong type of argument for addition in __Element__: " + str(type(other)))

    def flatten(self):
        return [self]

    def dependencies(self):
        return None


class __LayerElement__(__Element__):
    """  """

    layer = LayerParameter()

    def __init__(self, layer=0, transformation=None, **kwargs):
        super().__init__(layer=layer, transformation=transformation, **kwargs)

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, __LayerElement__):
            return False
        if other.layer.key != self.layer.key:
            return False                
        if self.shape.transform_copy(self.transformation) != other.shape.transform_copy(other.transformation):
            return False
        return True

    def __ne__(self,other):
        return not self.__eq__(other)      
