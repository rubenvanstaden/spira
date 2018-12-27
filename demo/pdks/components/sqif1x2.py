import spira
from spira import param
from spira.rdd import get_rule_deck
from examples.squid import Squid
from examples.jj_squid import JunctionSquid
from examples.junction import Junction
from examples.squid import PhysicalJunction


RDD = get_rule_deck()


class Sqif1x2(Squid):

    def create_elementals(self, elems):

        super().create_elementals(elems)

        con = 6
        jj = PhysicalJunction(p1=[-self.w/con, -self.h/2],
                              p2=[self.w/con, self.h/2],
                              layer=RDD.J5)

        elems += spira.SRef(jj, origin=(2*self.width*1e6, 0))

        self.midpoint = 20

        elems += self.create_top_routing()
        elems += self.create_bot_routing()

        return elems


class JunctionSqif1x2(JunctionSquid):

    def create_elementals(self, elems):

        super().create_elementals(elems)

        jj = Junction()

        # FIXME: Automate this movement.
        jj.move(origin=jj.center, destination=(0,0))
        j1 = spira.SRef(jj, origin=(31, 0), rotation=-90)

        elems += j1

        self.midpoint = 30

        elems += self.create_top_routing()
        elems += self.create_bot_routing()

        return elems


if __name__ == '__main__':

    from spira import settings
    from spira.templates.library import library

    settings.set_library(library)

    name = 'sqif_1x2'
    doc = 'SQIF PCell with Junctions included.'

    spira.LOG.header('Running example: {}'.format(name))

    # jj = Sqif1x2(width=10, height=3, w=5, h=0.5)
    jj = JunctionSqif1x2(width=10, height=3, w=5, h=0.5)

    # mcell = MaskCell(cell=jj)

    # mcell.output(name=name)
    jj.output(name=name)

    spira.LOG.end_print('Junction example finished')







