import numpy as np
import networkx as nx
# import spira.all as spira 
from spira.core.param.variables import *
from spira.yevon.visualization.color import ColorField

from copy import copy, deepcopy
from spira.yevon.geometry import shapes
from spira.yevon.visualization import color
from spira.netex.structure import Structure
from spira.netex.containers import __CellContainer__, __CircuitContainer__
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class Device(__CircuitContainer__, Structure):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    level = IntegerField(default=1)
    lcar = FloatField(default=1.0)

    def __init__(self, name=None, metals=None, contacts=None, **kwargs):
        super().__init__(name=None, **kwargs)

        # if routes is not None:
        #     self.routes = routes
        # if structures is not None:
        #     self.structures = structures

        if metals is not None:
            self.metals = metals
        if contacts is not None:
            self.contacts = contacts

    def create_primitives(self, elems):
        for N in self.contacts:
            elems += N
        # FIXME: Works for ytron, fails for junction.
        for P in self.ports:
            elems += P
        return elems

    def create_contacts(self, elems):
        for e in self.structures:
            elems += e
        return elems

    def create_metals(self, elems):
        for e in self.routes:
            elems += e
        return elems

    def create_elementals(self, elems):
        for e in self.merged_layers:
            elems += e
        # for e in self.metals:
        #     if isinstance(e, spira.ElementList):
        #         for elem in e:
        #             elems += elem
        #     else:
        #         elems += e
        for e in self.contacts:
            elems += e

        # for e in self.routes:
        #     elems += e
        # for e in self.structures:
        #     elems += e

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        return elems

    def create_netlist(self):

        # print('Generating device netlist')

        # graphs = []
        # for net in self.nets:
        #     graphs.append(net.graph)

        graphs = []
        for m in self.merged_layers:
            graphs.append(m.graph)

        self.g = nx.disjoint_union_all(graphs)

        self.g = self.nodes_combine(algorithm='d2d')
        self.g = self.nodes_combine(algorithm='s2s')

        # self.plotly_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


class Via(Device):
    color = ColorField(default=color.COLOR_LIGHT_GRAY)


class DeviceDRC(__CellContainer__):

    def create_elementals(self, elems):

        for R in RDD.RULES.WIDTH:
            print(R.design_rule)
            for e in self.cell.elementals:
                if e.ps_layer == R.design_rule.layer1:
                    print(e.ports)
                    if not R.design_rule.apply(e1=e):
                        # e.error = R.error_layer.datatype
                        e.ps_layer.layer.datatype = 100

                    for p in e.edge_ports:
                        self.ports += p

                    elems += e
            print('')

        return elems

