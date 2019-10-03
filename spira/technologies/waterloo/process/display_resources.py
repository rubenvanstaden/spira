from spira.yevon.process.all import *
from spira.yevon.process import get_rule_deck

RDD = get_rule_deck()

# ------------------------------ Display Resources -------------------------------

class DisplayDatabase(LazyDatabase):

    def initialize(self):
        from spira.yevon.visualization import color
        from spira.yevon.visualization.display import DisplayStyle, DisplayStyleSet

        DISPLAY_SALMON = DisplayStyle(color=color.COLOR_SALMON, edgewidth=1.0)
        DISPLAY_SALMON_LIGHT = DisplayStyle(color=color.COLOR_SALMON_LIGHT, edgewidth=1.0)
        DISPLAY_SALMON_DARK = DisplayStyle(color=color.COLOR_SALMON_DARK, edgewidth=1.0)
        DISPLAY_TURQUOISE = DisplayStyle(color=color.COLOR_TURQUOISE, edgewidth=1.0)
        DISPLAY_TURQUOISE_PALE = DisplayStyle(color=color.COLOR_TURQUOISE_PALE, edgewidth=1.0)
        DISPLAY_TURQUOISE_MEDIUM = DisplayStyle(color=color.COLOR_TURQUOISE_MEDIUM, edgewidth=1.0)
        DISPLAY_CORAL = DisplayStyle(color=color.COLOR_CORAL, alpha=0.5, edgewidth=1.0)
        DISPLAY_CORAL_LIGHT = DisplayStyle(color=color.COLOR_CORAL_LIGHT, alpha=0.5, edgewidth=1.0)
        DISPLAY_WHITE = DisplayStyle(color=color.COLOR_WHITE, alpha=0.5, edgewidth=1.0)
        DISPLAY_LIGHT_GREEN = DisplayStyle(color=color.COLOR_LIGHT_GREEN, edgewidth=1.0)
        DISPLAY_SEA_GREEN_DARK = DisplayStyle(color=color.COLOR_SEA_GREEN_DARK, edgewidth=1.0)
        DISPLAY_SEA_GREEN_MEDIUM = DisplayStyle(color=color.COLOR_SEA_GREEN_MEDIUM, edgewidth=1.0)
        DISPLAY_SEA_GREEN_PALE = DisplayStyle(color=color.COLOR_SEA_GREEN_PALE, edgewidth=1.0)
        DISPLAY_GRAY = DisplayStyle(color=color.COLOR_GRAY, edgewidth=1.0)
        DISPLAY_BLACK = DisplayStyle(color=color.COLOR_BLACK, edgewidth=1.0)
        DISPLAY_AZURE = DisplayStyle(color=color.COLOR_AZURE, edgewidth=1.0)
        DISPLAY_DARK_MAGENTA = DisplayStyle(color=color.COLOR_DARK_MAGENTA, edgewidth=1.0)
        DISPLAY_YELLOW = DisplayStyle(color=color.COLOR_YELLOW, edgewidth=1.0)
        DISPLAY_ROYAL_BLUE = DisplayStyle(color=color.COLOR_ROYAL_BLUE, edgewidth=1.0)
        DISPLAY_GREEN = DisplayStyle(color=color.COLOR_GREEN, edgewidth=1.0)
        DISPLAY_SILVER = DisplayStyle(color=color.COLOR_SILVER, edgewidth=1.0)
        DISPLAY_CYAN = DisplayStyle(color=color.COLOR_CYAN, edgewidth=1.0)
        DISPLAY_PLUM = DisplayStyle(color=color.COLOR_PLUM, edgewidth=1.0)
        DISPLAY_POWER_BLUE = DisplayStyle(color=color.COLOR_POWER_BLUE, edgewidth=1.0)
        DISPLAY_INDIAN_RED = DisplayStyle(color=color.COLOR_INDIAN_RED, edgewidth=1.0)
        DISPLAY_AQUAMARINE = DisplayStyle(color=color.COLOR_AQUAMARINE, edgewidth=1.0)

        style_set = DisplayStyleSet()
        style_set.background = DISPLAY_WHITE

        style_set += [
            (RDD.PLAYER.METAL, DISPLAY_WHITE),
            (RDD.PLAYER.M5.METAL, DISPLAY_SALMON_LIGHT),
            (RDD.PLAYER.M5.DEVICE_METAL, DISPLAY_SALMON),
            (RDD.PLAYER.M5.CIRCUIT_METAL, DISPLAY_SALMON_LIGHT),
            (RDD.PLAYER.M5.ROUTE, DISPLAY_SALMON),
            (RDD.PLAYER.M5.HOLE, DISPLAY_SALMON),
            (RDD.PLAYER.M5.BBOX, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.M5.PORT_CONTACT, DISPLAY_YELLOW),
            (RDD.PLAYER.M5.PORT_BRANCH, DISPLAY_AZURE),
            (RDD.PLAYER.M5.PORT_DIRECTION, DISPLAY_SALMON),
            (RDD.PLAYER.M5.PORT_PIN, DISPLAY_GRAY),
            (RDD.PLAYER.M5.PORT_TERMINAL, DISPLAY_GRAY),
            (RDD.PLAYER.M5.PORT_DUMMY, DISPLAY_INDIAN_RED),
            (RDD.PLAYER.M5.INSIDE_EDGE_DISABLED, DISPLAY_WHITE),

            (RDD.PLAYER.M6.METAL, DISPLAY_TURQUOISE_MEDIUM),
            (RDD.PLAYER.M6.DEVICE_METAL, DISPLAY_TURQUOISE_PALE),
            (RDD.PLAYER.M6.CIRCUIT_METAL, DISPLAY_TURQUOISE),
            (RDD.PLAYER.M6.ROUTE, DISPLAY_TURQUOISE),
            (RDD.PLAYER.M6.HOLE, DISPLAY_TURQUOISE),
            (RDD.PLAYER.M6.BBOX, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.M6.PORT_CONTACT, DISPLAY_TURQUOISE_PALE),
            (RDD.PLAYER.M6.PORT_BRANCH, DISPLAY_POWER_BLUE),
            (RDD.PLAYER.M6.PORT_DIRECTION, DISPLAY_TURQUOISE_PALE),
            (RDD.PLAYER.M6.PORT_PIN, DISPLAY_GRAY),
            (RDD.PLAYER.M6.PORT_TERMINAL, DISPLAY_GRAY),
            (RDD.PLAYER.M6.PORT_DUMMY, DISPLAY_INDIAN_RED),
            (RDD.PLAYER.M6.INSIDE_EDGE_DISABLED, DISPLAY_WHITE),

            (RDD.PLAYER.R5.METAL, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.R5.DEVICE_METAL, DISPLAY_SEA_GREEN_DARK),
            (RDD.PLAYER.R5.CIRCUIT_METAL, DISPLAY_SEA_GREEN_PALE),
            (RDD.PLAYER.R5.ROUTE, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.R5.HOLE, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.R5.BBOX, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.R5.PORT_CONTACT, DISPLAY_CORAL_LIGHT),
            (RDD.PLAYER.R5.PORT_DIRECTION, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.R5.PORT_PIN, DISPLAY_GRAY),
            (RDD.PLAYER.R5.PORT_TERMINAL, DISPLAY_GRAY),
            (RDD.PLAYER.R5.PORT_DUMMY, DISPLAY_INDIAN_RED),
            (RDD.PLAYER.R5.INSIDE_EDGE_DISABLED, DISPLAY_WHITE),

            (RDD.PLAYER.I5.VIA, DISPLAY_SILVER),
            (RDD.PLAYER.I5.PORT_CONTACT, DISPLAY_AQUAMARINE),

            (RDD.PLAYER.C5R.VIA, DISPLAY_SEA_GREEN_MEDIUM),
            (RDD.PLAYER.C5R.PORT_CONTACT, DISPLAY_GREEN),

            (RDD.PLAYER.J5.JUNCTION, DISPLAY_YELLOW),
            (RDD.PLAYER.J5.PORT_CONTACT, DISPLAY_PLUM),
        ]

        self.STYLE_SET = style_set

RDD.DISPLAY = DisplayDatabase()


