import spira.all as spira
from spira.core import param
from spira.yevon.gdsii.base import __Group__, __Elemental__


class Group(__Group__, __Elemental__):

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)
    
    def flat_copy(self, level=-1):
        if not level == 0:
            return self.elementals.flat_copy(level).transform(self.transformation)
        else:
            return spira.ElementList(self.elementals)

    def expand_transform(self):
        if not self.transformation.is_identity():
            self.elementals.transform(self.transformation)
            self.transformation = None  

    def __eq__(self, other):
            return (self.elementals == other.elementals) and (self.transformation == other.transformation)


           