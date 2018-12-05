from spira.rdd.technology import DataTree
from spira.rdd.technology import ProcessTree
from spira.rdd import RULE_DECK_DATABASE as RDD

# --------------------------------------------------------------------------------
# MiTLL Process
# --------------------------------------------------------------------------------

print('Initializing Rule Deck Library...')

RDD.name = 'MiTLL'
RDD.desc = 'Process fabrication data for the MITLL process from the USA.'

# ---------------------------------- GDSII ----------------------------------------

RDD.GDSII = DataTree()
RDD.GDSII.UNITS = 1e-6
RDD.GDSII.TERM = 19
RDD.GDSII.TEXT = 18

# ---------------------------------- GDSII ----------------------------------------

RDD.ERRORS = ProcessTree()
RDD.ERRORS.SPACING = 101
RDD.ERRORS.DENSITY = 102
RDD.ERRORS.WIDTH = 103

RDD.GROUND = ProcessTree()
RDD.GROUND.M4 = ProcessTree()
RDD.GROUND.M4.LAYER = 40
RDD.GROUND.M4.COLOR = '#B6EBE6'

RDD.METALS = ProcessTree()
RDD.METALS.DATATYPE = 0

RDD.METALS.L0 = ProcessTree()
RDD.METALS.M0 = ProcessTree()
RDD.METALS.M1 = ProcessTree()
RDD.METALS.M2 = ProcessTree()
RDD.METALS.M3 = ProcessTree()
# RDD.METALS.M4 = ProcessTree()
RDD.METALS.M5 = ProcessTree()
RDD.METALS.M6 = ProcessTree()
RDD.METALS.M7 = ProcessTree()
RDD.METALS.M8 = ProcessTree()
RDD.METALS.R5 = ProcessTree()

RDD.METALS.L0.LAYER = 3
RDD.METALS.L0.COLOR = '#49CEC1'
RDD.METALS.M0.LAYER = 1
RDD.METALS.M0.COLOR = '#7FDCD3'
RDD.METALS.M1.LAYER = 10
RDD.METALS.M1.COLOR = '#91E1D9'
RDD.METALS.M2.LAYER = 20
RDD.METALS.M2.COLOR = '#A4E6E0'
RDD.METALS.M3.LAYER = 30
RDD.METALS.M3.COLOR = '#B6EBE6'

# RDD.METALS.M4.LAYER = 40
# RDD.METALS.M4.GROUND = True
# RDD.METALS.M4.COLOR = '#91E1B2'

RDD.METALS.M5.LAYER = 50
RDD.METALS.M5.COLOR = '#FF7F50'
RDD.METALS.M6.LAYER = 60
RDD.METALS.M6.COLOR = '#40E0D0'
RDD.METALS.M7.LAYER = 70
RDD.METALS.M7.COLOR = '#6DD798'
RDD.METALS.M8.LAYER = 80
RDD.METALS.M8.COLOR = '#9AE9A1'
RDD.METALS.R5.LAYER = 52
RDD.METALS.R5.COLOR = '#98FB98'

RDD.VIAS = ProcessTree()

# --------------------------------------------------------------------------------
# I0 Via
# --------------------------------------------------------------------------------
RDD.VIAS.C0 = ProcessTree()
RDD.VIAS.C0.LAYER = 4
RDD.VIAS.C0.WIDTH = 0.5
RDD.VIAS.C0.M5_METAL = 1.0
RDD.VIAS.C0.M4_METAL = RDD.VIAS.C0.M5_METAL

# --------------------------------------------------------------------------------
# I0 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I0 = ProcessTree()
RDD.VIAS.I0.LAYER = 2
RDD.VIAS.I0.WIDTH = 0.5
RDD.VIAS.I0.M5_METAL = 1.0
RDD.VIAS.I0.M4_METAL = RDD.VIAS.I0.M5_METAL

# --------------------------------------------------------------------------------
# I4 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I1 = ProcessTree()
RDD.VIAS.I1.LAYER = 11
RDD.VIAS.I1.WIDTH = 0.5
RDD.VIAS.I1.M5_METAL = 1.0
RDD.VIAS.I1.M4_METAL = RDD.VIAS.I1.M5_METAL

# --------------------------------------------------------------------------------
# I4 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I2 = ProcessTree()
RDD.VIAS.I2.LAYER = 21
RDD.VIAS.I2.WIDTH = 0.5
RDD.VIAS.I2.M5_METAL = 1.0
RDD.VIAS.I2.M4_METAL = RDD.VIAS.I2.M5_METAL

# --------------------------------------------------------------------------------
# I4 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I3 = ProcessTree()
RDD.VIAS.I3.LAYER = 31
RDD.VIAS.I3.WIDTH = 0.5
RDD.VIAS.I3.M5_METAL = 1.0
RDD.VIAS.I3.M4_METAL = RDD.VIAS.I3.M5_METAL

# --------------------------------------------------------------------------------
# I4 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I4 = ProcessTree()
RDD.VIAS.I4.LAYER = 41
RDD.VIAS.I4.WIDTH = 0.5
RDD.VIAS.I4.M5_METAL = 1.0
RDD.VIAS.I4.M4_METAL = RDD.VIAS.I4.M5_METAL

# --------------------------------------------------------------------------------
# I5 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I5 = ProcessTree()
RDD.VIAS.I5.LAYER = 54
RDD.VIAS.I5.WIDTH = 0.5
RDD.VIAS.I5.M5_METAL = 1.0
RDD.VIAS.I5.M4_METAL = RDD.VIAS.I5.M5_METAL

# --------------------------------------------------------------------------------
# I5 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I6 = ProcessTree()
RDD.VIAS.I6.LAYER = 61
RDD.VIAS.I6.WIDTH = 0.5
RDD.VIAS.I6.M5_METAL = 1.0
RDD.VIAS.I6.M4_METAL = RDD.VIAS.I6.M5_METAL

# --------------------------------------------------------------------------------
# I5 Via
# --------------------------------------------------------------------------------
RDD.VIAS.I7 = ProcessTree()
RDD.VIAS.I7.LAYER = 71
RDD.VIAS.I7.WIDTH = 0.5
RDD.VIAS.I7.M5_METAL = 1.0
RDD.VIAS.I7.M4_METAL = RDD.VIAS.I7.M5_METAL

# --------------------------------------------------------------------------------
# C5 Via
# --------------------------------------------------------------------------------
RDD.VIAS.C5 = ProcessTree()
RDD.VIAS.C5.LAYER = 53
RDD.VIAS.C5.WIDTH = 0.5
RDD.VIAS.C5.R5_METAL = 1.0
RDD.VIAS.C5.M6_METAL = RDD.VIAS.C5.R5_METAL

# --------------------------------------------------------------------------------
# J5 Via
# --------------------------------------------------------------------------------
RDD.VIAS.J5 = ProcessTree()
RDD.VIAS.J5.LAYER = 51
RDD.VIAS.J5.WIDTH = 0.5
RDD.VIAS.J5.M5_METAL = 1.0
RDD.VIAS.J5.M6_METAL = RDD.VIAS.J5.M5_METAL


from spira.templates.templates import *
from spira.lrc.rules import *
from spira.kernel.layer import Layer

# RDD.VIAS.C0.PCELL = ViaC0()
# RDD.VIAS.I0.PCELL = ViaI0()
# RDD.VIAS.I1.PCELL = ViaI1()
# RDD.VIAS.I2.PCELL = ViaI2()
# RDD.VIAS.I3.PCELL = ViaI3()

M4 = Layer(name='M4', number=RDD.GROUND.M4.LAYER, datatype=0)
M5 = Layer(name='M5', number=RDD.METALS.M5.LAYER, datatype=0)
M6 = Layer(name='M6', number=RDD.METALS.M6.LAYER, datatype=0)
M7 = Layer(name='M7', number=RDD.METALS.M7.LAYER, datatype=0)
R5 = Layer(name='R5', number=RDD.METALS.R5.LAYER, datatype=0)

I4 = Layer(name='I4', number=RDD.VIAS.I4.LAYER, datatype=0)
I5 = Layer(name='I5', number=RDD.VIAS.I5.LAYER, datatype=0)
J5 = Layer(name='J5', number=RDD.VIAS.J5.LAYER, datatype=0)
C5 = Layer(name='C5', number=RDD.VIAS.C5.LAYER, datatype=0)
MOAT = Layer(name='MOAT', number=67, datatype=0)

RDD.VIAS.I4.PCELL = ViaTemplate(
    name = 'I4',
    # surround = Surround(layer1=I4, layer2=M5, min=0.3),
    via_layer = I4, layer1 = M4, layer2 = M5
)

RDD.VIAS.I5.PCELL = ViaTemplate(
    name = 'I5',
    # surround = Surround(layer1=I5, layer2=M6, min=0.3),
    via_layer = I5, layer1 = M5, layer2 = M6
)

RDD.VIAS.J5.PCELL = ViaTemplate(
    name = 'J5',
    # surround = Surround(layer1=J5, layer2=M6, min=0.3),
    via_layer = J5, layer1 = M5, layer2 = M6
)

RDD.VIAS.C5.PCELL = ViaTemplate(
    name = 'C5',
    # surround = Surround(layer1=C5, layer2=M6, min=0.35),
    via_layer = C5, layer1 = R5, layer2 = M6
)

RDD.MOAT = MOAT
RDD.M4 = M4
RDD.M5 = M5
RDD.M6 = M6
RDD.R5 = R5
RDD.M7 = M7

RDD.J5 = J5
RDD.I4 = I4
RDD.I5 = I5
RDD.C5 = C5


# RDD.RULES = Rules()


# # RDD.VIAS.I5.PCELL = ViaI5()
# RDD.VIAS.I6.PCELL = ViaI6()
# RDD.VIAS.I7.PCELL = ViaI7()
# # RDD.VIAS.C5.PCELL = ViaC5()
# # RDD.VIAS.J5.PCELL = ViaJ5()
