import spira.all as spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import utils

from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __Elemental__

from spira.core.parameters.variables import *
from spira.yevon.visualization.color import ColorField
from spira.yevon.rdd.gdsii_layer import LayerField
from spira.core.parameters.descriptor import DataField
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon.rdd.physical_layer import PhysicalLayerField
from spira.yevon.geometry.vector import Vector
from spira.core.parameters.descriptor import RestrictedParameter
from spira.core.parameters.initializer import FieldInitializer
from spira.yevon.rdd.process_layer import ProcessField
from spira.yevon.rdd.purpose_layer import PurposeLayerField
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class __Port__(FieldInitializer):
    """  """

    doc = StringField()
    name = StringField()


class __PhysicalPort__(__Port__):

    process = ProcessField(default=RDD.PROCESS.VIRTUAL)
    purpose = PurposeLayerField(default=RDD.PURPOSE.PORT.EDGE_DISABLED)
    locked = BoolField(default=True)
    local_pid = StringField(default='none_local_pid')
    text_type = NumberField(default=RDD.GDSII.TEXT)

    def __add__(self, other):
        if other is None: return self
        p1 = Coord(self.midpoint[0], self.midpoint[1]) + Coord(other[0], other[1])
        return p1

    def flat_copy(self, level=-1):
        E = self.modified_copy(transformation=self.transformation)
        E.transform_copy(self.transformation)
        return E

    def encloses(self, points):
        return pyclipper.PointInPolygon(self.midpoint, points) != 0

    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(self.midpoint)
        return self

    def move(self, coordinate):
        self.midpoint.move(coordinate)
        return self

    def distance(self, other):
        return norm(np.array(self.midpoint) - np.array(other.midpoint))

    def connect(self, S, P):
        """ Connects the port to a specific polygon in a cell reference. """
        self.node_id = '{}_{}'.format(S.ref.name, P.id)

    @property
    def normal(self):
        dx = np.cos((self.orientation)*np.pi/180)
        dy = np.sin((self.orientation)*np.pi/180)
        return np.array([self.midpoint, self.midpoint + np.array([dx,dy])])

    @property
    def key(self):
        return (self.name, self.gds_layer.number, self.midpoint[0], self.midpoint[1])


