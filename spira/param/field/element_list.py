# from spira.gdsii.lists.elemental_list import ElementList
# from spira.core.descriptor import DataFieldDescriptor
# class ElementalListField(DataFieldDescriptor):
#     __type__ = ElementList

#     def __init__(self, default=[], **kwargs):
#         kwargs['default'] = self.__type__(default)
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
#         obj.__store__[self.__name__] = value
#         return value

