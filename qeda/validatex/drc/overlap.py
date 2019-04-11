import spira
from core import param
from spira.lrc.rules import __DoubleLayerDesignRule__
from core.initializer import ElementalInitializer


RDD = spira.get_rule_deck()


class Overlap(__DoubleLayerDesignRule__):
    minimum = param.FloatField()

    def __repr__(self):
        return 'Rule surround: min={}'.format(self.minimum)

    def apply(self, elems):
        pass
