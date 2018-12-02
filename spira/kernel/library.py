import os
import spira
import gdspy
import pathlib

from spira.kernel.parameters.field.element_list import ElementList

from spira.kernel.io import import_gds
from spira.kernel.mixins import OutputMixin
from spira.kernel.parameters.initializer import BaseLibrary


class __Library__(gdspy.GdsLibrary, BaseLibrary):

    _ID = 0

    __mixins__ = [OutputMixin]


class Library(__Library__):
    """

    """

    def __init__(self, name='spira_library', infile=None, **kwargs):
        from spira.kernel.cell import CellList
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

    # def __add__(self, other):
    #     if isinstance(other, spira.Cell):
    #         self.cells += other
    #         for d in other.dependencies():
    #             self.cells += d
    #     elif isinstance(other, spira.ElementList):
    #         for d in other.dependencies():
    #             self.cells += d
    #         # for s in other.sref:
    #         #     self.cells += s.ref
    #     return self

    def __add__(self, other):
        from spira.kernel.cell import CellList
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

    @property
    def to_gdspy(self):
        for c in self.cells:
            # FIXME: Add unit test for gdspy interfacing.
            # cd = gdspy.current_library.cell_dict
            cell = c.gdspycell
            if c.name in self.cell_dict.keys():
                self.cell_dict[c.name] = cell
                # self.add(self.cell_dict[c.name])
            else:
                # self.cell_dict
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
