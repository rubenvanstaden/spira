from spira.param.field.typed_list import TypedList
class PortList(TypedList):
    """

    """

    def __repr__(self):
        if len(self._list) == 0: 
            print('PortList is empty')
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, i):
        from spira.gdsii.elemental.sref import SRef
        from spira.gdsii.cell import Cell
        from spira.gdsii.elemental.polygons import Polygons

        if isinstance(i, str):
            for port in self._list:
                if port.name == i:
                    return port._copy()
                    # return copy(port)
                    # return deepcopy(port)
        else:
            return self._list[i]

