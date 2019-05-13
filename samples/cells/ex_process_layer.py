import spira.all as spira
from spira.yevon import process as pc
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class BasicProcess(spira.Cell):

    def create_elementals(self, elems):

        e1 = pc.Rectangle(p1=(0,0), p2=(10*1e6, 10*1e6), ps_layer=RDD.PLAYER.COU)

        elems += e1

        return elems


if __name__ == '__main__':

    D = BasicProcess()
    D.output()

