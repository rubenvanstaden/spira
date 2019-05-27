from spira.yevon.rdd.all import *
from spira.yevon.rdd import RULE_DECK_DATABASE as RDD

# ---------------------------------- GDSII ---------------------------------------

RDD.GDSII = DataTree()
RDD.GDSII.TEXT = 64
RDD.GDSII.UNIT = 1e-6
RDD.GDSII.GRID = 1e-12
RDD.GDSII.PRECISION = 1e-9

# ---------------------------------- Process ---------------------------------------

RDD.PROCESS = ProcessTree()

RDD.PROCESS.VIRTUAL = ProcessLayer(name='Virtual Layer', symbol='VIR')
RDD.PROCESS.LABEL = ProcessLayer(name='Contact 3', symbol='LBL')

RDD.PROCESS.GND = ProcessLayer(name='Ground Plane', symbol='GND')
RDD.PROCESS.SKY = ProcessLayer(name='Sky Plane', symbol='SKY')
RDD.PROCESS.M1 = ProcessLayer(name='Metal 1', symbol='M1')
RDD.PROCESS.M2 = ProcessLayer(name='Metal 2', symbol='M2')
RDD.PROCESS.M3 = ProcessLayer(name='Metal 3', symbol='M3')
RDD.PROCESS.C1 = ProcessLayer(name='Contact 1', symbol='C1')
RDD.PROCESS.C2 = ProcessLayer(name='Contact 2', symbol='C2')
RDD.PROCESS.C3 = ProcessLayer(name='Contact 3', symbol='C3')

# ---------------------------------- Layer Purposes ----------------------------------

RDD.PURPOSE = ProcessTree()

RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', symbol='GND')
RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', symbol='METAL')
RDD.PURPOSE.SKY = PurposeLayer(name='Sky plane polygons', symbol='SKY')
RDD.PURPOSE.PROTECTION = PurposeLayer(name='Protection layer for via structures', symbol='PRO')
RDD.PURPOSE.VIA = PurposeLayer(name='Via layer', symbol='VIA')
RDD.PURPOSE.JUNCTION = PurposeLayer(name='Junction layer', symbol='JJ')
RDD.PURPOSE.NTRON = PurposeLayer(name='nTron layer', symbol='NTRON')
RDD.PURPOSE.HOLE = PurposeLayer(name='Polygon holes', symbol='HOLE')
RDD.PURPOSE.DUMMY = PurposeLayer(name='Sky plane polygons', symbol='DUM')
RDD.PURPOSE.TEXT = PurposeLayer(name='Sky plane polygons', symbol='TXT')
RDD.PURPOSE.BOUNDARY_BOX = PurposeLayer(name='Bounding Box', symbol='BBOX', doc='')

# ---------------------------------- Port Purposes ------------------------------------

RDD.PURPOSE.PORT = ProcessTree()
RDD.PURPOSE.PORT.CONTACT = PurposeLayer(name='Port ports specified by the designer', symbol='TERM')
RDD.PURPOSE.PORT.EDGE_ENABLED = PurposeLayer(name='Edge', symbol='EDGEE', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.EDGE_DISABLED = PurposeLayer(name='Edge', symbol='EDGED', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.DIRECTION = PurposeLayer(name='Arrow', symbol='DIR', doc='Layer that represents the direction of a polygon edge terminal.')

# ---------------------------------- Error Purposes ------------------------------------

RDD.PURPOSE.ERROR = ProcessTree()
RDD.PURPOSE.ERROR.SPACING = PurposeLayer(name='nTron layer', symbol='SP')
RDD.PURPOSE.ERROR.MIN_WIDTH = PurposeLayer(name='nTron layer', symbol='MAXW')
RDD.PURPOSE.ERROR.MAX_WIDTH = PurposeLayer(name='nTron layer', symbol='MINW')
RDD.PURPOSE.ERROR.ENCLOSURE = PurposeLayer(name='nTron layer', symbol='ENC')
RDD.PURPOSE.ERROR.OVERLAP = PurposeLayer(name='nTron layer', symbol='OVR')
RDD.PURPOSE.ERROR.DENSITY = PurposeLayer(name='nTron layer', symbol='OVR')

# ------------------------------- DEFAULT ----------------------------------

RDD.PLAYER = PhysicalTree()

RDD.PORT = PropertyTree()
RDD.PORT.WIDTH = 0.5

# --------------------------------- Name Generator -------------------------------------

class TechAdminTree(DynamicDataTree):
    """ A technology tree with a name generator. """
    def initialize(self):
        from spira.yevon.gdsii.generators import NameGenerator
        self.NAME_GENERATOR = NameGenerator(
            prefix_attribute='__name_prefix__',
            counter_zero=0,
            process_name=''
        )

RDD.ADMIN = TechAdminTree()

# ------------------------------ Display Resources -------------------------------

# class DisplayDatabase(DynamicDataTree):
#     def initialize(self):
#         from spira.yevon.rdd.physical_layer import PhysicalLayer
#         from ipkiss.visualisation.display_style import DisplayStyle, DisplayStyleSet
#         from ipkiss.visualisation import color
#         from spira.yevon.visualization import *

#         self.PREDEFINED_STYLE_SETS = TechnologyTree()        

#         DISPLAY_BLACK = DisplayStyle(color=color.COLOR_BLACK, edgewidth = 0.0)
#         DISPLAY_WHITE = DisplayStyle(color=color.COLOR_WHITE, edgewidth = 0.0)
#         DISPLAY_INVERSION = DisplayStyle(color=color.COLOR_BLUE, alpha = 0.5, edgewidth = 1.0)
#         DISPLAY_DF = DisplayStyle(color=color.COLOR_GREEN, alpha = 0.5, edgewidth = 1.0)
#         DISPLAY_LF = DisplayStyle(color=color.COLOR_YELLOW, alpha = 0.5, edgewidth = 1.0)
#         DISPLAY_TEXT = DisplayStyle(color=color.COLOR_MAGENTA, alpha = 0.5, edgewidth = 1.0)
#         DISPLAY_HOLE = DisplayStyle(color=color.COLOR_RED, alpha = 0.5, edgewidth = 1.0)
#         DISPLAY_ALIGNMENT = DisplayStyle(color=color.COLOR_CYAN, alpha = 0.5, edgewidth = 1.0) 

#         style_set = DisplayStyleSet()
#         style_set.background = DISPLAY_WHITE
#         process_display_order = [ 
#             RDD.PROCESS.GND,
#             RDD.PROCESS.M1,
#             RDD.PROCESS.C1,
#             RDD.PROCESS.M2,
#             RDD.PROCESS.C2,
#             RDD.PROCESS.M3,
#             RDD.PROCESS.C3,
#             RDD.PROCESS.SKY,
#         ]

#         for process in process_display_order:
#             style_set += [
#                 (PhysicalLayer(process, RDD.PURPOSE.LF_AREA),   DISPLAY_INVERSION),
#                 (PhysicalLayer(process, RDD.PURPOSE.DF_AREA),   DISPLAY_INVERSION),
#                 (PhysicalLayer(process, RDD.PURPOSE.DF.MARKER), DISPLAY_ALIGNMENT),
#                 (PhysicalLayer(process, RDD.PURPOSE.LF.MARKER), DISPLAY_ALIGNMENT),
#                 (PhysicalLayer(process, RDD.PURPOSE.LF.LINE),   DISPLAY_DF),
#                 (PhysicalLayer(process, RDD.PURPOSE.LF.ISLAND), DISPLAY_DF),
#                 (PhysicalLayer(process, RDD.PURPOSE.DF.TEXT),   DISPLAY_TEXT),
#                 (PhysicalLayer(process, RDD.PURPOSE.DF.HOLE),   DISPLAY_HOLE),
#                 (PhysicalLayer(process, RDD.PURPOSE.DF.TRENCH), DISPLAY_LF),
#                 (PhysicalLayer(process, RDD.PURPOSE.DF.SQUARE), DISPLAY_HOLE),
#             ]

#         self.PREDEFINED_STYLE_SETS.PURPOSE_HIGHLIGHT  = style_set

# RDD.DISPLAY = DisplayDatabase()
# # RDD.overwrite_allowed.append('DISPLAY')
