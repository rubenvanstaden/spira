from spira.rdd.technology import DataTree
from spira.rdd.technology import ProcessTree
from spira.rdd import RULE_DECK_DATABASE as RDD

# -------------------------------- Initialize -------------------------------------

RDD.name = 'AiST'
RDD.desc = 'Process fabrication data for the AIST process from Japan.'

# ---------------------------------- GDSII ----------------------------------------

RDD.GDSII = DataTree()
RDD.GDSII.UNITS = 1e-6
RDD.GDSII.TERM = 63
RDD.GDSII.TEXT = 64
RDD.GDSII.GPLAYER = 1
# RDD.GDSII.TERM = 15
# RDD.GDSII.TEXT = 64

# --------------------------------- Errors ---------------------------------------

RDD.ERRORS = ProcessTree()
RDD.ERRORS.SPACING = 101
RDD.ERRORS.DENSITY = 102
RDD.ERRORS.WIDTH = 103

# --------------------------------- Metals ---------------------------------------

RDD.METALS = ProcessTree()
RDD.METALS.DATATYPE = 0

RDD.METALS.GP = ProcessTree()
RDD.METALS.RES = ProcessTree()
RDD.METALS.BAS = ProcessTree()
RDD.METALS.COU = ProcessTree()
RDD.METALS.CTL = ProcessTree()

RDD.METALS.GP.LAYER = 1
RDD.METALS.GP.COLOR = '#49CEC1'
RDD.METALS.RES.LAYER = 3
RDD.METALS.RES.COLOR = '#7FDCD3'
RDD.METALS.BAS.LAYER = 4
RDD.METALS.BAS.COLOR = '#91E1D9'
RDD.METALS.COU.LAYER = 8
RDD.METALS.COU.COLOR = '#A4E6E0'
RDD.METALS.CTL.LAYER = 12
RDD.METALS.CTL.COLOR = '#B6EBE6'

RDD.PROTECTION = ProcessTree()
RDD.PROTECTION.desc = 'Protection layer around via structures.'

RDD.PROTECTION.JP = ProcessTree()
RDD.PROTECTION.JP.LAYER = 5
RDD.PROTECTION.JP.WIDTH = 0.5
RDD.PROTECTION.JP.M5_METAL = 1.0

# --------------------------------- Vias ----------------------------------------

RDD.VIAS = ProcessTree()

RDD.VIAS.RC = ProcessTree()
RDD.VIAS.RC.LAYER = 9
RDD.VIAS.RC.WIDTH = 0.5
RDD.VIAS.RC.M5_METAL = 1.0

RDD.VIAS.GC = ProcessTree()
RDD.VIAS.GC.LAYER = 2
RDD.VIAS.GC.WIDTH = 0.5
RDD.VIAS.GC.M5_METAL = 1.0

RDD.VIAS.JJ = ProcessTree()
RDD.VIAS.JJ.LAYER = 6
RDD.VIAS.JJ.WIDTH = 0.5
RDD.VIAS.JJ.M5_METAL = 1.0

RDD.VIAS.BC = ProcessTree()
RDD.VIAS.BC.LAYER = 7
RDD.VIAS.BC.WIDTH = 0.5
RDD.VIAS.BC.M5_METAL = 1.0

RDD.VIAS.JC = ProcessTree()
RDD.VIAS.JC.LAYER = 10
RDD.VIAS.JC.WIDTH = 0.5
RDD.VIAS.JC.M5_METAL = 1.0

RDD.VIAS.CC = ProcessTree()
RDD.VIAS.CC.LAYER = 11
RDD.VIAS.CC.WIDTH = 0.5
RDD.VIAS.CC.M5_METAL = 1.0








from spira.templates.templates import *
from spira.lrc.rules import *
from spira.kernel.layer import Layer

GP = Layer(name='M4', number=RDD.METALS.GP.LAYER, datatype=0)
RES = Layer(name='M5', number=RDD.METALS.RES.LAYER, datatype=0)
BAS = Layer(name='M6', number=RDD.METALS.BAS.LAYER, datatype=0)
COU = Layer(name='M7', number=RDD.METALS.COU.LAYER, datatype=0)
CTL = Layer(name='R5', number=RDD.METALS.CTL.LAYER, datatype=0)

RC = Layer(name='I4', number=RDD.VIAS.RC.LAYER, datatype=0)
GC = Layer(name='I5', number=RDD.VIAS.GC.LAYER, datatype=0)
BC = Layer(name='J5', number=RDD.VIAS.BC.LAYER, datatype=0)
JC = Layer(name='C5', number=RDD.VIAS.JC.LAYER, datatype=0)
CC = Layer(name='C5', number=RDD.VIAS.CC.LAYER, datatype=0)
JJ = Layer(name='JJ', number=RDD.VIAS.JC.LAYER, datatype=0)
MOAT = Layer(name='MOAT', number=67, datatype=0)

RDD.VIAS.RC.PCELL = ViaTemplate(
    name = 'RC',
    via_layer = RC, layer1 = BAS, layer2 = RES
)

RDD.VIAS.GC.PCELL = ViaTemplate(
    name = 'GC',
    via_layer = GC, layer1 = GP, layer2 = BAS
)

RDD.VIAS.BC.PCELL = ViaTemplate(
    name = 'BC',
    via_layer = BC, layer1 = BAS, layer2 = COU
)

RDD.VIAS.JC.PCELL = ViaTemplate(
    name = 'JC',
    via_layer = JC, layer1 = JJ, layer2 = COU
)

RDD.VIAS.CC.PCELL = ViaTemplate(
    name = 'CC',
    via_layer = CC, layer1 = COU, layer2 = CTL
)

RDD.MOAT = MOAT
RDD.GP = GP
RDD.RES = RES
RDD.BAS = BAS
RDD.COU = COU
RDD.CTL = CTL

RDD.RC = RC
RDD.GC = GC
RDD.BC = BC
RDD.JC = JC
RDD.CC = CC
RDD.JJ = JJ


