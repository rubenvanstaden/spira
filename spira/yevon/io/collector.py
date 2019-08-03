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


