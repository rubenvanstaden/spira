import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from spira.yevon.gdsii.base import __LayerElement__
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import Coord, CoordParameter
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Label']


class __Label__(__LayerElement__):
    """ Base class for label element. """

    text = StringParameter(default='no_text')

    def __init__(self, position, **kwargs):
        super().__init__(position=position, **kwargs)

    def encloses(self, ply):
        if isinstance(ply, spira.Polygon):
            return pyclipper.PointInPolygon(self.position, ply.shape.points) != 0
        elif isinstance(ply, (list, set, np.ndarray)):
            return pyclipper.PointInPolygon(self.position, ply) != 0
        else:
            raise ValueError('Not Implemented!')

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        c_label = self.copy(position=self.position)
        if commit_to_gdspy: self.gdspy_commit = True
        return c_label

    def id_string(self):
        return self.__repr__()


class Label(__Label__):
    """ Label that contains a text description.

    Example
    -------
    >>> lbl = spira.Label(text='P1', position=(0,0))
    >>> [SPiRA: Label] (P1 at (0,0), texttype 0)
    """

    position = CoordParameter(default=(0,0))
    orientation = NumberParameter(default=0)

    def __init__(self, position, **kwargs):
        super().__init__(position=position, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Label is None!'
        string = "[SPiRA: Label] ({} at ({}), layer {})"
        return string.format(self.text, self.position, self.layer.name)






