import networkx as nx

from spira.core.typed_list import TypedList
from spira.yevon.geometry.nets.branch import __Branch__
from spira.core.parameters.variables import FloatParameter
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.core.parameters.restrictions import RestrictType


# NOTE: Algoritm before adding branch to branch list.
# 1. Check that the branch does not already exist.
# 2. Check that the source ana target is valid branch nodes.


class BranchList(TypedList):
    """ 
    Store all valid net branches in a list. This allows
    us to use the list index as a unique ID and apply operations
    on all branches simultantiously.

    Notes
    -----
    Branches can alos be accessed using the inductance name, making
    this implementation compatible with JoSIM and InductEx.
    """

    __item_type__ = __Branch__

    def __repr__(self):
        if len(self._list) == 0:
            print('Branch list is empty')
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._list[key]
        else:
            return self.get_from_label(key)

    def __delitem__(self, key):
        for i in range(0, len(self._list)):
            if self._list[i] is key:
                return list.__delitem__(self._list, i)

    def __contains__(self, item):
        return self.is_stored(item)

    def flat_copy(self, level = -1):
        el = BranchList()
        for e in self._list:
            el += e.flat_copy(level)
        return el

    def move(self, position):
        for c in self._list:
            c.move(position)
        return self

    def move_copy(self, position):
        T = self.__class__()
        for c in self._list:
            T.append(c.move_copy(position))
        return T

    def transform_copy(self, transformation):
        T = self.__class__()
        for c in self._list:
            T.append(c.transform_copy(transformation))
        return T

    def transform(self, transformation):
        for c in self._list:
            c.transform(transformation)
        return self

    def append(self, item):
        if isinstance(item, self.__item_type__):
            if not self.is_stored(item):
                self._list.append(item)
        elif isinstance(item, list):
            # self._list.extend(item)
            for b in item:
                if not self.is_stored(b):
                    self._list.append(b)
        else:
            error_message = "You are trying to add an element of type {} to {}. You can only add elements of type {}."
            raise ValueError(error_message.format(str(type(item)), str(self.__class__), str(self.__item_type__)))

    def is_stored(self, item):
        for e in self._list:
            return (item == e)

    # Implement a method to check that 'device_reference ' is 
    # alays a SRef or port, boefore construction.
    def id_branch(self, i, s, t):
        number = 'ID: {}'.format(BranchPaths._ID)

        s = self.g.node[s]['device_reference'].net_source()
        t = self.g.node[t]['device_reference'].net_target()

        # if issubclass(type(Ds), spira.SRef):
        #     source = 'source: {}'.format(Ds.reference.name)
        # elif isinstance(Ds, spira.Port):
        #     source = 'source: {}'.format(Ds.name)

        # if issubclass(type(Dt), spira.SRef):
        #     target = 'target: {}'.format(Dt.reference.name)
        # elif isinstance(Ds, spira.Port):
        #     target = 'target: {}'.format(Dt.name)

        return "\n".join([number, s, t])



class BranchListParameter(ParameterDescriptor):
    __type__ = BranchList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        kwargs['restrictions'] = RestrictType([self.__type__])
        super().__init__(**kwargs)

    def __repr__(self):
        return ''

    def __str__(self):
        return ''

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f(self.__type__(), 100)
        if value is None:
            value = self.__type__()
        new_value = self.__cache_parameter_value__(obj, value)
        return new_value


