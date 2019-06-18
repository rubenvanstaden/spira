import gdspy
import numpy as np

from copy import deepcopy
from spira.yevon.gdsii.group import __Group__
from spira.yevon.aspects.geometry import __GeometryAspects__


class CellAspects(__Group__, __GeometryAspects__):

    # FIXME: Replace this with the new BoundaryBox class.
    @property
    def bbox(self):
        D = deepcopy(self)
        cell = D.get_gdspy_cell()
        bbox = cell.get_bounding_box()
        if bbox is None: bbox = ((0,0),(0,0))
        return np.array(bbox)



