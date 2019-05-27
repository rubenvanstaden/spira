import spira.all as spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __Elemental__
# from spira.yevon.rdd.gdsii_layer import LayerField
from spira.yevon.rdd.process_layer import ProcessField
from spira.core.parameters.variables import *
from spira.yevon.visualization.color import ColorField
from spira.yevon.geometry.coord import Coord, CoordField
from spira.yevon import utils
from spira.yevon.rdd.physical_layer import PhysicalLayer
from spira.yevon.rdd.purpose_layer import PurposeLayerField
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Label']


# class __Label__(gdspy.Label, __Elemental__):
class __Label__(__Elemental__):
    """  """

    text = StringField(default='no_text')
    process = ProcessField(default=RDD.PROCESS.VIRTUAL)
    purpose = PurposeLayerField(default=RDD.PURPOSE.TEXT)

    def __init__(self, position, **kwargs):
        super().__init__(position, **kwargs)

    def __eq__(self, other):
        return self.id == other.id

    def __deepcopy__(self, memo):
        c_label = self.modified_copy(
            position=deepcopy(self.position),
            gds_layer=deepcopy(self.gds_layer)
        )
        return c_label

    def convert_to_gdspy(self, transformation=None):
        T = self.transformation + transformation
        # self.transform(T)
        self.position = T.apply_to_coord(self.position)
        self.orientation = T.apply_to_angle(self.orientation)
        if isinstance(self.position, Coord):
            position = self.position.to_numpy_array()
        else:
            position = self.position
        ps = PhysicalLayer(self.process, self.purpose)
        layer = RDD.GDSII.EXPORT_LAYER_MAP[ps]
        return gdspy.Label(self.text,
            # deepcopy(self.position),
            position=position,
            anchor='o',
            rotation=self.orientation,
            layer=layer.number,
            texttype=layer.datatype
        )

    def encloses(self, ply):
        if isinstance(ply, spira.Polygon):
            return pyclipper.PointInPolygon(self.position, ply.shape.points) != 0
        elif isinstance(ply, (list, set, np.ndarray)):
            return pyclipper.PointInPolygon(self.position, ply) != 0
        else:
            raise ValueError('Not Implemented!')

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        c_label = self.modified_copy(position=self.position)
        if commit_to_gdspy:
            self.gdspy_commit = True
        return c_label

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = utils.move_algorithm(obj=self, midpoint=midpoint, destination=destination, axis=axis)
        dx, dy = np.array(d) - o
        super().translate(dx, dy)
        return self

    def id_string(self):
        return self.__repr__()


class Label(__Label__):
    """ Label that contains a text description.

    Example
    -------
    >>> lbl = spira.Label(text='P1', position=(0,0))
    >>> [SPiRA: Label] (P1 at (0,0), texttype 0)
    """

    route = StringField(default='no_route')
    orientation = NumberField(default=0)

    def __init__(self, position, **kwargs):

        # TODO: Convert to Point object.
        if isinstance(position, (list, tuple, set, np.ndarray)):
            self.position = list(position)
        elif isinstance(position, Coord):
            self.position = list([position[0], position[1]])
        else:
            raise ValueError('Position type not supported!')

        __Elemental__.__init__(self, **kwargs)
        # gdspy.Label.__init__(self,
        #     text=self.text,
        #     position=self.position,
        #     anchor=str('o'),
        #     rotation=self.orientation,
        #     # magnification=self.magnification,
        #     # x_reflection=self.reflection,
        #     layer=self.gds_layer.number,
        #     texttype=self.texttype
        # )

    def __repr__(self):
        if self is None:
            return 'Label is None!'
        return ("[SPiRA: Label] ({}, at ({}), texttype: {})").format(self.text, self.position, self.process)
        # params = [ self.text, self.position, self.rotation,
        #            self.magnification, self.reflection,
        #            self.layer, self.texttype ]
        # return ("[SPiRA: Label] (\"{0}\", at ({1[0]}, {1[1]}), " +
        #         "rot: {2}, mag: {3}, ref: {4}, layer: {5}, " +
        #         "texttype: {6})").format(*params)

    # def transform(self, transformation):
    #     self.position = transformation.apply_to_coord(self.position)
    #     self.orientation = transformation.apply_to_angle(self.orientation)
    #     return self

    # def transform_copy(self, transformation):
    #     port = self.__class__(
    #         name=self.name,
    #         gds_layer=deepcopy(self.gds_layer),
    #         midpoint=transformation.apply_to_coord(self.midpoint), 
    #         orientation=transformation.apply_to_angle(self.orientation)
    #     )
    #     return port





