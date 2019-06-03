import spira.all as spira
from tests._03_structures.jtl_bias import JtlBias
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


D = JtlBias()
# D.output()
D.write_gdsii_vmodel()


# class JtlModel(spira.Cell):
#     """ Generates a post-processing model of the JTL cell. """

#     def create_elementals(self, elems):
#         return elems

