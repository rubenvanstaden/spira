import spira
import numpy as np
from copy import copy, deepcopy
from spira import param, shapes
from spira.rdd import get_rule_deck
from demo.pdks.components.junction import Junction
from spira.lgm.route.manhattan_base import RouteManhattan
from demo.pdks import ply
from spira.lgm.route.basic import RouteShape, RouteBasic, Route
from spira.lpe.primitives import SLayout
from spira.lpe.containers import __CellContainer__
from spira.lpe.circuits import Circuit
from spira.lpe.devices import DeviceLayout, __Device__
from spira.lgm.shapes.advance import YtronShape


RDD = get_rule_deck()


class YtronDevice(__Device__):

    um = param.FloatField(default=1e+6)

    ytron = param.DataField(fdef_name='create_ytron')

    def create_ytron(self):
        return YtronShape(theta_resolution=100)

    def create_metals(self, elems):

        physical_ytron = ply.Polygon(
            name='ytron',
            player=RDD.PLAYER.BAS,
            points=self.ytron.points,
        )
        elems += physical_ytron

        return elems

    def create_ports(self, ports):

        s = self.ytron

        ml = [-(s.xc + s.arm_x_left + s.arm_widths[0]/2), s.yc + s.arm_y_left]
        mr = [s.xc + s.arm_x_right + s.arm_widths[1]/2, s.yc + s.arm_y_right]
        ms = [(s.arm_widths[1] - s.arm_widths[0])/2, -s.source_length + s.yc]

        ports += spira.Term(
            name='left',
            midpoint=ml,
            width=s.arm_widths[0],
            orientation=0
        )
        ports += spira.Term(
            name='right',
            midpoint=mr,
            width=s.arm_widths[1],
            orientation=0
        )
        ports += spira.Term(
            name='source',
            midpoint=ms,
            width=s.arm_widths[0] + s.arm_widths[1] + 2*s.xc,
            orientation=180
        )

        return ports


if __name__ == '__main__':

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = YtronDevice(level=2)

    jj.netlist
    # jj.output()
    # jj.mask.output()

    spira.LOG.end_print('JTL example finished')



