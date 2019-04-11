import spira
from core import param
from core.initializer import ElementalInitializer


# class GroupElementals(ElementalInitializer):

#     _ID = 0

#     elementals = param.ElementalListField(fdef_name='create_elementals')

#     def __init__(self, name=None, elementals=None, **kwargs):
#         ElementalInitializer.__init__(self, **kwargs)

#         if elementals is not None:
#             self.ee = elementals

#         self._ID += 1

#     def __repr__(self):
#         return '[SPiRA: GroupElementals] id {} polygons {} labels {}'.format(self._ID, len(self.ee.polygons), len(self.ee.labels))

#     def __str__(self):
#         return self.__repr__()

#     def __iadd__(self, other):
#         if other is None:
#             return self
#         self.elementals += other
#         return self

#     def create_elementals(self, elems):
#         return elems


class Group(__Group__, __Element__):
    
    # def __init__(self, transformation=None, **kwargs):
    #     super(Group, self).__init__(transformation=transformation, **kwargs)
        
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
         

           