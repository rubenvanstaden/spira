import spira
import spira.kernel.parameters as param
# from spira.rdd import get_rule_deck


# RDD = spira.get_rule_deck()


class Via(spira.Cell):
    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return "[SPiRA: Via(\'{}\', {} elements)] ({} sref, {} polygons, {} labels)".format(
                        self.name, 
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)


class Junction(spira.Cell):

    # m1 = param.IntegerField(default=RDD.METALS.M5.LAYER)
    # m2 = param.IntegerField(default=RDD.METALS.M6.LAYER)

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return "[SPiRA: Junction(\'{}\', {} elements)] ({} sref, {} polygons, {} labels)".format(
                        self.name, 
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)


class Ntron(spira.Cell):
    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return "[SPiRA: Ntron(\'{}\', {} elements)] ({} sref, {} polygons, {} labels)".format(
                        self.name, 
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)



