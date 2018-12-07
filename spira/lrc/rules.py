import spira
from spira.kernel import parameters as param
from spira.kernel.parameters.initializer import BaseElement
from spira.kernel.parameters.descriptor import DataFieldDescriptor
from spira.rdd import get_rule_deck
from spira.lpe.layers import *


RDD = get_rule_deck()


class __DesignRule__(BaseElement):
    violate = param.BoolField()
    doc = param.StringField()
    name = param.StringField()


class __SingleLayerDesignRule__(__DesignRule__):
    """ Rule applying to a specific layer """
    layer1 = param.LayerField()


class __DoubleLayerDesignRule__(__DesignRule__):
    """ Rule applying to a specific layer """
    layer1 = param.LayerField()
    layer2 = param.LayerField()


class Width(__SingleLayerDesignRule__):
    minimum = param.FloatField()
    maximum = param.FloatField()
    error = param.IntegerField(default=RDD.PURPOSE.ERROR.MIN_WIDTH.datatype)

    def __repr__(self):
        return 'Rule width: min={} max={}'.format(self.minimum, self.maximum)

    def apply(self, elems):
        fails = False
        if self.violate:
            fails = True
        return fails


class Surround(__DoubleLayerDesignRule__):
    minimum = param.FloatField()
    error = param.IntegerField(default=RDD.PURPOSE.ERROR.SPACING.datatype)

    def __repr__(self):
        return 'Rule surround: min={}'.format(self.minimum)

    def apply(self, elems):

        pos_elems = spira.ElementList()
        neg_elems = spira.ElementList()

        # print(elems)

        for C in elems.dependencies():
            for S in C.elementals.sref:
                if S.ref.layer.number == self.layer1.number:
                    pos_elems = S.ref.elementals
                    C1 = S.ref

                    for C in elems.dependencies():
                        for S in C.elementals.sref:
                            if S.ref.layer.number == self.layer2.number:
                                neg_elems = S.ref.elementals
                                C2 = S.ref

                                fails = False

                                if pos_elems and neg_elems:
                                    P = pos_elems[0]
                                    M = neg_elems[0]

                                    space = self.minimum*1.0e+6

                                    x1 = abs(P.xmax - P.center[0])
                                    sx = (x1 + space)/x1

                                    p_copy = deepcopy(P)

                                    p_scale = p_copy.scale(scalex=sx, scaley=sx, center=P.center)

                                    p_overlap = p_scale | M
                                    # print(M)

                                    if p_overlap:
                                        a1 = round(p_scale.ply_area*10e-9)
                                        a2 = round(p_overlap.ply_area*10e-9)

                                        if abs(a1 - a2) > 1e-9:
                                            fails = True

                                            P_error = ELayer(points=P.polygons,
                                                    number=C1.layer.number,
                                                    error_type=self.error)
                                            C1 += SRef(P_error)

                                            M_error = ELayer(points=M.polygons,
                                                    number=C2.layer.number,
                                                    error_type=self.error)
                                            C2 += SRef(M_error)

                                            print('\n ------ Surround Rules ------')
                                            print(self.layer1)
                                            print('Surround ({}): {}'.format('fail', self.minimum))
                                        else:
                                            fails = False
                                            print('\n ------ Surround Rules ------')
                                            print(self.layer1)
                                            print('Surround ({}): {}'.format('pass', self.minimum))

                                return fails


class Density(__DoubleLayerDesignRule__):
    minimum = param.IntegerField()
    error = param.IntegerField(default=RDD.PURPOSE.ERROR.DENSITY.datatype)

    # TODO: Detect holes in die polygon

    def __repr__(self):
        return 'Rule density: min={}'.format(self.minimum)

    def get_layer_area(self, elems):
        area = 0.0
        for e in elems:
            area += e.ply_area
        return area

    def apply(self, elems):

        pos_elems = spira.ElementList()
        neg_elems = spira.ElementList()

        for C in elems.dependencies():
            if C.layer.number == self.layer1.number:
                pos_elems = C.elementals
            elif C.layer.number == self.layer2.number:
                neg_elems = C.elementals

        fails = False

        Ap = self.get_layer_area(pos_elems)
        An = self.get_layer_area(neg_elems)

        if (Ap > 0) and (An > 0):
            presentage = 100 - (An/Ap)*100

            if presentage < self.minimum:
                fails = True
                print('\n ------ Design Rules ------')
                print(self.layer1)
                message = '[DRC: Density ({})]: (layer1 {}, layer2 {}, extracted_value {}%, rule_value {}%)'.format('fail', self.layer1.number, self.layer2.number, int(round(presentage)), self.min)
                raise ValueError(message)
            else:
                fails = False
                print('\n ------ Design Rules ------')
                print(self.layer1)
                print('Density ({}): {}%'.format('pass', int(round(presentage))))

        return fails


def WidthField(min=0, max=0, **kwargs):
    """ Field definition for minimum and maximum widths. """
    F = Width(min=min, max=max, **kwargs)
    return DataFieldDescriptor(default=F)


def SurroundField(min=0, **kwargs):
    """ Field definition for minimum and maximum widths. """
    F = Surround(min=min, **kwargs)
    return DataFieldDescriptor(default=F, **kwargs)


def DensityField(min=0, max=0, **kwargs):
    """ Field definition for minimum and maximum widths. """
    F = Density(min=min, **kwargs)
    return DataFieldDescriptor(default=F)
