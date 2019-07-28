import gdspy
from spira.core.parameters.initializer import ParameterInitializer


class __Collector__(ParameterInitializer):

    def __init__(self, **kwargs):
        self.reset()
        super().__init__(**kwargs)

    def reset(self):
        return self


class ListCollector(__Collector__):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._list = {}

    def __iadd__(self, item):
        self._list.update(item)
        return self

    def reset(self):
        return self

    def cells(self):
        return self._list.values()


# class ListCollector(__Collector__):

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._list = []

#     def __iadd__(self, item_list):
#         # print(item_list)
#         # self._list += item_list
#         self._list.append(item_list)
#         return self

#     def reset(self):
#         return self

#     def output(self):
#         return self._list


# class GdspyCollector(__Collector__):

#     def __init__(self, library, **kwargs):
#         super().__init__(**kwargs)
#         self._gdspy_library = library

#     def __iadd__(self, item):
#         print(item)
#         self._gdspy_library.add(item)
#         return self

#     def reset(self):
#         return self

#     def output(self):
#         return self._gdspy_library.cell_dict.items()

#     def library(self):
#         return self._gdspy_library



