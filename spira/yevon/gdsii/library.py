import os
import gdspy

from spira.core.parameters.variables import *
from spira.yevon.gdsii.cell import Cell
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.cell_list import CellList
from spira.core.parameters.descriptor import Parameter
from spira.core.mixin import MixinBowl
from spira.yevon.gdsii.unit_grid import UnitGridContainer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class Library(UnitGridContainer, MixinBowl):
    """ 
    Library contains all the cell and pcell informartion
    of a given layout connected to a RDD. 

    Examples
    --------
    >>> lib = spira.Library(name='LIB')
    """

    name = StringParameter(doc='Unique name for the library.')
    accessed = TimeParameter(doc='Timestamp at which the library was accessed.')
    modified = TimeParameter(doc='Timestamp at which the library was modified.')

    def __init__(self, name='spira_library', infile=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.cells = CellList()
        self.graphs = list()

    def __repr__(self):
        class_string = "[SPiRA: Library(\'{}\')] ({} cells)"
        return class_string.format(self.name, self.cells.__len__())

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, index):
        return self.cells[index]

    def __contains__(self, item):
        return self.cells.__contains__(item)

    def __iadd__(self, other):
        if isinstance(other, Cell):
            self.cells.add(other)
            for d in other.dependencies():
                self.cells.add(d)
        elif isinstance(other, ElementList):
            for d in other.dependencies():
                self.cells.add(d)
        return self

    def __eq__(self, other):
        if not isinstance(other, Library):
            return False
        if len(self.cells) != len(other.cells):
            return False
        for cell1, cells in zip(self.cells, other.cells):
            if cell1.name != cell2.name:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def referenced_cells(self):
        referred_to_list = CellList()
        for c in self.cells:
            referred_to_list.append(c.dependencies())
        return referred_to_list

    def get_cell(self, cell_name):
        for C in self.cells:
            if C.name == cell_name:
                return C
        return None

    def is_empty(self):
        return len(self.cells) == 0


