import spira
from spira import param
from spira.rdd import get_rule_deck
from examples.junction import Junction


RDD = get_rule_deck()


class JunctionSquid(spira.Cell):

    width = param.FloatField()
    height = param.FloatField()
    midpoint = param.FloatField()
    w = param.FloatField()
    h = param.FloatField()

    top_routing = param.DataField(fdef_name='create_top_routing')
    bot_routing = param.DataField(fdef_name='create_bot_routing')

    def create_top_routing(self):
        p1 = [self.midpoint, self.h/2]
        p2 = [self.midpoint, self.h/2+self.height]
        p3 = [self.width, self.h/2+self.height]
        p4 = [self.width, self.h/2]

        points = [p1, p2, p3, p4]

        return spira.Path(points, width=1, gdslayer=RDD.M5, distance=3)

    def create_bot_routing(self):
        p1 = [self.midpoint, -self.h/2]
        p2 = [self.midpoint, -self.height]
        p3 = [self.width, -self.height]
        p4 = [self.width, -self.h/2]

        points = [p1, p2, p3, p4]

        return spira.Path(points, width=1, gdslayer=RDD.M6, distance=3)

    def create_elementals(self, elems):

        jj = Junction()

        # FIXME: Automate this movement.
        jj.move(origin=jj.center, destination=(0,0))

        # FIXME: Rotation applies to parent cell.
        j1 = spira.SRef(jj, origin=(-1, 0), rotation=90)
        # j1.move(origin=j1.ref.center, destination=(0,0))
        j2 = spira.SRef(jj, origin=(10.5, 0), rotation=180)

        elems += j1
        elems += j2

        elems += self.top_routing
        elems += self.bot_routing

        return elems


if __name__ == '__main__':

    # from spira import settings
    # from spira.templates.library import library

    # settings.set_library(library)

    name = 'jj_squid'
    doc = 'Squid PCell with Junctions included.'

    spira.LOG.header('Running example: {}'.format(name))

    jj = JunctionSquid(width=10, height=3, w=5, h=0.5)
    jj.output(name=name)

    spira.LOG.end_print('Junction example finished')

