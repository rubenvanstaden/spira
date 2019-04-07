import spira
from spira.core import param
from spira.lrc.rules import __DoubleLayerDesignRule__
from spira.core.initializer import ElementalInitializer


RDD = spira.get_rule_deck()


class Enclosure(__DoubleLayerDesignRule__):
    minimum = param.FloatField()

    def __repr__(self):
        return "'{}' must be enclosed by '{}' by at least {} micrometers.".format(self.layer1, self.layer2, self.minimum)

    def __str__(self):
        return self.__repr__()
        
    def apply(self, elems):
        pass

    # def apply(self, elems):

    #     pos_elems = spira.ElementList()
    #     neg_elems = spira.ElementList()

    #     for C in elems.dependencies():
    #         for S in C.elementals.sref:
    #             if S.ref.layer.number == self.layer1.number:
    #                 pos_elems = S.ref.elementals
    #                 C1 = S.ref

    #                 for C in elems.dependencies():
    #                     for S in C.elementals.sref:
    #                         if S.ref.layer.number == self.layer2.number:
    #                             neg_elems = S.ref.elementals
    #                             C2 = S.ref

    #                             fails = False

    #                             if pos_elems and neg_elems:
    #                                 P = pos_elems[0]
    #                                 M = neg_elems[0]

    #                                 space = self.minimum*1.0e+6

    #                                 x1 = abs(P.xmax - P.center[0])
    #                                 sx = (x1 + space)/x1

    #                                 p_copy = deepcopy(P)

    #                                 p_scale = p_copy.scale(scalex=sx, scaley=sx, center=P.center)

    #                                 p_overlap = p_scale | M

    #                                 if p_overlap:
    #                                     a1 = round(p_scale.ply_area*10e-9)
    #                                     a2 = round(p_overlap.ply_area*10e-9)

    #                                     if abs(a1 - a2) > 1e-9:
    #                                         fails = True

    #                                         P_error = ELayer(points=P.polygons,
    #                                                 number=C1.layer.number,
    #                                                 error_type=self.error)
    #                                         C1 += SRef(P_error)

    #                                         M_error = ELayer(points=M.polygons,
    #                                                 number=C2.layer.number,
    #                                                 error_type=self.error)
    #                                         C2 += SRef(M_error)

    #                                         print('\n ------ Surround Rules ------')
    #                                         print(self.layer1)
    #                                         print('Surround ({}): {}'.format('fail', self.minimum))
    #                                     else:
    #                                         fails = False
    #                                         print('\n ------ Surround Rules ------')
    #                                         print(self.layer1)
    #                                         print('Surround ({}): {}'.format('pass', self.minimum))

    #                             return fails
