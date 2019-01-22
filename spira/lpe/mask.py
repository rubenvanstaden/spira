import spira
from spira import param
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class __Mask__(spira.Cell):

    layer = param.LayerField()

    def create_elementals(self, elems):
        return elems

    def set_net(self):
        pass

    def get_net(self):
        pass


class Metal(__Mask__):
    pass


class Native(__Mask__):
    pass



