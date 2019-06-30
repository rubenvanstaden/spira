import gdspy
import pyclipper
import numpy as np
import spira.all as spira

from numpy.linalg import norm
from spira.core.parameters.variables import *
from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.geometry.coord import Coord
from spira.yevon.process.process_layer import ProcessParameter
from spira.yevon.process.purpose_layer import PurposeLayerParameter
from spira.yevon.process.physical_layer import PLayer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class __Port__(ParameterInitializer):
    """  """

    doc = StringParameter()
    name = StringParameter()
    locked = BoolParameter(default=False)


class __PhysicalPort__(__Port__):

    process = ProcessParameter(default=RDD.PROCESS.VIRTUAL)
    purpose = PurposeLayerParameter(default=RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED)
    local_pid = StringParameter(default='none_local_pid')
    text_type = NumberParameter(default=RDD.GDSII.TEXT)

    # FIXME: Look at how this is done with elements.
    def __add__(self, other):
        """
        Allows for this type of operations:

        Example
        -------
        >>> midpoint = self.jj1.ports['P2'] + [-5, 0]
        """
        if other is None: return self
        p1 = Coord(self.midpoint[0], self.midpoint[1]) + Coord(other[0], other[1])
        return p1

    def __sub__(self, other):
        """
        Allows for this type of operations:

        Example
        -------
        >>> midpoint = self.jj1.ports['P2'] + [-5, 0]
        """
        if other is None: return self
        p1 = Coord(self.midpoint[0], self.midpoint[1]) - Coord(other[0], other[1])
        return p1

    @property
    def layer(self):
        return PLayer(self.process, self.purpose)

    @property
    def key(self):
        return (self.name, self.layer, self.midpoint[0], self.midpoint[1])

    @property
    def normal(self):
        dx = np.cos((self.orientation)*np.pi/180)
        dy = np.sin((self.orientation)*np.pi/180)
        return np.array([self.midpoint, self.midpoint + np.array([dx,dy])])

    def flatcopy(self, level=-1):
        E = self.copy(transformation=self.transformation)
        E.transform_copy(self.transformation)
        return E

    def encloses(self, points):
        from spira.yevon.utils import clipping
        return clipping.encloses(coord=self.midpoint, points=points)

    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(self.midpoint)
        return self

    def transform_copy(self, transformation):
        m = transformation.apply_to_coord(self.midpoint)
        return self.__class__(midpoint=m)

    def move(self, coordinate):
        self.midpoint.move(coordinate)
        return self

    def distance(self, other):
        return norm(np.array(self.midpoint) - np.array(other.midpoint))



