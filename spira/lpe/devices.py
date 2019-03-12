import spira 
from spira import param, shapes
from spira.lne.net import Net
import numpy as np
from copy import copy, deepcopy
from spira.lpe.structure import Structure
from spira.gdsii.elemental.port import __Port__
from spira.core.mixin.netlist import NetlistSimplifier
from spira.lpe.containers import __CellContainer__
from spira.visualization import color


RDD = spira.get_rule_deck()


class Device(Structure):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=1)

    def __init__(self, name=None, metals=None, contacts=None, **kwargs):
        super().__init__(name=None, **kwargs)

        if metals is not None:
            self.metals = metals
        if contacts is not None:
            self.contacts = contacts

    def create_primitives(self, elems):
        for N in self.contacts:
            elems += N
        # FIXME: Works for ytron, fails for junction.
        # for P in self.ports:
        #     prim_elems += P
        return elems

    def create_elementals(self, elems):
        for e in self.merged_layers:
            elems += e
        for e in self.contacts:
            elems += e

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        return elems

    def create_netlist(self):
        self.g = self.merge

        self.g = self.nodes_combine(algorithm='d2d')
        self.g = self.nodes_combine(algorithm='s2s')

        # self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


class Via(Device):
    color = param.ColorField(default=color.COLOR_LIGHT_GRAY)

