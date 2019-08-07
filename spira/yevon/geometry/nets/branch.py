
# from spira.yevon import constants
# from spira.log import SPIRA_LOG as LOG
# from spira.yevon.filters.filter import Filter
# from spira.yevon.gdsii.elem_list import ElementList
# from spira.yevon.gdsii.polygon import Polygon
# from spira.yevon.gdsii.group import Group
# from spira.yevon.geometry.shapes.adapters import ShapeEdge
# from spira.yevon.process.purpose_layer import PurposeLayerParameter

# from copy import deepcopy
# from spira.core.parameters.variables import GraphParameter, StringParameter
# from spira.core.parameters.descriptor import Parameter
# from spira.yevon.geometry.coord import Coord
# from spira.yevon.vmodel.geometry import GeometryParameter
# from spira.yevon.geometry.ports.base import __Port__

from spira.yevon.geometry.nets import NetParameter
from spira.core.parameters.variables import *
from spira.core.parameters.initializer import ParameterInitializer, MetaInitializer


__all__ = ['Branch']


class MetaBranch(MetaInitializer):
    """

    """

    def __call__(cls, *params, **keyword_params):

        kwargs = cls.__map_parameters__(*params, **keyword_params)

        # print(kwargs)

        path = kwargs['path']
        kwargs['path'] = path[1:-1]
        s, t = path[0], path[-1]

        net = None
        if 'net' in kwargs:
            net = kwargs['net']
        else:
            raise ValueError('No net specified.')

        is_valid = False
        # FIXME: Has to test if path already exists.
        is_valid = all(i in net.branch_nodes for i in [s, t])

        for n in path[1:-1]:
            if 'device_reference' in net.g.node[n]:
                D = net.g.node[n]['device_reference']
                is_valid = (not D.is_valid_path())

        # print(is_valid)

        if is_valid is True:
            kwargs['source'] = s
            kwargs['target'] = t

        kwargs['is_valid'] = is_valid

        # print(kwargs)

        cls.__keywords__ = kwargs
        cls = super().__call__(**kwargs)
        return cls


class __Branch__(ParameterInitializer, metaclass=MetaBranch):

    doc = StringParameter()
    is_valid = BoolParameter(default=False)
    net = NetParameter()


class Branch(__Branch__):
    """ Branch path inside a graph net. A valid branch is a path
    between two branch nodes (source and target), and does not
    contain any other branch nodes in between. """

    source = NumberParameter()
    target = NumberParameter()
    path = ListParameter(default=[], doc='')

    def __init__(self, path, **kwargs):
        super().__init__(path=path, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Branch is None!'
        class_string = "[SPiRA: Branch] (source {}, target {}, count {})"
        return class_string.format(self.source, self.target, len(self.path))

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def id_string(self):
        return self.__repr__()

    def short_string(self):
        return "Branch [{}, {}]".format(self.source, self.target)





