import spira
from spira import param
from spira.lrc.rules import *


RDD = spira.get_rule_deck()


class Rules(spira.Cell):

    def create_elementals(self, elems):

        # elems += Density(layer1=RDD.M4, layer2=RDD.MOAT, minimum=35)
        # elems += Surround(layer1=RDD.M6, layer2=RDD.M4, minimum=0.3) # TODO: Remove, just a test
        # elems += Width(layer1=RDD.M5, minimum=0.7, maximum=20) # TODO: Not implemented!
        # elems += Width(layer1=RDD.R5, minimum=0.5, maximum=20, violate=True) # TODO: Not implemented!

        # # ----------- Via DRC --------------
        # elems += Surround(layer1=RDD.J5, layer2=RDD.M6, minimum=0.3)
        # elems += Surround(layer1=RDD.C5, layer2=RDD.M6, minimum=0.35)

        return elems


RDD.RULES = Rules()


