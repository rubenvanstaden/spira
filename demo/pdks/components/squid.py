import spira
from spira import param
from spira import shapes
from spira.rdd import get_rule_deck
from demo.pdks.components.junction import Junction
from spira.lgm.route.manhattan import RouteManhattan, RouteManhattan180


RDD = get_rule_deck()


class Squid(spira.Cell):

    def create_elementals(self, elems):

        jj = Junction()

        jj.center = (0,0)

        s1 = spira.SRef(jj, midpoint=(0,0), rotation=90)
        s2 = spira.SRef(jj, midpoint=(20,0), rotation=-90)

        rm = RouteManhattan180(
            port1=s2.ports['Output'],
            port2=s1.ports['Input'],
            radius=1, length=5
        )

        s3 = spira.SRef(rm)
        s3.move(midpoint=s3.ports['T1'], destination=s2.ports['Output'])
        elems += [s1, s2, s3]

        return elems


if __name__ == '__main__':

    name = 'SQUID PCell'
    spira.LOG.header('Running example: {}'.format(name))

    squid = Squid()
    squid.output(name=name)

    spira.LOG.end_print('Junction example finished')



