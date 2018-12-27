from spira.core.descriptor import DataFieldDescriptor
from spira.core.initializer import ElementalInitializer


# class __DesignRule__(ElementalInitializer):
#     doc = param
#
#
# class Width(__DesignRule__):
#     __type__ = list
#
#     def __init__(self, default=(0,0), **kwargs):
#         kwargs['default'] = self.__type__(default)
#         super().__init__(**kwargs)
#
#     def get_stored_value(self, obj):
#         value = obj.__store__[self.__name__]
#         return self.__type__(value)
#
#     # def __eq__(self, other):
#     #     print('Updating value {}'.format(self))
#     #     return obj.__store__[self.__name__] == other.value
#
#     def __set__(self, obj, value):
#         if isinstance(value, self.__type__):
#             obj.__store__[self.__name__] = value
#         elif isinstance(value, (set, tuple, np.ndarray)):
#             obj.__store__[self.__name__] = self.__type__(value)
#         else:
#             raise TypeError("Invalid type in setting value " +
#                             "of {} (expected {}): {}"
#                             .format(self.__class_, type(value)))
#
#
# def WidthField(polygons=[]):
#     """ Field definition for minimum and maximum widths. """
#     F = Width(default=(0,0))
#     return DataFieldDescriptor(default=F)
