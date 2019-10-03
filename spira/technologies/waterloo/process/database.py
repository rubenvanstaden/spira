from spira.yevon.process.all import *
from spira.yevon.process import get_rule_deck

RDD = get_rule_deck()

# --------------------------------- Metals --------------------------------------

RDD.M0 = ParameterDatabase()
RDD.M0.MIN_SIZE = 1000

RDD.Al = ParameterDatabase()
RDD.Al.MIN_SIZE = 500
RDD.Al.B0_MIN_SURROUND = 10

# --------------------------------- Vias ----------------------------------------

RDD.B0 = ParameterDatabase()
RDD.B0.MIN_SIZE = 100
RDD.B0.MAX_SIZE = 300

# ------------------------------- Physical Layers -------------------------------

RDD.PLAYER.M0 = PhysicalLayerDatabase()
RDD.PLAYER.Al = PhysicalLayerDatabase()

RDD.PLAYER.M0.GROUND = PhysicalLayer(name='M0', process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.GROUND)
RDD.PLAYER.M0.METAL = PhysicalLayer(name='M0', process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.M0.PORT_PIN = PhysicalLayer(process=RDD.PROCESS.M0, purpose=RDD.PURPOSE.PORT.PIN)

RDD.PLAYER.Al.GROUND = PhysicalLayer(name='Al', process=RDD.PROCESS.Al, purpose=RDD.PURPOSE.GROUND)
RDD.PLAYER.Al.METAL = PhysicalLayer(name='Al', process=RDD.PROCESS.Al, purpose=RDD.PURPOSE.METAL)
RDD.PLAYER.Al.PORT_PIN = PhysicalLayer(process=RDD.PROCESS.Al, purpose=RDD.PURPOSE.PORT.PIN)

# ------------------------------- Physical Contacts ----------------------------------

RDD.PLAYER.B0 = PhysicalLayerDatabase()

RDD.PLAYER.B0.VIA = PhysicalLayer(name='B0', process=RDD.PROCESS.B0, purpose=RDD.PURPOSE.VIA)

# ------------------------------ Map GDSII Layers -------------------------------

RDD.GDSII.PROCESS_LAYER_MAP = {
    RDD.PROCESS.M0 : 0,
    RDD.PROCESS.Al : 1,
    RDD.PROCESS.B0 : 10,
}

RDD.GDSII.PURPOSE_DATATYPE_MAP = {
    RDD.PURPOSE.GROUND : 0,
    RDD.PURPOSE.METAL : 1,
    RDD.PURPOSE.VIA : 9,
    RDD.PURPOSE.JUNCTION : 10,
    RDD.PURPOSE.PORT.DIRECTION : 6,
    RDD.PURPOSE.PORT.INSIDE_EDGE_ENABLED : 7,
    RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED : 8,
    RDD.PURPOSE.PORT.PIN : 15,
    RDD.PURPOSE.PORT.TERMINAL : 28,
    RDD.PURPOSE.PORT.EDGE : 16,
    RDD.PURPOSE.PORT.CONTACT : 17,
    RDD.PURPOSE.PORT.BRANCH : 18,
    RDD.PURPOSE.PORT.DUMMY : 19,
    RDD.PURPOSE.PORT.ROUTE : 26,
    RDD.PURPOSE.TEXT.PIN : 20,
    RDD.PURPOSE.TEXT.TERMINAL : 27,
    RDD.PURPOSE.TEXT.EDGE : 21,
    RDD.PURPOSE.TEXT.CONTACT : 22,
    RDD.PURPOSE.TEXT.ROUTE : 25,
    RDD.PURPOSE.TEXT.DUMMY : 26,
    RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED : 23,
    RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED : 24,
    RDD.PURPOSE.TEXT : 64,
}

RDD.GDSII.EXPORT_LAYER_MAP = MapPhysicalToGdsii(
    process_layer_map=RDD.GDSII.PROCESS_LAYER_MAP,
    purpose_datatype_map=RDD.GDSII.PURPOSE_DATATYPE_MAP
)

RDD.GDSII.IMPORT_LAYER_MAP = MapGdsiiToPhysical(
    process_layer_map=RDD.GDSII.PROCESS_LAYER_MAP,
    purpose_datatype_map=RDD.GDSII.PURPOSE_DATATYPE_MAP
)

# ------------------------------------- Virtual Modelling ----------------------------------------------

RDD.VMODEL = PhysicalLayerDatabase()

RDD.VMODEL.PROCESS_FLOW = VModelProcessFlow(
    active_processes=[
        RDD.PROCESS.M0,
        RDD.PROCESS.Al,
        RDD.PROCESS.B0,
    ]
)

RDD.VIAS = ParameterDatabase()

# --- ViaI5 ---

RDD.VIAS.B0 = ParameterDatabase()

RDD.VIAS.B0.LAYER_STACK = {
    'BOT_LAYER' : RDD.PLAYER.M0.METAL,
    'TOP_LAYER' : RDD.PLAYER.Al.METAL,
    'VIA_LAYER' : RDD.PLAYER.B0.VIA
}
RDD.PLAYER.B0.CLAYER_CONTACT = RDD.PLAYER.M0.METAL & RDD.PLAYER.Al.METAL & RDD.PLAYER.B0.VIA
RDD.PLAYER.B0.CLAYER_M1 = RDD.PLAYER.M0.METAL ^ RDD.PLAYER.B0.VIA
RDD.PLAYER.B0.CLAYER_M2 = RDD.PLAYER.Al.METAL ^ RDD.PLAYER.B0.VIA

class Bosch_PCELL_Database(LazyDatabase):
    def initialize(self):
        from ..circuits.tsv_bosch_v1 import BoschVia
        self.DEFAULT = BoschVia

RDD.VIAS.B0.PCELLS = Bosch_PCELL_Database()

