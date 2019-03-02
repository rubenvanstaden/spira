from spira.rdd.all import *
from spira.visualization import color
from spira.rdd.layer import PurposeLayer
from spira.rdd import RULE_DECK_DATABASE as RDD

# -------------------------------- Initialize ------------------------------------

RDD.name = 'MiTLL'
RDD.desc = 'Process fabrication data for the MiTLL process from the USA.'

# ---------------------------------- GDSII ---------------------------------------

RDD.GDSII = DataTree()
RDD.GDSII.TEXT = 18
RDD.GDSII.TERM_WIDTH = 0.2*1e6
RDD.GDSII.UNIT = 1e-6
RDD.GDSII.GRID = 1e-11
RDD.GDSII.PRECISION = 1e-9

# Overwrite default general rules
RDD.PURPOSE.TERM = PurposeLayer(
    name='Terminal ports specified by the designer',
    datatype=19,
    symbol='TERM'
)

# --------------------------------- Metals --------------------------------------

RDD.LAYER = ProcessTree()

RDD.L0 = ProcessTree()
RDD.L0.LAYER = Layer(name='L0', number=3)
RDD.L0.MIN_SIZE = 2.0 
RDD.L0.MAX_WIDTH = 20.0
# RDD.L0.COLOR = '#DEB887'
# RDD.L0.COLOR = 
RDD.L0.COLOR = color.COLOR_CORAL

RDD.M0 = ProcessTree()
RDD.M0.LAYER = Layer(name='M0', number=1)
RDD.M0.MIN_SIZE = 0.5
RDD.M0.MAX_WIDTH = 20.0
RDD.M0.COLOR = '#DA70D6'

RDD.M1 = ProcessTree()
RDD.M1.LAYER = Layer(name='M1', number=10)
RDD.M1.MIN_SIZE = 0.5
RDD.M1.MAX_WIDTH = 20.0
RDD.M1.COLOR = '#FFB6C1'

RDD.M2 = ProcessTree()
RDD.M2.LAYER = Layer(name='M2', number=20)
RDD.M2.MIN_SIZE = 0.35
RDD.M2.MAX_WIDTH = 20.0
# RDD.M2.COLOR = '#F0E68C'
RDD.M2.COLOR = color.COLOR_CORAL

RDD.M3 = ProcessTree()
RDD.M3.LAYER = Layer(name='M3', number=30)
RDD.M3.MIN_SIZE = 0.35
RDD.M3.MAX_WIDTH = 20.0
# RDD.M3.COLOR = '#FA8072'
RDD.M3.COLOR = color.COLOR_CORAL

RDD.M4 = ProcessTree()
RDD.M4.LAYER = Layer(name='M4', number=40)
RDD.M4.MIN_SIZE = 0.35
RDD.M4.MAX_WIDTH = 20.0
# RDD.M4.COLOR = '#EF9631'
RDD.M4.COLOR = color.COLOR_WHITE

RDD.M5 = ProcessTree()
RDD.M5.LAYER = Layer(name='M5', number=50)
RDD.M5.MIN_SIZE = 0.7
RDD.M5.MAX_WIDTH = 20.0
# RDD.M5.COLOR = '#FFC0CB'
RDD.M5.COLOR = color.COLOR_SALMON

RDD.M6 = ProcessTree()
RDD.M6.LAYER = Layer(name='M6', number=60)
RDD.M6.MIN_SIZE = 0.5
RDD.M6.MAX_WIDTH = 20.0
# RDD.M6.COLOR = '#E9F26F'
RDD.M6.COLOR = color.COLOR_TURQUOISE

RDD.M7 = ProcessTree()
RDD.M7.LAYER = Layer(name='M7', number=70)
RDD.M7.MIN_SIZE = 0.5
RDD.M7.MAX_WIDTH = 20.0
# RDD.M7.COLOR = '#C497E2'
RDD.M7.COLOR = color.COLOR_CORAL

RDD.M8 = ProcessTree()
RDD.M8.LAYER = Layer(name='M8', number=80)
RDD.M8.MIN_SIZE = 10.0
# RDD.M8.COLOR = '#E4B1E2'
RDD.M8.COLOR = color.COLOR_CORAL

RDD.R5 = ProcessTree()
RDD.R5.LAYER = Layer(name='R5', number=52)
RDD.R5.MIN_SIZE = 0.5
# FIXME: Validation is processlayer.py
RDD.R5.MAX_WIDTH = 5.0
# RDD.R5.COLOR = '#D2B48C'
RDD.R5.COLOR = color.COLOR_LIGHT_GREEN

# --------------------------------- Vias ----------------------------------------

RDD.C0 = ProcessTree()
RDD.C0.LAYER = Layer(name='C0', number=4)
RDD.C0.MIN_SIZE = 0.7
RDD.C0.MAX_SIZE = 1.0
RDD.C0.M5_METAL = 1.0

RDD.I0 = ProcessTree()
RDD.I0.LAYER = Layer(name='I0', number=2)
RDD.I0.MIN_SIZE = 0.6
RDD.I0.MAX_SIZE = 1.2
RDD.I0.M5_METAL = 1.0
RDD.I0.COLOR = color.COLOR_LIGHT_GRAY

RDD.I1 = ProcessTree()
RDD.I1.LAYER = Layer(name='I1', number=11)
RDD.I1.MIN_SIZE = 0.6
RDD.I1.MAX_SIZE = 1.2
RDD.I1.M5_METAL = 1.0
RDD.I1.COLOR = color.COLOR_LIGHT_GRAY

RDD.I2 = ProcessTree()
RDD.I2.WIDTH = 0.5
RDD.I2.LAYER = Layer(name='I2', number=21)
RDD.I2.MIN_SIZE = 0.6
RDD.I2.MAX_SIZE = 1.2
RDD.I2.M5_METAL = 1.0
RDD.I2.COLOR = color.COLOR_LIGHT_GRAY

RDD.I3 = ProcessTree()
RDD.I3.LAYER = Layer(name='I3', number=31)
RDD.I3.MIN_SIZE = 0.6
RDD.I3.MAX_SIZE = 1.2
RDD.I3.M5_METAL = 1.0
RDD.I3.COLOR = color.COLOR_LIGHT_GRAY

RDD.I4 = ProcessTree()
RDD.I4.LAYER = Layer(name='I4', number=41)
RDD.I4.MIN_SIZE = 0.8
RDD.I4.MAX_SIZE = 1.2
RDD.I4.M5_METAL = 1.0
RDD.I4.COLOR = color.COLOR_INDIAN_RED

RDD.I5 = ProcessTree()
RDD.I5.LAYER = Layer(name='I5', number=54)
RDD.I5.MIN_SIZE = 0.7
RDD.I5.MAX_SIZE = 1.2
RDD.I5.M5_METAL = 1.0
RDD.I5.COLOR = color.COLOR_LIGHT_GRAY

RDD.J5 = ProcessTree()
RDD.J5.LAYER = Layer(name='J5', number=51)
RDD.J5.MIN_SIZE = 0.7
RDD.J5.MAX_SIZE = 3.0
RDD.J5.M5_METAL = 1.0
RDD.J5.COLOR = color.COLOR_LIGHT_GRAY

RDD.C5J = ProcessTree()
RDD.C5J.LAYER = Layer(name='C5J', number=55)
RDD.C5J.MIN_SIZE = 0.5
RDD.C5J.M5_METAL = 1.0
RDD.C5J.COLOR = color.COLOR_LIGHT_GRAY

RDD.C5R = ProcessTree()
RDD.C5R.LAYER = Layer(name='C5R', number=53)
# RDD.C5R.LAYER = Layer(name='C5R', number=56)
RDD.C5R.MIN_SIZE = 0.7
RDD.C5R.M5_METAL = 1.0
RDD.C5R.COLOR = color.COLOR_LIGHT_GRAY

RDD.I6 = ProcessTree()
RDD.I6.LAYER = Layer(name='I6', number=61)
RDD.I6.MIN_SIZE = 0.7
RDD.I6.M5_METAL = 1.0
RDD.I6.COLOR = color.COLOR_STEEL_BLUE

RDD.I7 = ProcessTree()
RDD.I7.LAYER = Layer(name='I7', number=71)
RDD.I7.MIN_SIZE = 5.0
RDD.I7.M5_METAL = 1.0
RDD.I7.COLOR = color.COLOR_DARK_MAGENTA

# ------------------------------- Physical Layers -------------------------------

RDD.PLAYER = PhysicalTree()
RDD.PLAYER.R5 = PhysicalLayer(layer=RDD.R5.LAYER, purpose=RDD.PURPOSE.METAL, data=RDD.R5)
RDD.PLAYER.M0 = PhysicalLayer(layer=RDD.M0.LAYER, purpose=RDD.PURPOSE.METAL, data=RDD.M0)
RDD.PLAYER.M1 = PhysicalLayer(layer=RDD.M1.LAYER, purpose=RDD.PURPOSE.METAL, data=RDD.M1)
RDD.PLAYER.M2 = PhysicalLayer(layer=RDD.M2.LAYER, purpose=RDD.PURPOSE.METAL, data=RDD.M2)
RDD.PLAYER.M3 = PhysicalLayer(layer=RDD.M3.LAYER, purpose=RDD.PURPOSE.METAL, data=RDD.M3)
RDD.PLAYER.M4 = PhysicalLayer(layer=RDD.M4.LAYER, purpose=RDD.PURPOSE.GROUND, data=RDD.M4)
RDD.PLAYER.M5 = PhysicalLayer(layer=RDD.M5.LAYER, purpose=RDD.PURPOSE.METAL, data=RDD.M5)
RDD.PLAYER.M6 = PhysicalLayer(layer=RDD.M6.LAYER, purpose=RDD.PURPOSE.METAL, data=RDD.M6)
RDD.PLAYER.M7 = PhysicalLayer(layer=RDD.M7.LAYER, purpose=RDD.PURPOSE.SKY, data=RDD.M7)
RDD.PLAYER.M8 = PhysicalLayer(layer=RDD.M8.LAYER, purpose=RDD.PURPOSE.SKY, data=RDD.M8)

# ------------------------------ Physical Vias ----------------------------------

RDD.PLAYER.C0 = PhysicalLayer(layer=RDD.C0.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.C0)
RDD.PLAYER.I0 = PhysicalLayer(layer=RDD.I0.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I0)
RDD.PLAYER.I1 = PhysicalLayer(layer=RDD.I1.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I1)
RDD.PLAYER.I2 = PhysicalLayer(layer=RDD.I2.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I2)
RDD.PLAYER.I3 = PhysicalLayer(layer=RDD.I3.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I3)
RDD.PLAYER.I4 = PhysicalLayer(layer=RDD.I4.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I4)
RDD.PLAYER.I5 = PhysicalLayer(layer=RDD.I5.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I5)
RDD.PLAYER.I6 = PhysicalLayer(layer=RDD.I6.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I6)
RDD.PLAYER.I7 = PhysicalLayer(layer=RDD.I7.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.I7)
RDD.PLAYER.C5J = PhysicalLayer(layer=RDD.C5J.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.C5J)
RDD.PLAYER.C5R = PhysicalLayer(layer=RDD.C5R.LAYER, purpose=RDD.PURPOSE.PRIM.VIA, data=RDD.C5R)
RDD.PLAYER.J5 = PhysicalLayer(layer=RDD.J5.LAYER, purpose=RDD.PURPOSE.PRIM.JUNCTION, data=RDD.J5)

# --------------------------------- TCells --------------------------------------

RDD.VIAS = ProcessTree()

class TCellI4(DynamicDataTree):
    def initialize(self):
        from spira.lpe.contact import ViaTemplate
        from demo.pdks.components.mitll.via import ViaC5R
        self.DEFAULT = ViaC5R
        self.PCELL = ViaTemplate(
            name = 'I4',
            via_layer = RDD.I4.LAYER,
            layer1 = RDD.M4.LAYER,
            layer2 = RDD.M5.LAYER
        )

RDD.VIAS.I4 = TCellI4()

class TCellI5(DynamicDataTree):
    def initialize(self):
        from spira.lpe.contact import ViaTemplate
        from demo.pdks.components.mitll.via import ViaI5
        self.DEFAULT = ViaI5
        self.PCELL = ViaTemplate(
            name = 'I5',
            via_layer = RDD.I5.LAYER,
            layer1 = RDD.M5.LAYER,
            layer2 = RDD.M6.LAYER
        )

RDD.VIAS.I5 = TCellI5()

class TCellI6(DynamicDataTree):
    def initialize(self):
        from spira.lpe.contact import ViaTemplate
        from demo.pdks.components.mitll.via import ViaI6
        self.DEFAULT = ViaI6
        self.PCELL = ViaTemplate(
            name = 'I6',
            via_layer = RDD.I6.LAYER,
            layer1 = RDD.M6.LAYER,
            layer2 = RDD.M7.LAYER
        )

RDD.VIAS.I6 = TCellI6()

class TCellC5R(DynamicDataTree):
    def initialize(self):
        from spira.lpe.contact import ViaTemplate
        from demo.pdks.components.mitll.via import ViaC5R
        self.DEFAULT = ViaC5R
        self.PCELL = ViaTemplate(
            name = 'C5R',
            via_layer = RDD.C5R.LAYER,
            layer1 = RDD.R5.LAYER,
            layer2 = RDD.M6.LAYER
        )

RDD.VIAS.C5R = TCellC5R()

class TCellJ5(DynamicDataTree):
    def initialize(self):
        from spira.lpe.contact import ViaTemplate
        from demo.pdks.components.mitll.via import ViaC5R
        self.DEFAULT = ViaC5R
        self.PCELL = ViaTemplate(
            name = 'J5',
            via_layer = RDD.J5.LAYER,
            layer1 = RDD.M5.LAYER,
            layer2 = RDD.M6.LAYER
        )

RDD.VIAS.J5 = TCellJ5()

# --------------------------------- Device TCells ---------------------------------

RDD.DEVICES = ProcessTree()

class TCellJunction(DynamicDataTree):
    def initialize(self):
        from demo.pdks.components.mitll.junction import Junction
        self.PCELL = Junction

RDD.DEVICES.JJ = TCellJunction()

class TCellGJunction(DynamicDataTree):
    def initialize(self):
        from demo.pdks.components.mitll.junction import GJunction
        self.PCELL = GJunction

RDD.DEVICES.G_JJ = TCellGJunction()

class TCellSJunction(DynamicDataTree):
    def initialize(self):
        from demo.pdks.components.mitll.junction import SJunction
        self.PCELL = SJunction

RDD.DEVICES.S_JJ = TCellSJunction()

class TCellSGJunction(DynamicDataTree):
    def initialize(self):
        from demo.pdks.components.mitll.junction import SGJunction
        self.PCELL = SGJunction

RDD.DEVICES.SG_JJ = TCellSGJunction()

# --------------------------------- Finished -------------------------------------

class TechAdminTree(DynamicDataTree):
    """ A technology tree with a name generator. """
    def initialize(self):
        from spira.gdsii.generators import NameGenerator
        self.NAME_GENERATOR = NameGenerator(
            prefix_attribute='__name_prefix__',
            counter_zero=0,
            process_name='MiTLL_CELL'
        )
        
RDD.ADMIN = TechAdminTree()

