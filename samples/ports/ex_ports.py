import os
import spira.all as spira
import numpy as np
import networkx as nx
import pygmsh
import meshio
from spira.yevon.geometry import shapes
from spira.yevon.gdsii.group import Group
from spira.core.initializer import FieldInitializer
from spira.yevon.utils import numpy_to_list
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class ProcessLayer(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.RectangleShape(p1=(0,0), p2=(50*1e6, 5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        elems += ply

        return elems

    def create_ports(self, ports):

        ports += spira.Terminal(midpoint=(0, 2.5*1e6), width=5*1e6)
        ports += spira.Terminal(midpoint=(50*1e6, 2.5*1e6), width=5*1e6, orientation=180)

        return ports


class PhysicalGeometry(Group):

    bool_op = spira.StringField(default='union', restriction=spira.RestrictContains(['union', 'intersection', 'difference']))

    def _union_elementals(self, elems):
        points = np.array([])
        ply = elems[0]
        for i in range(1, len(elems)):
            ply = ply | elems[i]
        el = spira.ElementList()
        el += ply
        return el

    def create_elementals(self, elems):

        elems += spira.Polygon(
            shape=shapes.RectangleShape(p1=(0,0), p2=(50*1e6, 5*1e6)),
            gds_layer=spira.Layer(number=1)
        )

        elems += spira.Polygon(
            shape=shapes.RectangleShape(p1=(50*1e6, 5*1e6), p2=(55*1e6, -50*1e6)),
            gds_layer=spira.Layer(number=1)
        )

        elems += spira.Polygon(
            shape=shapes.RectangleShape(p1=(55*1e6, -50*1e6), p2=(100*1e6, -45*1e6)),
            gds_layer=spira.Layer(number=1)
        )

        if self.bool_op == 'union':
            elems = self._union_elementals(elems)

        return elems


class Metals(spira.Cell):

    bool_op = spira.StringField(default='union', restriction=spira.RestrictContains(['union', 'intersection', 'difference']))

    def _union_elementals(self, elems):
        points = np.array([])
        ply = elems[0]
        for i in range(1, len(elems)):
            ply = ply | elems[i]
        el = spira.ElementList()
        el += ply
        return el

    def create_elementals(self, elems):

        elems += spira.Polygon(
            shape=shapes.RectangleShape(p1=(0,0), p2=(50*1e6, 5*1e6)),
            gds_layer=spira.Layer(number=8)
        )

        elems += spira.Polygon(
            shape=shapes.RectangleShape(p1=(50*1e6, 5*1e6), p2=(55*1e6, -50*1e6)),
            gds_layer=spira.Layer(number=8)
        )

        elems += spira.Polygon(
            shape=shapes.RectangleShape(p1=(55*1e6, -50*1e6), p2=(100*1e6, -45*1e6)),
            gds_layer=spira.Layer(number=8)
        )

        if self.bool_op == 'union':
            elems = self._union_elementals(elems)

        return elems

    def create_ports(self, ports):

        ports += spira.Terminal(midpoint=(0, 2.5*1e6), width=5*1e6, ps_layer=RDD.PLAYER.COU)
        ports += spira.Terminal(midpoint=(100*1e6, -47.5*1e6), width=5*1e6, orientation=180, ps_layer=RDD.PLAYER.COU)

        return ports

    def get_metals(self, pl):
        elems = spira.ElementList()
        for e in self.elementals.polygons:
            if pl.layer == e.gds_layer:
                elems += e
        return elems

    def get_ports(self, pl):
        ports = spira.PortList()
        for p in self.ports:
            if p.ps_layer == pl:
                ports += p
        return ports

    def create_nets(self, nets):

        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            elems = self.get_metals(pl)
            ports = self.get_ports(pl)
            if len(elems) > 0:
                nets += spira.Net(elementals=elems, ports=ports, ps_layer=pl)

        return nets


if __name__ == '__main__':

    # 1.)
    # pc = ProcessLayer()
    # pc.output()

    # 2.)
    # cell = spira.Cell(name='MetalCell')
    # pg = PhysicalGeometry()
    # cell += pg.elementals
    # cell.output()

    # 3.)
    # cell = spira.Cell(name='PC')
    # pc = ProcessLayer()
    # cell += spira.SRef(pc, transformation=spira.Rotation(45))
    # cell.output()

    # 4.)
    # pc = ProcessLayer(transformation=spira.Rotation(30))
    # pc.transformation.apply_to_object(pc)
    # # pc = ProcessLayer()
    # # pc.transform(spira.Rotation(30))
    # pc.output()

    # 5.)
    metal = Metals()
    # g = metal.nets.disjoint()
    g = metal.nets[0].g
    metal.plotly_netlist(G=g, graphname='metal', labeltext='id')
    metal.output()


