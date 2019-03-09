import spira
from spira import param, shapes, io
from spira.lpe.circuits import Circuit

from demo.pdks.components.mitll.junction import Junction
from demo.pdks.components.mitll.via import ViaC5R, ViaI5
from spira.lpe.mask import Mask
from demo.pdks.process.mitll_pdk.database import RDD


class Resistor(Circuit):
    """ Resistor PCell of type Circuit between two vias connecting to layer M6. """

    length = param.FloatField(default=10*1e6)
    via_left = param.DataField(fdef_name='create_via_left')
    via_right = param.DataField(fdef_name='create_via_right')

    def create_via_left(self):
        via = ViaC5R()
        return spira.SRef(via)

    def create_via_right(self):
        via = ViaC5R()
        return spira.SRef(via, midpoint=(self.length, 0))

    def create_elementals(self, elems):

        res = spira.Route(
            port1=self.via_left.ports['Output'],
            port2=self.via_right.ports['Input'],
            player=RDD.PLAYER.R5
        )

        elems += self.via_left
        elems += self.via_right
        elems += spira.SRef(res)

        return elems

    def create_ports(self, ports):
        for p in self.via_left.ports.values():
            name = 'vl_{}'.format(p.name)
            ports += p.modified_copy(name=name, width=1*self.um)
        for p in self.via_right.ports.values():
            name = 'vr_{}'.format(p.name)
            ports += p.modified_copy(name=name, width=1*self.um)
        return ports


if __name__ == '__main__':

    name = 'Resistor PCell'
    spira.LOG.header('Running example: {}'.format(name))

    cell = spira.Cell(name='ResistorTest')

    c1 = Resistor()
    c2 = Resistor(length=20*1e6)

    cell += spira.SRef(c1)
    cell += spira.SRef(c2, midpoint=(0, -5*1e6))

    cell.output()

    # c1.netlist
    # c1.output()

    # mask = Mask(name=input_cell.name, cell=input_cell)
    # mask.netlist
    # mask.output()

    spira.LOG.end_print('JTL example finished')

