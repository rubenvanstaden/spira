from spira.rdd.technology import DataTree
from spira.rdd.technology import ProcessTree
from spira.rdd.technology import PhysicalTree
from spira.rdd.technology import DynamicDataTree
from spira.gdsii.layer import Layer
from spira.rdd.layer import PhysicalLayer
from spira.rdd import RULE_DECK_DATABASE as RDD

# -------------------------------- Initialize ------------------------------------

RDD.name = 'MiTLL'
RDD.desc = 'Process fabrication data for the MiTLL process from the USA.'

# ---------------------------------- GDSII ---------------------------------------

RDD.GDSII = DataTree()
RDD.GDSII.TEXT = 64
RDD.GDSII.UNITS = 1e-6

# --------------------------------- Metals ---------------------------------------

RDD.LAYER = ProcessTree()

RDD.L0 = ProcessTree()
RDD.L0.LAYER = Layer(name='L0', number=3)
RDD.L0.COLOR = '#B6EBE6'

RDD.M0 = ProcessTree()
RDD.M0.LAYER = Layer(name='M0', number=1)
RDD.M0.COLOR = '#B6EBE6'

RDD.M1 = ProcessTree()
RDD.M1.LAYER = Layer(name='M1', number=10)
RDD.M1.COLOR = '#B6EBE6'

RDD.M2 = ProcessTree()
RDD.M2.LAYER = Layer(name='M2', number=20)
RDD.M2.COLOR = '#B6EBE6'

RDD.M3 = ProcessTree()
RDD.M3.LAYER = Layer(name='M3', number=30)
RDD.M3.COLOR = '#B6EBE6'

RDD.M4 = ProcessTree()
RDD.M4.LAYER = Layer(name='M4', number=40)
RDD.M4.COLOR = '#B6EBE6'

RDD.M5 = ProcessTree()
RDD.M5.LAYER = Layer(name='M5', number=50)
RDD.M5.COLOR = '#7FDCD3'

RDD.M6 = ProcessTree()
RDD.M6.LAYER = Layer(name='M6', number=60)
RDD.M6.COLOR = '#91E1D9'

RDD.M7 = ProcessTree()
RDD.M7.LAYER = Layer(name='M7', number=70)
RDD.M7.COLOR = '#A4E6E0'

RDD.M8 = ProcessTree()
RDD.M8.LAYER = Layer(name='M8', number=80)
RDD.M8.COLOR = '#B6EBE6'

RDD.R5 = ProcessTree()
RDD.R5.LAYER = Layer(name='R5', number=52)
RDD.R5.COLOR = '#B6EBE6'

# --------------------------------- Vias ----------------------------------------

RDD.C0 = ProcessTree()
RDD.C0.LAYER = Layer(name='C0', number=4)
RDD.C0.WIDTH = 0.5
RDD.C0.M5_METAL = 1.0

RDD.I0 = ProcessTree()
RDD.I0.LAYER = Layer(name='I0', number=2)
RDD.I0.WIDTH = 0.5
RDD.I0.M5_METAL = 1.0

RDD.I1 = ProcessTree()
RDD.I1.LAYER = Layer(name='I1', number=11)
RDD.I1.WIDTH = 0.5
RDD.I1.M5_METAL = 1.0

RDD.I2 = ProcessTree()
RDD.I2.WIDTH = 0.5
RDD.I2.LAYER = Layer(name='I2', number=21)
RDD.I2.WIDTH = 0.5
RDD.I2.M5_METAL = 1.0

RDD.I3 = ProcessTree()
RDD.I3.LAYER = Layer(name='I3', number=31)
RDD.I3.WIDTH = 0.5
RDD.I3.M5_METAL = 1.0

RDD.I4 = ProcessTree()
RDD.I4.LAYER = Layer(name='I4', number=41)
RDD.I4.WIDTH = 0.5
RDD.I4.M5_METAL = 1.0

RDD.I5 = ProcessTree()
RDD.I5.LAYER = Layer(name='I5', number=54)
RDD.I5.WIDTH = 0.5
RDD.I5.M5_METAL = 1.0

RDD.I6 = ProcessTree()
RDD.I6.LAYER = Layer(name='I6', number=61)
RDD.I6.WIDTH = 0.5
RDD.I6.M5_METAL = 1.0

RDD.I7 = ProcessTree()
RDD.I7.LAYER = Layer(name='I7', number=71)
RDD.I7.WIDTH = 0.5
RDD.I7.M5_METAL = 1.0

RDD.C5 = ProcessTree()
RDD.C5.LAYER = Layer(name='C5', number=53)
RDD.C5.WIDTH = 0.5
RDD.C5.M5_METAL = 1.0

RDD.J5 = ProcessTree()
RDD.J5.LAYER = Layer(name='J5', number=51)
RDD.J5.WIDTH = 0.5
RDD.J5.M5_METAL = 1.0

# ------------------------------- Physical Layers -------------------------------

RDD.PLAYER = PhysicalTree()
RDD.PLAYER.M0 = PhysicalLayer(layer=RDD.M0.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M1 = PhysicalLayer(layer=RDD.M1.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M2 = PhysicalLayer(layer=RDD.M2.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M3 = PhysicalLayer(layer=RDD.M3.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M4 = PhysicalLayer(layer=RDD.M4.LAYER, purpose=RDD.PURPOSE.GROUND)
RDD.PLAYER.M5 = PhysicalLayer(layer=RDD.M5.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M6 = PhysicalLayer(layer=RDD.M6.LAYER, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M7 = PhysicalLayer(layer=RDD.M7.LAYER, purpose=RDD.PURPOSE.SKY)
RDD.PLAYER.M8 = PhysicalLayer(layer=RDD.M8.LAYER, purpose=RDD.PURPOSE.METAL)

# --------------------------------- Vias ----------------------------------------

RDD.PLAYER.C0 = PhysicalLayer(layer=RDD.C0.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I0 = PhysicalLayer(layer=RDD.I0.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I1 = PhysicalLayer(layer=RDD.I1.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I2 = PhysicalLayer(layer=RDD.I2.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I3 = PhysicalLayer(layer=RDD.I3.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I4 = PhysicalLayer(layer=RDD.I4.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I5 = PhysicalLayer(layer=RDD.I5.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I6 = PhysicalLayer(layer=RDD.I6.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.I7 = PhysicalLayer(layer=RDD.I7.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.C5 = PhysicalLayer(layer=RDD.C5.LAYER, purpose=RDD.PURPOSE.PRIM.VIA)
RDD.PLAYER.J5 = PhysicalLayer(layer=RDD.J5.LAYER, purpose=RDD.PURPOSE.PRIM.JUNCTION)

# --------------------------------- TCells --------------------------------------

RDD.VIAS = ProcessTree()

class TCellI4(DynamicDataTree):
    def initialize(self):
        from ...templates.contact import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'I4',
            via_layer = RDD.I4.LAYER,
            layer1 = RDD.M4.LAYER,
            layer2 = RDD.M5.LAYER
        )

RDD.VIAS.I4 = TCellI4()

class TCellI5(DynamicDataTree):
    def initialize(self):
        from ...templates.contact import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'I5',
            via_layer = RDD.I5.LAYER, 
            layer1 = RDD.M5.LAYER, 
            layer2 = RDD.M6.LAYER
        )

RDD.VIAS.I5 = TCellI5()

class TCellC5(DynamicDataTree):
    def initialize(self):
        from ...templates.contact import ViaTemplate
        self.PCELL = ViaTemplate(
            name = 'C5',
            via_layer = RDD.C5.LAYER, 
            layer1 = RDD.R5.LAYER, 
            layer2 = RDD.M6.LAYER
        )

RDD.VIAS.C5 = TCellC5()

class TCellJ5(DynamicDataTree):
    def initialize(self):
        from ...templates.contact import ViaTemplate
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
        from ...templates.junction import JunctionTemplate
        self.PCELL = JunctionTemplate()

RDD.DEVICES.JJ = TCellJunction()

# --------------------------------- Finished -------------------------------------

