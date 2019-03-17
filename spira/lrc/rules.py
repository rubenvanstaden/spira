import spira
from spira import param
from spira.core.initializer import ElementalInitializer


class __DesignRule__(ElementalInitializer):
    """ Base class for design rules. """
    doc = param.StringField()
    name = param.StringField()
    violate = param.BoolField()
    um = param.FloatField(default=1e6)


class __SingleLayerDesignRule__(__DesignRule__):
    """ Rule applying to a single specific layer. """
    # layer1 = param.LayerField()
    layer1 = param.PhysicalLayerField()


class __DoubleLayerDesignRule__(__DesignRule__):
    """ Rule applying to two differnet layers. """
    layer1 = param.LayerField()
    layer2 = param.LayerField()


class Rule(ElementalInitializer):
    """  """

    design_rule = param.DesignRuleField()
    error_layer = param.PurposeLayerField()

    def __repr__(self):
        return '[SPiRA: Rule] {}'.format(self.design_rule.__class__.__name__)

    def __str__(self):
        return self.__repr__()
