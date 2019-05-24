import os
import gdspy
import spira.all as spira

from spira.core.parameters.variables import *
from spira.yevon.io import import_gds
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.gdsii.cell_list import CellList
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.descriptor import DataField
from spira.core.mixin import MixinBowl
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class __Library__(FieldInitializer, MixinBowl):

    def __add__(self, other):
        if isinstance(other, spira.Cell):
            self.cells.add(other)
            for d in other.dependencies():
                self.cells.add(d)
        elif isinstance(other, spira.ElementalList):
            for d in other.dependencies():
                self.cells.add(d)
        return self

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, index):
        return self.cells[index]

    def __contains__(self, item):
        return self.cells.__contains__(item)

    def __eq__(self, other):
        if not isinstance(other, Library):
            return False
        if len(self.cells) != len(other.cells):
            return False
        for struct1, struct2 in zip(self.cells, other.cells):
            if (struct1.name != struct2.name):
                return False
            if (struct1 != struct2):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class LibraryAbstract(gdspy.GdsLibrary, __Library__):

    grid = FloatField(default=RDD.GDSII.GRID)
    grids_per_unit = DataField(fdef_name='create_grids_per_unit')
    units_per_grid = DataField(fdef_name='create_units_per_grid')

    def create_grids_per_unit(self):
        return self.unit / self.grid

    def create_units_per_grid(self):
        return self.grid / self.unit

    def validate_parameters(self):
        if self.grid > self.unit:
            raise Exception('The grid should be smaller than the unit.')
        return True

    def referenced_structures(self):
        referred_to_list = list()
        for s in self.cells:
            referred_to_list.append(s.dependencies())
        return referred_to_list

    def get_cell(self, cell_name):
        for C in self.cells:
            if C.name == cell_name:
                return C
        return None

    def is_empty(self):
        return len(self.cells) == 0

    def clear(self):
        self.cells.clear()


class Library(LibraryAbstract):
    """ Library contains all the cell and pcell informartion
    of a given layout connected to a RDD. 
    
    Examples
    --------
    >>> lib = spira.Library(name='LIB')
    """
    def __init__(self, name='spira_library', infile=None, **kwargs):
        super().__init__(name=name, infile=None, **kwargs)
        self.cells = CellList()
        self.graphs = list()

    def __repr__(self):
        return "[SPiRA: Library(\'{}\')] ({} cells)".format(
            self.name,
            self.cells.__len__()
        )

    def __str__(self):
        return self.__repr__()









