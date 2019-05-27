from spira.yevon.rdd.all import *
from spira.yevon.rdd import RULE_DECK_DATABASE as RDD

# --------------------------------- Metals --------------------------------------

RDD.GND = PropertyTree()

RDD.M1 = PropertyTree()
RDD.M1.MIN_SIZE = 0.35
RDD.M1.MAX_WIDTH = 1.5
RDD.M1.MIN_SURROUND_OF_C1 = 0.3

RDD.M2 = PropertyTree()
RDD.M2.WIDTH = 1.5

RDD.M3 = PropertyTree()
RDD.M3.WIDTH = 1.5

# --------------------------------- Vias ----------------------------------------

RDD.C1 = PropertyTree()
RDD.C1.WIDTH = 0.5
RDD.C1.M5_METAL = 1.0

RDD.C2 = PropertyTree()
RDD.C2.WIDTH = 0.5
RDD.C2.M5_METAL = 1.0

RDD.C3 = PropertyTree()
RDD.C3.WIDTH = 0.5
RDD.C3.M5_METAL = 1.0

# ------------------------------- Physical Metals -------------------------------

RDD.PLAYER.M0 = ProcessTree()
RDD.PLAYER.M1 = ProcessTree()
RDD.PLAYER.M2 = ProcessTree()
RDD.PLAYER.M3 = ProcessTree()

RDD.PLAYER.BBOX = PhysicalLayer(process=RDD.PROCESS.VIRTUAL, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.PORT = PhysicalLayer(process=RDD.PROCESS.VIRTUAL, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M0.GND = PhysicalLayer(process=RDD.PROCESS.GND, purpose=RDD.PURPOSE.GROUND)

RDD.PLAYER.M1.METAL = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M1.HOLE = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M1.BBOX = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M1.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M1.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M1.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M1, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M2.METAL = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M2.HOLE = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M2.BBOX = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M2.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M2.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M2.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M2, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

RDD.PLAYER.M3.METAL = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M3.HOLE = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.HOLE)
RDD.PLAYER.M3.BBOX = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.BOUNDARY_BOX)
RDD.PLAYER.M3.PORT_DIRECTION = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.PORT.DIRECTION)
RDD.PLAYER.M3.EDGE_PORT_ENABLED = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.PORT.EDGE_ENABLED)
RDD.PLAYER.M3.EDGE_PORT_DISABLED = PhysicalLayer(process=RDD.PROCESS.M3, purpose=RDD.PURPOSE.PORT.EDGE_DISABLED)

# ------------------------------- Physical Vias ----------------------------------

RDD.PLAYER.C1 = PhysicalLayer(process=RDD.PROCESS.C1, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.C2 = PhysicalLayer(process=RDD.PROCESS.C2, purpose=RDD.PURPOSE.VIA)
RDD.PLAYER.C3 = PhysicalLayer(process=RDD.PROCESS.C3, purpose=RDD.PURPOSE.VIA)

# ------------------------------ Map GDSII Layers -------------------------------

RDD.GDSII.PROCESS_LAYER_MAP = {
    RDD.PROCESS.VIRTUAL : 199,
    # RDD.PROCESS.LABEL : 198,
    RDD.PROCESS.GND : 0,
    RDD.PROCESS.M1 : 1,
    RDD.PROCESS.M2 : 2,
    RDD.PROCESS.M3 : 3,
    RDD.PROCESS.C1 : 10,
    RDD.PROCESS.C2 : 20,
    RDD.PROCESS.C3 : 30,
    RDD.PROCESS.SKY : 99,
}

RDD.GDSII.PURPOSE_DATATYPE_MAP = {
    RDD.PURPOSE.GROUND : 0,
    RDD.PURPOSE.METAL : 1,
    RDD.PURPOSE.SKY : 3,
    RDD.PURPOSE.HOLE : 4,
    RDD.PURPOSE.BOUNDARY_BOX : 5,
    RDD.PURPOSE.PORT.DIRECTION : 6,
    RDD.PURPOSE.PORT.EDGE_ENABLED : 7,
    RDD.PURPOSE.PORT.EDGE_DISABLED : 8,
    RDD.PURPOSE.VIA : 9,
    RDD.PURPOSE.TEXT : 64,
}

RDD.GDSII.EXPORT_LAYER_MAP = UnconstrainedGdsiiPPLayerOutputMap(
    process_layer_map=RDD.GDSII.PROCESS_LAYER_MAP, 
    purpose_datatype_map=RDD.GDSII.PURPOSE_DATATYPE_MAP
)



