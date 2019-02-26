import spira
from spira import param
from spira.core.initializer import FieldInitializer


# Color Map: https://www.rapidtables.com/web/color/html-color-codes.html


class Color(FieldInitializer):
    """ Defines a color in terms of a name and RGB values. """

    name = param.StringField()
    red = param.FloatField(default=0.0)
    green = param.FloatField(default=0.0)
    blue = param.FloatField(default=0.0)

    def __init__(self, red=0.0, green=0.0, blue=0.0, **kwargs):
        super().__init__(red=red, green=green, blue=blue, **kwargs)

    def rgb_tuple(self):
        return (self.red, self.green, self.blue)

    def numpy_array(self):
        import numpy
        return numpy.array([self.red, self.green, self.blue])

    def set(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def hexcode(self):
        return '#{:02x}{:02x}{:02x}'.format(int(self.red), int(self.green), int(self.blue))

    def __eq__(self, other):
        return other.red == self.red and other.green == self.green and other.blue == self.blue

    def __neq__(self, other):
        return other.red != self.red or other.green != self.green or other.blue != self.blue

    def __str__(self):
        return self.name


COLOR_BLACK = Color(name='black', red=0, green=0, blue=0)
COLOR_WHITE = Color(name='white', red=255, green=255, blue=255)
COLOR_GREEN = Color(name='green', red=0, green=128, blue=0)
COLOR_LIGHT_GREEN = Color(name='light green', red=144, green=238, blue=144)
COLOR_BLUE = Color(name='blue', red=0, green=0, blue=255)
COLOR_CYAN = Color(name='cyan', red=0, green=255, blue=255)
COLOR_YELLOW = Color(name='yellow', red=255, green=255, blue=0)
COLOR_SILVER = Color(name='silver', red=192, green=192, blue=192)
COLOR_GRAY = Color(name='gray', red=128, green=128, blue=128)
COLOR_LIGHT_GRAY = Color(name='light gray', red=211, green=211, blue=211)
COLOR_BLUE_VIOLET = Color(name='blue violet', red=238, green=130, blue=238)
COLOR_GHOSTWHITE = Color(name='ghost white', red=248, green=248, blue=255)
COLOR_SALMON = Color(name='salmon', red=250, green=128, blue=144)
COLOR_CADET_BLUE = Color(name='cadet blue', red=95, green=158, blue=160)
COLOR_TURQUOISE = Color(name='turquoise', red=95, green=158, blue=160)
COLOR_CORAL = Color(name='coral', red=255, green=127, blue=80)
COLOR_AZURE = Color(name='azure', red=240, green=255, blue=255)
COLOR_PLUM = Color(name='plum', red=221, green=160, blue=221)
COLOR_DARK_SLATE_GREY = Color(name='dark slate grey', red=47, green=79, blue=79)
COLOR_DARKSEA_GREEN = Color(name='darksea green', red=143, green=188, blue=143)


# COLOR_BLACK = Color(name = "black", red = 0, green = 0, blue = 0)
# COLOR_WHITE = Color(name = "white", red = 1, green = 1, blue = 1)
# COLOR_GHOSTWHITE = Color(name = "ghost white", red = 0.97, green = 0.97, blue = 1)
# COLOR_RED = Color(name = "red", red = 1, green = 0, blue = 0)
# COLOR_GREEN = Color(name = "green", red = 0, green = 1, blue = 0)
# COLOR_BLUE = Color(name = "blue", red = 0, green = 0, blue = 1)
# COLOR_CYAN = Color(name = "cyan", red = 0, green = 1, blue = 1)
# COLOR_YELLOW = Color(name = "yellow", red = 1, green = 1, blue = 0)
# COLOR_MAGENTA = Color(name = "magenta", red = 1, green = 0, blue = 1)
# COLOR_DARK_GREEN = Color(name = "dark green", red = 0.5, green = 0.31, blue = 0)
# COLOR_DEEP_GREEN = Color(name = "deep green", red = 0, green = 0.5, blue = 0.5)
# COLOR_ORANGE = Color(name = "ORANGE", red = 1, green = 0.62, blue = 0.62)
# COLOR_PURPLE = Color(name = "PURPLE", red = 0.75, green = 0.5, blue = 1)
# COLOR_CHAMPAGNE = Color(name = "CHAMPAGNE", red = 0.98, green = 0.84, blue = 0.65)
# COLOR_BLUE_VIOLET = Color(name = "BLUE-VIOLET", red = 0.44, green = 0.0, blue = 1.0)
# COLOR_BLUE_CRAYOLA = Color(name = "BLUE (CRAYOLA)", red = 0.12, green = 0.46, blue = 1.0)
# COLOR_SCARLET = Color(name = "SCARLET", red = 1.0, green = 0.14, blue = 0.0)
# COLOR_SANGRIA = Color(name = "SANGRIA", red=0.57, green = 0.0, blue = 0.04)
# COLOR_SILVER = Color(name = "SILVER", red=0.75, green = 0.75, blue = 0.75)
# COLOR_TITANIUM_YELLOW = Color(name = "TITANIUM_YELLOW", red=0.93, green = 0.90, blue = 0.0)
# COLOR_GRAY = Color(name="GRAY", red=0.55, green=0.52, blue = 0.55)
# COLOR_COPPER = Color(name="COPPER", red=0.72, green = 0.45, blue = 0.20)




