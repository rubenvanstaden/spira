from spira.yevon.process.all import *
from spira.yevon.process import RULE_DECK_DATABASE as RDD

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

        style_set = DisplayStyleSet()
        style_set.background = DISPLAY_WHITE

        style_set += [
            (RDD.PLAYER.METAL, DISPLAY_WHITE),
            (RDD.PLAYER.M1.METAL, DISPLAY_SALMON),
            # (RDD.PLAYER.M1.ROUTE, DISPLAY_SALMON),
            (RDD.PLAYER.M1.HOLE, DISPLAY_SALMON),
            (RDD.PLAYER.M1.BBOX, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.M1.PORT_CONTACT, DISPLAY_SALMON_LIGHT),
            (RDD.PLAYER.M1.PORT_BRANCH, DISPLAY_SALMON_DARK),
            (RDD.PLAYER.M1.PORT_PIN, DISPLAY_GRAY),
            (RDD.PLAYER.M1.PORT_DUMMY, DISPLAY_SEA_GREEN_PALE),
            (RDD.PLAYER.M1.PORT_DIRECTION, DISPLAY_SALMON),
            (RDD.PLAYER.M1.INSIDE_EDGE_ENABLED, DISPLAY_GRAY),
            (RDD.PLAYER.M1.INSIDE_EDGE_DISABLED, DISPLAY_WHITE),
            
            (RDD.PLAYER.M2.METAL, DISPLAY_TURQUOISE),
            # (RDD.PLAYER.M2.ROUTE, DISPLAY_TURQUOISE),
            (RDD.PLAYER.M2.HOLE, DISPLAY_TURQUOISE),
            (RDD.PLAYER.M2.BBOX, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.M2.PORT_CONTACT, DISPLAY_TURQUOISE_PALE),
            (RDD.PLAYER.M2.PORT_BRANCH, DISPLAY_SEA_GREEN_DARK),
            (RDD.PLAYER.M2.PORT_PIN, DISPLAY_GRAY),
            (RDD.PLAYER.M2.PORT_DUMMY, DISPLAY_SEA_GREEN_PALE),
            (RDD.PLAYER.M2.PORT_DIRECTION, DISPLAY_TURQUOISE_PALE),
            (RDD.PLAYER.M2.INSIDE_EDGE_ENABLED, DISPLAY_GRAY),
            (RDD.PLAYER.M2.INSIDE_EDGE_DISABLED, DISPLAY_WHITE),
            
            (RDD.PLAYER.M3.METAL, DISPLAY_CORAL),
            # (RDD.PLAYER.M3.ROUTE, DISPLAY_CORAL),
            (RDD.PLAYER.M3.HOLE, DISPLAY_CORAL),
            (RDD.PLAYER.M3.BBOX, DISPLAY_LIGHT_GREEN),
            (RDD.PLAYER.M3.PORT_CONTACT, DISPLAY_CORAL_LIGHT),
            (RDD.PLAYER.M3.PORT_PIN, DISPLAY_GRAY),
            (RDD.PLAYER.M3.PORT_DUMMY, DISPLAY_SEA_GREEN_PALE),
            (RDD.PLAYER.M3.PORT_DIRECTION, DISPLAY_CORAL),
            (RDD.PLAYER.M3.INSIDE_EDGE_ENABLED, DISPLAY_GRAY),
            (RDD.PLAYER.M3.INSIDE_EDGE_DISABLED, DISPLAY_WHITE),
        ]

        # process_display_order = [ 
        #     RDD.PROCESS.M1,
        #     RDD.PROCESS.M2,
        #     RDD.PROCESS.M3,
        #     RDD.PROCESS.M4,
        #     RDD.PROCESS.M5,
        #     RDD.PROCESS.M6,
        #     RDD.PROCESS.M7,
        # ]

        # for process in process_display_order:
        #     style_set += [
        #         (PhysicalLayer(process, RDD.PURPOSE.METAL), DISPLAY_INVERSION),
        #         (PhysicalLayer(process, RDD.PURPOSE.ROUTE), DISPLAY_INVERSION),
        #         (PhysicalLayer(process, RDD.PURPOSE.HOLE), DISPLAY_ALIGNMENT),
        #         (PhysicalLayer(process, RDD.PURPOSE.BBOX), DISPLAY_ALIGNMENT),
        #         (PhysicalLayer(process, RDD.PURPOSE.PORT_DIRECTION), DISPLAY_DF),
        #         (PhysicalLayer(process, RDD.PURPOSE.INSIDE_EDGE_ENABLED), DISPLAY_DF),
        #         (PhysicalLayer(process, RDD.PURPOSE.INSIDE_EDGE_DISABLED), DISPLAY_TEXT),
        #     ]

        self.STYLE_SET = style_set

RDD.DISPLAY = DisplayDatabase()


