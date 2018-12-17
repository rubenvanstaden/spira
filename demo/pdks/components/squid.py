import spira
from spira import param
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class PhysicalJunction(spira.Cell):

    p1 = param.ListField()
    p2 = param.ListField()
    layer = param.LayerField()

    def create_elementals(self, elems):
        elems += spira.Rectangle(point1=self.p1, point2=self.p2, layer=self.layer)

        return elems


class Squid(spira.Cell):

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
        con = 6
        jj = PhysicalJunction(p1=[-self.w/con, -self.h/2],
                              p2=[self.w/con, self.h/2],
                              layer=RDD.J5)

        elems += spira.SRef(jj, origin=(0, 0))
        elems += spira.SRef(jj, origin=(self.width*1e6, 0))

        elems += self.top_routing
        elems += self.bot_routing

        return elems

# ----------------------------------------------------------

if __name__ == '__main__':

    name = 'SQUID_PCell'

    from spira import settings
    from spira.templates.library import library

    settings.set_library(library)

    spira.LOG.header('Running example: {}'.format(name))

    squid = Squid(width=10, height=3, midpoint=5, w=5, h=0.5)
    squid.output(name=name)

    spira.LOG.end_print('SQUID example finished')



