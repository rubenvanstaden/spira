from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.yevon.visualization.color import *
from spira.yevon.visualization.patterns import StippleParameter
from spira.core.parameters.processors import ProcessorTypeCast
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.variables import *
from spira.yevon.visualization.patterns import *


__all__ = [
    'DisplayStyle',
    'DisplayStyleSet',
    'DisplayStyleParameter'
]


class DisplayStyle(ParameterInitializer):
    """  """

    alpha = FloatParameter(default=1.0)
    edgewidth = FloatParameter(default=1.0)

    color = ColorParameter(default=COLOR_BLACK)
    edgecolor = ColorParameter(default=COLOR_BLACK)
    stipple = StippleParameter(default=STIPPLE_NONE)    

    def __str__(self):
        class_string = "[SPiRA: DisplayStyle] (color {}, stipple {}, alpha {}, edgewidth {})"
        return class_string.format(self.color.name, str(self.stipple), self.alpha, self.edgewidth)

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

    def __getitem__(self, value):
        for item in self:
            if item[0] == value:
                return item[1]
        return None


class ProcessorDisplayStyle(ProcessorTypeCast):
    def __init__(self):
        ProcessorTypeCast.__init__(self, DisplayStyle)

    def process(self, value, obj= None):
        if value is None:
            return DisplayStyle()
        else:
            return ProcessorTypeCast.process(self, value, obj)


def DisplayStyleParameter(local_name=None, restriction=None, preprocess=None,**kwargs):
    if not 'default' in kwargs:
        kwargs['default'] = None
    R = RestrictType(DisplayStyle) & restriction
    P = ProcessorDisplayStyle() + preprocess
    return RestrictedProperty(local_name, restriction=R, preprocess=P, **kwargs)




