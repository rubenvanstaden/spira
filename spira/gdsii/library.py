import os
import gdspy
import spira

from spira import param
from spira.gdsii.io import import_gds
from spira.core.lists import ElementList
from spira.gdsii.lists.cell_list import CellList
from spira.core.initializer import FieldInitializer
from spira.core.mixin.gdsii_output import OutputMixin


RDD = spira.get_rule_deck()


class __Library__(gdspy.GdsLibrary, FieldInitializer):

    __mixins__ = [OutputMixin]


class LibraryAbstract(__Library__):

    grid = param.FloatField(default=RDD.GDSII.GRID)
    grids_per_unit = param.DataField(fdef_name='create_grids_per_unit')
    units_per_grid = param.DataField(fdef_name='create_units_per_grid')

    def create_grids_per_unit(self):
        return self.unit / self.grid

    def create_units_per_grid(self):
        return self.grid / self.unit

    def validate_parameters(self):
        if self.grid > self.unit:
            raise Exception('The grid should be smaller than the unit.')
        return True

    def __add__(self, other):
        if isinstance(other, spira.Cell):
            self.cells.add(other)
            for d in other.dependencies():
                self.cells.add(d)
        elif isinstance(other, spira.ElementList):
            for d in other.dependencies():
                self.cells.add(d)
        return self

    def add_pcell(self, pcell):
        self.pcells += pcell

    def get_cell(self, cell_name):
        for C in self.cells:
            if C.name == cell_name:
                return C
        return None

    @property
    def to_gdspy(self):
        for c in self.cells:
            cell = c.gdspycell
            if c.name in self.cell_dict.keys():
                self.cell_dict[c.name] = cell
            else:
                self.add(cell)

    def referenced_structures(self):
        referred_to_list = list()
        for s in self.structures:
            referred_to_list.append(s.dependencies())
        return referred_to_list

    @property
    def device_types(self):
        devices = [0, 1]
        for cell in self.structures:
            devices.append(cell.gdsdatatype)
        return devices


class Library(LibraryAbstract):
    """ Library contains all the cell and pcell informartion
    of a given layout connected to a RDD. """
    def __init__(self, name='spira_library', infile=None, **kwargs):
        super().__init__(name=name, infile=None, **kwargs)
        self.cells = CellList()
        self.pcells = ElementList()
        self.graphs = list()

    def __repr__(self):
        return "[SPiRA: Library(\'{}\')] ({} cells)".format(
            self.name,
            self.cells.__len__()
        )

    def __str__(self):
        return self.__repr__()









