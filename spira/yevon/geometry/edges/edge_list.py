# from spira.core.typed_list import TypedList
# from spira.core.parameters.descriptor import ParameterDescriptor
# from spira.core.parameters.restrictions import RestrictType
# from spira.yevon.geometry.edges.edges import __Edge__


# class EdgeList(TypedList):
#     """ List containing nets for each metal plane in a cell. """

#     __item_type__ = __Edge__

#     def __repr__(self):
#         if len(self._list) == 0: print('Edgelist is empty')
#         return '\n'.join('{}'.format(k) for k in enumerate(self._list))

#     def __str__(self):
#         return self.__repr__()

#     def __getitem__(self, key):
#         if isinstance(key, int):
#             return self._list[key]
#         else:
#             return self.get_from_label(key)

#     def __delitem__(self, key):
#         for i in range(0, len(self._list)):
#             if self._list[i] is key:
#                 return list.__delitem__(self._list, i)

#     def flat_copy(self, level = -1):
#         el = EdgeList()
#         for e in self._list:
#             el += e.flat_copy(level)
#         return el

#     def move(self, position):
#         for c in self._list:
#             c.move(position)
#         return self

#     def movecopy(self, position):
#         T = self.__class__()
#         for c in self._list:
#             T.append(c.movecopy(position))
#         return T

#     def transform_copy(self, transformation):
#         T = self.__class__()
#         for c in self._list:
#             T.append(c.transform_copy(transformation))
#         return T

#     def transform(self, transformation):
#         for c in self._list:
#             c.transform(transformation)
#         return self


# class EdgeListParameter(ParameterDescriptor):

#     __type__ = EdgeList

#     def __init__(self, default=[], **kwargs):
#         kwargs['default'] = self.__type__(default)
#         kwargs['restrictions'] = RestrictType([self.__type__])
#         super().__init__(**kwargs)

#     def __repr__(self):
#         return ''

#     def __str__(self):
#         return ''

#     def call_param_function(self, obj):
#         f = self.get_param_function(obj)
#         value = f(self.__type__())
#         if value is None:
#             value = self.__type__()
#         new_value = self.__cache_parameter_value__(obj, value)
#         return new_value

