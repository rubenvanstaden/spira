import spira.all as spira


RDD = spira.get_rule_deck()


class Density(__DoubleLayerDesignRule__):
    minimum = param.IntegerParameter()

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
                pos_elems = C.elements
            elif C.layer.number == self.layer2.number:
                neg_elems = C.elements

        fails = False

        Ap = self.get_layer_area(pos_elems)
        An = self.get_layer_area(neg_elems)

        if (Ap > 0) and (An > 0):
            presentage = 100 - (An/Ap)*100

            if presentage < self.minimum:
                fails = True
                message = '[DRC: Density ({})]: (layer1 {}, layer2 {}, extracted_value {}%, rule_value {}%)'.format('fail', self.layer1.number, self.layer2.number, int(round(presentage)), self.min)
                raise ValueError(message)
            else:
                fails = False

        return fails

