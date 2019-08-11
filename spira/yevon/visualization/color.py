import numpy as np
import spira.all as spira

from spira.core.parameters.variables import StringParameter, IntegerParameter
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.core.parameters.restrictions import RestrictType


# Color Map: https://www.rapidtables.com/web/color/html-color-codes.html


class Color(ParameterInitializer):
    """ Defines a color in terms of a name and RGB values. """

    name = StringParameter(default='black')
    red = IntegerParameter(default=0)
    green = IntegerParameter(default=0)
    blue = IntegerParameter(default=0)

    def __init__(self, red=0, green=0, blue=0, **kwargs):
        super().__init__(red=red, green=green, blue=blue, **kwargs)

    def __eq__(self, other):
        return other.red == self.red and other.green == self.green and other.blue == self.blue

    def __neq__(self, other):
        return other.red != self.red or other.green != self.green or other.blue != self.blue

    def __repr__(self):
        _str = "[SPiRA: Color] (name '{}', hex {}, rgb ({}, {}, {})"
        return _str.format(self.name, self.hexcode, self.red, self.green, self.blue)

    def __str__(self):
        return self.__repr__()

    @property
    def hexcode(self):
        return '#{:02x}{:02x}{:02x}'.format(int(self.red), int(self.green), int(self.blue))

    @property
    def norm(self):
        return (self.red/255, self.green/255, self.blue/255)

    def rgb_tuple(self):
        return (self.red, self.green, self.blue)

    def numpy_array(self):
        return np.array([self.red, self.green, self.blue])

    def tint(self, factor=0.0):
        """ Make color lighter. """
        r = self.red   + (255-self.red)   * factor
        g = self.green + (255-self.green) * factor
        b = self.blue  + (255-self.blue)  * factor
        return Color(int(r), int(g), int(b))
        
    def shade(self, factor=0.0):
        """ Make color darker. """
        r = self.red   * (1 - factor)
        g = self.green * (1 - factor)
        b = self.blue  * (1 - factor)
        return Color(int(r), int(g), int(b))

    def set(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


COLOR_KEYNOTE_BLACK = Color(name='white', red=34, green=34, blue=34)
COLOR_KEYNOTE_GRAY = Color(name='white', red=167, green=170, blue=169)
COLOR_BLACK = Color(name='black', red=0, green=0, blue=0)
COLOR_WHITE = Color(name='white', red=255, green=255, blue=255)
COLOR_GREEN = Color(name='green', red=0, green=128, blue=0)
COLOR_LIGHT_GREEN = Color(name='light green', red=144, green=238, blue=144)
COLOR_BLUE = Color(name='blue', red=0, green=0, blue=255)
COLOR_CYAN = Color(name='cyan', red=0, green=255, blue=255)
COLOR_YELLOW = Color(name='yellow', red=255, green=255, blue=0)
COLOR_BLUE_VIOLET = Color(name='blue violet', red=238, green=130, blue=238)
COLOR_GHOSTWHITE = Color(name='ghost white', red=248, green=248, blue=255)
COLOR_SILVER = Color(name='silver', red=192, green=192, blue=192)
COLOR_GRAY = Color(name='gray', red=128, green=128, blue=128)
COLOR_LIGHT_GRAY = Color(name='light gray', red=211, green=211, blue=211)
COLOR_SALMON = Color(name='salmon', red=250, green=128, blue=144)
COLOR_SALMON_LIGHT = Color(name='salmon light', red=255, green=160, blue=122)
COLOR_SALMON_DARK = Color(name='salmon dark', red=233, green=150, blue=122)
COLOR_POWER_BLUE = Color(name='power blue', red=176, green=224, blue=230)
COLOR_AQUAMARINE = Color(name='aquamarine', red=127, green=255, blue=212)
COLOR_TURQUOISE_PALE = Color(name='turquoise pale', red=175, green=238, blue=238)
COLOR_TURQUOISE_DARK = Color(name='turquoise dark', red=0, green=206, blue=209)
COLOR_TURQUOISE_MEDIUM = Color(name='turquoise medium', red=72, green=209, blue=204)
COLOR_TURQUOISE = Color(name='turquoise', red=95, green=158, blue=160)
COLOR_CORAL = Color(name='coral', red=255, green=127, blue=80)
COLOR_CORAL_LIGHT = Color(name='coral light', red=240, green=128, blue=128)
COLOR_PLUM = Color(name='plum', red=221, green=160, blue=221)
COLOR_VIOLET = Color(name='violet', red=238, green=130, blue=238)
COLOR_ORCHID = Color(name='orchid', red=218, green=112, blue=214)
COLOR_SEA_GREEN_DARK = Color(name='sea green dark', red=143, green=188, blue=143)
COLOR_SEA_GREEN = Color(name='sea green', red=46, green=139, blue=87)
COLOR_SEA_GREEN_MEDIUM = Color(name='sea green medium', red=60, green=179, blue=113)
COLOR_SEA_GREEN_LIGHT = Color(name='sea green light', red=32, green=178, blue=170)
COLOR_SEA_GREEN_PALE = Color(name='sea green pale', red=152, green=251, blue=152)
COLOR_CADET_BLUE = Color(name='cadet blue', red=95, green=158, blue=160)
COLOR_AZURE = Color(name='azure', red=240, green=255, blue=255)
COLOR_DARK_SLATE_GREY = Color(name='dark slate grey', red=47, green=79, blue=79)
COLOR_INDIAN_RED = Color(name='indian red', red=205, green=92, blue=92)
COLOR_STEEL_BLUE = Color(name='steel blue', red=70, green=130, blue=180)
COLOR_DARK_MAGENTA = Color(name='dark magenta', red=139, green=0, blue=139)
COLOR_ROYAL_BLUE = Color(name='royal blue', red=65, green=105, blue=225)


def ColorParameter(red=0, green=0, blue=0, **kwargs):
    from spira.yevon.visualization.color import Color
    if 'default' not in kwargs:
        kwargs['default'] = Color(red=0, green=0, blue=0, **kwargs)
    R = RestrictType(Color)
    return ParameterDescriptor(restrictions=R, **kwargs)




