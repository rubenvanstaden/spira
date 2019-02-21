import spira
from spira import param, shapes
from spira.rdd import get_rule_deck
from demo.pdks.components.junction import Junction
from spira.lgm.route.manhattan_base import Route
from spira.lpe.primitives import SLayout


RDD = get_rule_deck()


class Squid(spira.PCell):

    m1 = param.MidPointField(default=(0,0))
    m2 = param.MidPointField(default=(0,0))
    rotation = param.FloatField(default=0)

    # def create_routes(self, routes):
    #     return routes

    def create_elementals(self, elems):

        jj = Junction()

        # FIXME: Automate this centering.
        jj.center = (0,0)

        s1 = spira.SRef(jj, midpoint=self.m1, rotation=self.rotation)
        s2 = spira.SRef(jj, midpoint=self.m2, rotation=-self.rotation)

        r1 = Route(
            port1=s1.ports['Output'],
            port2=s2.ports['Output'],
            gdslayer=RDD.COU.LAYER,
            radius=1, length=1
        )

        r2 = Route(
            port1=s1.ports['Input'],
            port2=s2.ports['Input'],
            gdslayer=RDD.COU.LAYER,
            radius=1, length=1
        )

        s3 = spira.SRef(r1)
        elems += s3

        s4 = spira.SRef(r2)
        elems += s4

        elems += [s1, s2]

        return elems


if __name__ == '__main__':

    name = 'SQUID PCell'
    spira.LOG.header('Running example: {}'.format(name))

    s = Squid(m2=(30,-30), rotation=0)
    # s.output(name=name)

    # layout = SLayout(cell=s7, level=1)
    layout = SLayout(cell=s, level=2)
    layout.output(name=name)

    # ------------------------------------------------------

    # squid = spira.Cell(name='SQUID')

    # # s5 = Squid(m2=(30,30), rotation=0)
    # # s6 = Squid(m2=(-30,30), rotation=0)
    # s7 = Squid(m2=(30,-30), rotation=0)

    # # squid += spira.SRef(s5, midpoint=(0,0))
    # # squid += spira.SRef(s6, midpoint=(50,0))
    # squid += spira.SRef(s7, midpoint=(100,0))

    # squid.output(name=name)

    # ------------------------------------------------------

    spira.LOG.end_print('SQUID example finished')



