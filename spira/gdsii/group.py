import spira
from spira import param
from spira.core.initializer import ElementalInitializer


# RDD = spira.get_rule_deck()


class GroupElementals(ElementalInitializer):

    _ID = 0

    elementals = param.ElementalListField(fdef_name='create_elementals')

    def __init__(self, name=None, elementals=None, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

        if elementals is not None:
            self.ee = elementals

        self._ID += 1

    def __repr__(self):
        return '[SPiRA: GroupElementals] id {} polygons {} labels {}'.format(self._ID, len(self.ee.polygons), len(self.ee.labels))

    def __str__(self):
        return self.__repr__()

    def __iadd__(self, other):
        if other is None:
            return self
        self.elementals += other
        return self

    def create_elementals(self, elems):
        return elems

