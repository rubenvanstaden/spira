from spira.rdd.technology import DataTree
from spira.rdd.technology import ProcessTree
from spira.rdd.technology import PhysicalTree
from spira.rdd.technology import DynamicDataTree
from spira.gdsii.layer import Layer
from spira.rdd.layer import PhysicalLayer
from spira.rdd import RULE_DECK_DATABASE as RDD

# -------------------------------- Initialize ------------------------------------

RDD.name = 'SPiRA-default'
RDD.desc = 'Process fabrication data for the AIST process from Japan.'

# ---------------------------------- GDSII ---------------------------------------

RDD.GDSII = DataTree()
RDD.GDSII.TEXT = 64
RDD.GDSII.UNIT = 1e-6
RDD.GDSII.PRECISION = 1e-9

# --------------------------------- Metals --------------------------------------

RDD.LAYER = ProcessTree()

RDD.GP = ProcessTree()
RDD.GP.LAYER = Layer(name='GP', number=1)
RDD.GP.COLOR = '#49CEC1'

RDD.RES = ProcessTree()
RDD.RES.LAYER = Layer(name='RES', number=3)
RDD.RES.WIDTH = 1.5
RDD.RES.COLOR = '#7FDCD3'

RDD.BAS = ProcessTree()
RDD.BAS.LAYER = Layer(name='BAS', number=4)
RDD.BAS.WIDTH = 1.5
RDD.BAS.COLOR = '#91E1D9'

RDD.COU = ProcessTree()
RDD.COU.LAYER = Layer(name='COU', number=8)
RDD.COU.WIDTH = 1.5
RDD.COU.COLOR = '#A4E6E0'

RDD.CTL = ProcessTree()
RDD.CTL.LAYER = Layer(name='CTL', number=12)
RDD.CTL.WIDTH = 1.5
RDD.CTL.COLOR = '#B6EBE6'

RDD.JP = ProcessTree()
RDD.JP.LAYER = Layer(name='JP', number=5)
RDD.JP.WIDTH = 0.5
RDD.JP.M5_METAL = 1.0

# --------------------------------- Vias ----------------------------------------

RDD.RC = ProcessTree()
RDD.RC.LAYER = Layer(name='RC', number=9)
RDD.RC.WIDTH = 0.5
RDD.RC.M5_METAL = 1.0

RDD.GC = ProcessTree()
RDD.GC.LAYER = Layer(name='GC', number=2)
RDD.GC.WIDTH = 0.5
RDD.GC.M5_METAL = 1.0

RDD.JJ = ProcessTree()
RDD.JJ.LAYER = Layer(name='JJ', number=6)
RDD.JJ.WIDTH = 0.5
RDD.JJ.M5_METAL = 1.0

RDD.BC = ProcessTree()
RDD.BC.WIDTH = 0.5
RDD.BC.SPACING = 0.5
RDD.BC.LAYER = Layer(name='BC', number=7)
RDD.BC.WIDTH = 0.5
RDD.BC.M5_METAL = 1.0

RDD.JC = ProcessTree()
RDD.JC.LAYER = Layer(name='JC', number=10)
RDD.JC.WIDTH = 0.5
RDD.JC.M5_METAL = 1.0

RDD.CC = ProcessTree()
RDD.CC.LAYER = Layer(name='CC', number=11)
RDD.CC.WIDTH = 0.5
RDD.CC.M5_METAL = 1.0

# ------------------------------- Physical Metals -------------------------------

RDD.PLAYER = PhysicalTree()
RDD.PLAYER.GP = PhysicalLayer(layer=RDD.GP.LAYER, purpose=RDD.PURPOSE.GROUND)
RDD.PLAYER.RES = PhysicalLayer(layer=RDD.RES.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.BAS = PhysicalLayer(layer=RDD.BAS.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.COU = PhysicalLayer(layer=RDD.COU.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.CTL = PhysicalLayer(layer=RDD.CTL.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.JP = PhysicalLayer(layer=RDD.JP.LAYER, purpose=RDD.PURPOSE.PROTECTION)
RDD.PLAYER.JJ = PhysicalLayer(layer=RDD.JJ.LAYER, purpose=RDD.PURPOSE.PRIM.JUNCTION)

# ------------------------------- Physical Vias ----------------------------------

RDD.PLAYER.RC = PhysicalLayer(layer=RDD.RC.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.GC = PhysicalLayer(layer=RDD.GC.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.BC = PhysicalLayer(layer=RDD.BC.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.JC = PhysicalLayer(layer=RDD.JC.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.CC = PhysicalLayer(layer=RDD.CC.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)

# ------------------------------ Primitive TCells -------------------------------

RDD.VIAS = ProcessTree()

class TCellRC(DynamicDataTree):
    def initialize(self):
        from spira.core.default.templates import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'RC',
            via_layer = RDD.RC.LAYER,
            layer1 = RDD.BAS.LAYER,
            layer2 = RDD.RES.LAYER
        )

RDD.VIAS.RC = TCellRC()

class TCellGC(DynamicDataTree):
    def initialize(self):
        from spira.core.default.templates import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'GC',
            via_layer = RDD.GC.LAYER, 
            layer1 = RDD.GP.LAYER, 
            layer2 = RDD.BAS.LAYER
        )

RDD.VIAS.GC = TCellGC()

class TCellBC(DynamicDataTree):
    def initialize(self):
        from spira.core.default.templates import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'BC',
            via_layer = RDD.BC.LAYER, 
            layer1 = RDD.BAS.LAYER, 
            layer2 = RDD.COU.LAYER
        )

RDD.VIAS.BC = TCellBC()

class TCellJC(DynamicDataTree):
    def initialize(self):
        from spira.core.default.templates import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'JC',
            via_layer = RDD.JC.LAYER, 
            layer1 = RDD.JJ.LAYER, 
            layer2 = RDD.COU.LAYER
        )

RDD.VIAS.JC = TCellJC()

class TCellCC(DynamicDataTree):
    def initialize(self):
        from spira.core.default.templates import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'CC',
            via_layer = RDD.CC.LAYER, 
            layer1 = RDD.COU.LAYER, 
            layer2 = RDD.CTL.LAYER
        )

RDD.VIAS.CC = TCellCC()

# --------------------------------- Device TCells ---------------------------------

RDD.DEVICES = ProcessTree()

class TCellJunction(DynamicDataTree):
    def initialize(self):
        from spira.core.default.templates import JunctionTemplate
        self.PCELL = JunctionTemplate(pcell=False)

RDD.DEVICES.JJ = TCellJunction()

# --------------------------------- Finished -------------------------------------




