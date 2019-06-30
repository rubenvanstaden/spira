# from spira.core.typed_list import TypedList
# from spira.yevon.process.gdsii_layer import Layer
# from spira.yevon.process.layer import __Layer__
# from spira.core.parameters.restrictions import RestrictType
# from spira.core.parameters.descriptor import ParameterDescriptor


# __all__ = ['LayerList', 'LayerListParameter']


# class LayerList(TypedList):
#     """
#     Overload acces routines to get dictionary behaviour 
#     but without using the name as primary key.
#     """

#     __item_type__ = __Layer__

#     def __getitem__(self, key):
#         if isinstance(key, tuple):
#             for i in self._list:
#                 if i.key == key: 
#                     return i
#             raise IndexError("layer " + str(key) + " cannot be found in LayerList.")
#         elif isinstance(key, str):
#             for i in self._list:
#                 if i.name == key: 
#                     return i
#             raise IndexError("layer " + str(key) + " cannot be found in LayerList.")
#         else:
#             raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

#     def __setitem__(self, key, value):
#         if isinstance(key, tuple):
#             for i in range(0, len(self)):
#                 if self._list[i].key == key: 
#                     return self._list.__setitem__(self, i, value)
#             self._list.append(self, value)
#         elif isinstance(key, str):
#             for i in range(0, len(self)):
#                 if self._list[i].name == key: 
#                     return self._list.__setitem__(self, i, value)
#             self._list.append(self, value)
#         else:
#             raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

#     def __delitem__(self, key):
#         if isinstance(key, tuple):
#             for i in range(0, len(self)):
#                 if self._list.__getitem__(self, i).key == key: 
#                     return self._list.__delitem__(self, i)
#                 return
#             return self._list.__delitem__(self, key)
#         if isinstance(key, str):
#             for i in range(0, len(self)):
#                 if self._list.__getitem__(self, i).name == key: 
#                     return self._list.__delitem__(self, i)
#                 return
#             return self._list.__delitem__(self,key)
#         else:
#             raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

#     def __contains__(self, item):
#         if isinstance(item, Layer):
#             key = item.key
#         elif isinstance(item, tuple):
#             key = item
#         elif isinstance(item, str):
#             for i in self._list:
#                 if i.name == name: 
#                     return True
#             return False

#         if isinstance(key, tuple):
#             for i in self._list:
#                 if i.key == key:
#                     return True
#             return False

#     def __eq__(self, other):
#         return set(self) == set(other)

#     # def __hash__(self):
#     #     return do_hash(self)

#     def __fast_get_layer__(self, key):
#         for L in self._list:
#             if L.key == key:
#                 return L
#         return None

#     def index(self, item):
#         if isinstance(item, Layer):
#             key = item.key
#         elif isinstance(item, tuple):
#             key = item

#         if isinstance(key, tuple):
#             for i in range(0, len(self)):
#                 if self._list.__getitem__(self, i).key == key:
#                     return i
#             raise ValueError("layer " + key + " is not in LayerList")
#         if isinstance(item, str):
#             for i in range(0, len(self)):
#                 if self._list.__getitem__(self, i).name == item:
#                     return i
#             raise ValueError("layer " + item + " is not in LayerList")
#         else:
#             raise ValueError("layer " + item + " is not in LayerList")

#     def add(self, item, overwrite=False):
#         if isinstance(item, Layer):
#             if not item in self._list:
#                 self._list.append(item)
#             elif overwrite:
#                 self._list[item.key] = item
#                 return
#         elif isinstance(item, LayerList) or isinstance(item, list):
#             for s in item:
#                 self.add(s, overwrite)
#         elif isinstance(item, tuple):
#             if overwrite or (not item in self):
#                 self.add(Layer(number=item[0], datatype=item[1]), overwrite)
#         else:
#             raise ValueError('Invalid layer list item type.')

#     def append(self, other, overwrite = False):
#         return self.add(other, overwrite)

#     def extend(self, other, overwrite = False):
#         return self.add(other, overwrite)

#     def clear(self):
#         del self._list[:]


# class LayerListParameter(ParameterDescriptor):

#     __type__ = LayerList

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





