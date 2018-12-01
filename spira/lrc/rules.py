import spira
from spira.kernel import parameters as param
from spira.kernel.parameters.initializer import BaseElement
from spira.kernel.parameters.descriptor import DataFieldDescriptor


class __DesignRule__(BaseElement):
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
    min = param.FloatField()
    max = param.FloatField()

    def __repr__(self):
        return 'Rule width: min={} max={}'.format(self.min, self.max)

    def apply(self, elems):
        return True


class Surround(__DoubleLayerDesignRule__):
    min = param.FloatField()

    def __repr__(self):
        return 'Rule surround: min={}'.format(self.min)

    # def apply(self, i, P, M):
    def apply(self, elems):

        pos_elems = spira.ElementList()
        neg_elems = spira.ElementList()

        for C in elems.dependencies():
            if C.layer.number == self.layer1.number:
                pos_elems = C.elementals
            elif C.layer.number == self.layer2.number:
                neg_elems = C.elementals

        fails = False

        if pos_elems and neg_elems:
            P = pos_elems[0]
            M = neg_elems[0]

            space = self.min*1.0e+6

            x1 = abs(P.xmax - P.center[0])
            sx = (x1 + space)/x1

            p_copy = P.clean_copy()

            p_scale = p_copy.scale(scalex=sx, scaley=sx, center=P.center)

            p_overlap = p_scale | M

            a1 = round(p_scale.ply_area*10e-9)
            a2 = round(p_overlap.ply_area*10e-9)

            if abs(a1 - a2) > 1e-9:
                fails = True
                print('\n ------ Surround Rules ------')
                print(self.layer1)
                print('Surround ({}): {}'.format('fail', self.min))
            else:
                fails = False
                print('\n ------ Surround Rules ------')
                print(self.layer1)
                print('Surround ({}): {}'.format('pass', self.min))

        return fails

        # if (P.gdslayer.number == self.layer1) and (M.gdslayer.number == self.layer2):
        #     space = self.min*1.0e+6
        #
        #     x1 = abs(P.xmax - P.center[0])
        #     sx = (x1 + space)/x1
        #
        #     p_copy = P.clean_copy()
        #
        #     p_scale = p_copy.scale(scalex=sx, scaley=sx, center=P.center)
        #
        #     p_overlap = p_scale | M
        #
        #     a1 = round(p_scale.ply_area*10e-9)
        #     a2 = round(p_overlap.ply_area*10e-9)
        #
        #     if abs(a1 - a2) > 1e-9:
        #         return True
        # return False


class Density(__DoubleLayerDesignRule__):
    min = param.IntegerField()

    # TODO: Detect holes in die polygon

    def __repr__(self):
        return 'Rule density: min={}'.format(self.min)

    def get_layer_area(self, elems):
        area = 0.0
        for e in elems:
            area += e.ply_area
        return area

    fails = True

    def apply(self, elems):

        pos_elems = spira.ElementList()
        neg_elems = spira.ElementList()

        for C in elems.dependencies():
            if C.layer.number == self.layer1.number:
                pos_elems = C.elementals
            elif C.layer.number == self.layer2.number:
                neg_elems = C.elementals

        # pos_elems = spira.ElementList()
        # neg_elems = spira.ElementList()
        # for e in elems:
        #     if e.gdslayer.number == self.layer1.number:
        #         if e.gdslayer.datatype == 0:
        #             pos_elems += e
        #         elif e.gdslayer.datatype == 68:
        #             neg_elems += e
        #         else:
        #             raise ValueError('Metal layer design rule not implemented.')

        Ap = self.get_layer_area(pos_elems)
        An = self.get_layer_area(neg_elems)

        if (Ap > 0) and (An > 0):
            presentage = 100 - (An/Ap)*100

            if presentage < self.min:
                fails = False
                print('\n ------ Design Rules ------')
                print(self.layer1)
                message = '[DRC: Density ({})]: (layer1 {}, layer2 {}, extracted_value {}%, rule_value {}%)'.format('fail', self.layer1.number, self.layer2.number, int(round(presentage)), self.min)
                raise ValueError(message)
            else:
                fails = True
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
