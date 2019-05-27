from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.descriptor import DataFieldDescriptor
from spira.yevon.visualization.color import *
from spira.yevon.visualization.patterns import StippleField
from spira.core.parameters.processors import ProcessorTypeCast
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.variables import *
from spira.yevon.visualization.patterns import *


__all__ = [
    'DisplayStyle',
    'DisplayStyleSet',
    'DisplayStyleField'
]


class DisplayStyle(FieldInitializer):
    """  """

    color = ColorField(default=COLOR_BLACK)
    edgecolor = ColorField(default=COLOR_BLACK)
    stipple = StippleField(default=STIPPLE_NONE)    
    # alpha = RestrictedProperty(restriction = RESTRICT_FRACTION, default = 1.0)
    alpha = FloatField(default=1.0)

    def __str__(self):
        return "DisplayStyle : color: %s - edgecolor: %s - stipple: %s - alpha: %f - edgewidth: %f - visible: %s" %(str(self.color),str(self.edgecolor),str(self.stipple), self.alpha,self.edgewidth,self.visible)

    def blend(self, other, fraction_first_color = 0.33):
        result_color_red = fraction_first_color * self.color.red + (1.0-fraction_first_color) * other.color.red 
        result_color_green = fraction_first_color * self.color.green + (1.0-fraction_first_color) * other.color.green 
        result_color_blue = fraction_first_color * self.color.blue + (1.0-fraction_first_color) * other.color.blue 
        result_color = Color(
            name="#%02X%02X%02X" % (result_color_red, result_color_green, result_color_blue),
            red = result_color_red,
            green = result_color_green,
            blue = result_color_blue)
        result_ds = DisplayStyle(
            color = result_color,
            edgecolor = self.edgecolor,
            stipple = self.stipple,
            alpha = self.alpha)
        return result_ds


class DisplayStyleSet(list):
    pass


class ProcessorDisplayStyle(ProcessorTypeCast):
    def __init__(self):
        ProcessorTypeCast.__init__(self, DisplayStyle)

    def process(self, value, obj= None):
        if value is None:
            return DisplayStyle()
        else:
            return ProcessorTypeCast.process(self, value, obj)


def DisplayStyleField(local_name=None, restriction=None, preprocess=None,**kwargs):
    if not 'default' in kwargs:
        kwargs['default'] = None
    R = RestrictType(DisplayStyle) & restriction
    P = ProcessorDisplayStyle() + preprocess
    return RestrictedProperty(local_name, restriction=R, preprocess=P, **kwargs)




