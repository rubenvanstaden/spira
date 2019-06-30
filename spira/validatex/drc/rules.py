import spira.all as spira
from spira.core.parameters.initializer import ParameterInitializer


class __DesignRule__(ParameterInitializer):
    """ Base class for design rules. """
    doc = param.StringParameter()
    name = param.StringParameter()
    violate = param.BoolParameter()


class __SingleLayerDesignRule__(__DesignRule__):
    """ Rule applying to a single specific layer. """
    # layer1 = param.LayerParameter()
    layer1 = param.PhysicalLayerParameter()


class __DoubleLayerDesignRule__(__DesignRule__):
    """ Rule applying to two differnet layers. """
    layer1 = param.LayerParameter()
    layer2 = param.LayerParameter()


class Rule(ParameterInitializer):
    """  """

    design_rule = param.DesignRuleParameter()
    error_layer = param.PurposeLayerParameter()

    def __repr__(self):
        return '[SPiRA: Rule] {}'.format(self.design_rule.__class__.__name__)

    def __str__(self):
        return self.__repr__()
