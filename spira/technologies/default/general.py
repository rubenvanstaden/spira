from spira.yevon.process.all import *
from spira.yevon.process import RULE_DECK_DATABASE as RDD

# ---------------------------------- GDSII ---------------------------------------

RDD.GDSII = ParameterDatabase()
RDD.GDSII.TEXT = 64
RDD.GDSII.UNIT = 1e-6
# RDD.GDSII.GRID = 1e-6
RDD.GDSII.GRID = 1e-12
RDD.GDSII.PRECISION = 1e-9

# ---------------------------------- Engines ---------------------------------------

RDD.ENGINE = ParameterDatabase()
RDD.ENGINE.SPICE = 'JOSIM_ENGINE'
RDD.ENGINE.GEOMETRY = 'GMSH_ENGINE'
RDD.ENGINE.IMPEDANCE = 'INDUCTEX_ENGINE'

# ---------------------------------- Process ---------------------------------------

RDD.PROCESS = ProcessLayerDatabase()

RDD.PROCESS.VIRTUAL = ProcessLayer(name='Virtual Layer', symbol='VIR')
RDD.PROCESS.LABEL = ProcessLayer(name='Contact 3', symbol='LBL')

RDD.PROCESS.GND = ProcessLayer(name='Ground Plane', symbol='GND')
RDD.PROCESS.SKY = ProcessLayer(name='Sky Plane', symbol='SKY')
RDD.PROCESS.M1 = ProcessLayer(name='Metal 1', symbol='M1')
RDD.PROCESS.M2 = ProcessLayer(name='Metal 2', symbol='M2')
RDD.PROCESS.M3 = ProcessLayer(name='Metal 3', symbol='M3')
RDD.PROCESS.M4 = ProcessLayer(name='Metal 4', symbol='M4')
RDD.PROCESS.M5 = ProcessLayer(name='Metal 5', symbol='M5')
RDD.PROCESS.M6 = ProcessLayer(name='Metal 6', symbol='M6')
RDD.PROCESS.M7 = ProcessLayer(name='Metal 7', symbol='M7')
RDD.PROCESS.R1 = ProcessLayer(name='Resistor Metal 1', symbol='R1')
RDD.PROCESS.J1 = ProcessLayer(name='Junction 1', symbol='J1')
RDD.PROCESS.C1 = ProcessLayer(name='Contact 1', symbol='C1')
RDD.PROCESS.C2 = ProcessLayer(name='Contact 2', symbol='C2')
RDD.PROCESS.C3 = ProcessLayer(name='Contact 3', symbol='C3')

# ---------------------------------- Layer Purposes ----------------------------------

RDD.PURPOSE = PurposeLayerDatabase()

RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', symbol='GND')
RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', symbol='METAL')
RDD.PURPOSE.ROUTE = PurposeLayer(name='Metal routes', symbol='ROUTE')
RDD.PURPOSE.SKY = PurposeLayer(name='Sky plane polygons', symbol='SKY')
RDD.PURPOSE.PROTECTION = PurposeLayer(name='Protection layer for via structures', symbol='PRO')
RDD.PURPOSE.VIA = PurposeLayer(name='Via layer', symbol='VIA')
RDD.PURPOSE.JUNCTION = PurposeLayer(name='Junction layer', symbol='JJ')
RDD.PURPOSE.NTRON = PurposeLayer(name='nTron layer', symbol='NTRON')
RDD.PURPOSE.HOLE = PurposeLayer(name='Polygon holes', symbol='HOLE')
RDD.PURPOSE.DUMMY = PurposeLayer(name='Sky plane polygons', symbol='DUM')
RDD.PURPOSE.BOUNDARY_BOX = PurposeLayer(name='Bounding Box', symbol='BBOX', doc='')
RDD.PURPOSE.INTERSECTED = PurposeLayer(name='Bounding Box', symbol='AND', doc='')
RDD.PURPOSE.UNION = PurposeLayer(name='Bounding Box', symbol='OR', doc='')
RDD.PURPOSE.DIFFERENCE = PurposeLayer(name='Bounding Box', symbol='NOR', doc='')

# ---------------------------------- Text Purposes ------------------------------------

RDD.PURPOSE.TEXT = PurposeLayerDatabase()
RDD.PURPOSE.TEXT.PIN = PurposeLayer(name='PinText', symbol='PT')
RDD.PURPOSE.TEXT.EDGE = PurposeLayer(name='EdgeText', symbol='ET')
RDD.PURPOSE.TEXT.CONTACT = PurposeLayer(name='ContactText', symbol='CT')
RDD.PURPOSE.TEXT.ROUTE = PurposeLayer(name='RouteText', symbol='IT')
RDD.PURPOSE.TEXT.DUMMY = PurposeLayer(name='DummyText', symbol='DT')

# ---------------------------------- Port Purposes ------------------------------------

RDD.PURPOSE.PORT = PurposeLayerDatabase()
RDD.PURPOSE.PORT.PIN = PurposeLayer(name='PinPort', symbol='P')
RDD.PURPOSE.PORT.TERMINAL = PurposeLayer(name='PinPort', symbol='T')
RDD.PURPOSE.PORT.EDGE = PurposeLayer(name='EdgePort', symbol='E')
RDD.PURPOSE.PORT.CONTACT = PurposeLayer(name='ContactPort', symbol='C')
RDD.PURPOSE.PORT.ROUTE = PurposeLayer(name='RoutePort', symbol='I')
RDD.PURPOSE.PORT.BRANCH = PurposeLayer(name='BranchPort', symbol='B')
RDD.PURPOSE.PORT.DUMMY = PurposeLayer(name='DummyPort', symbol='D')
RDD.PURPOSE.PORT.INSIDE_EDGE_ENABLED = PurposeLayer(name='Enabled edge', symbol='EDGE_IE', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED = PurposeLayer(name='Disabled edge', symbol='EDGE_ID', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED = PurposeLayer(name='Enabled edge', symbol='EDGE_OE', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED = PurposeLayer(name='Disabled edge', symbol='EDGE_OD', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.DIRECTION = PurposeLayer(name='Arrow', symbol='DIR', doc='Layer that represents the direction of a edge terminal.')
# RDD.PURPOSE.PORT.TEXT_ENABLED = PurposeLayer(name='Enabled text', symbol='TEXT_E', doc='Layer that represents a polygon edge.')
# RDD.PURPOSE.PORT.TEXT_DISABLED = PurposeLayer(name='Disabled text', symbol='TEXT_D', doc='Layer that represents a polygon edge.')
# RDD.PURPOSE.PORT.INSIDE = PurposeLayer(name='Inside', symbol='IE', doc='The inside edge of the shape.')
# RDD.PURPOSE.PORT.OUTSIDE = PurposeLayer(name='Outside', symbol='OE', doc='The outside edge of the shape.')

# ---------------------------------- Error Purposes ------------------------------------

RDD.PURPOSE.ERROR = ProcessLayerDatabase()
RDD.PURPOSE.ERROR.SPACING = PurposeLayer(name='nTron layer', symbol='SP')
RDD.PURPOSE.ERROR.MIN_WIDTH = PurposeLayer(name='nTron layer', symbol='MAXW')
RDD.PURPOSE.ERROR.MAX_WIDTH = PurposeLayer(name='nTron layer', symbol='MINW')
RDD.PURPOSE.ERROR.ENCLOSURE = PurposeLayer(name='nTron layer', symbol='ENC')
RDD.PURPOSE.ERROR.OVERLAP = PurposeLayer(name='nTron layer', symbol='OVR')
RDD.PURPOSE.ERROR.DENSITY = PurposeLayer(name='nTron layer', symbol='OVR')

# ------------------------------- DEFAULT ----------------------------------

RDD.PLAYER = Database()

RDD.PORT = ParameterDatabase()
RDD.PORT.WIDTH = 0.5

# --------------------------------- Name Generator -------------------------------------

class AdminDatabase(LazyDatabase):
    """ A technology tree with a name generator. """

    def initialize(self):
        from spira.yevon.gdsii.generators import NameGenerator
        self.NAME_GENERATOR = NameGenerator(
            prefix_attribute='__name_prefix__',
            counter=0,
            process_name=''
        )

RDD.ADMIN = AdminDatabase()

# ---------------------------- Parameterized Cell Data --------------------------------

RDD.FILTERS = ParameterDatabase()

class PCellFilterDatabase(LazyDatabase):
    """ Define the filters that will be used when creating a spira.PCell object. """

    def initialize(self):
        from spira.yevon import filters

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.ProcessBooleanFilter(name='boolean', metal_purpose=RDD.PURPOSE.DEVICE_METAL)
        f += filters.SimplifyFilter(name='simplify')
        f += filters.ContactAttachFilter(name='contact_attach')

        f['boolean'] = True
        f['simplify'] = True
        f['contact_attach'] = True

        self.DEVICE = f

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.ProcessBooleanFilter(name='boolean', metal_purpose=RDD.PURPOSE.CIRCUIT_METAL)
        f += filters.SimplifyFilter(name='simplify')

        f['boolean'] = True
        f['simplify'] = True

        self.CIRCUIT = f

        f = filters.ToggledCompositeFilter(name='mask_filters', filters=[])
        f += filters.ElectricalAttachFilter(name='erc')
        f += filters.PinAttachFilter(name='pin_attach')
        f += filters.DeviceMetalFilter(name='device_metal')

        f['erc'] = True
        f['pin_attach'] = True
        f['device_metal'] = False

        self.MASK = f

RDD.FILTERS.PCELL = PCellFilterDatabase()


class OutputFilterDatabase(LazyDatabase):
    """ Define the filters that will be used when creating a spira.PCell object. """

    def initialize(self):
        from spira.yevon import filters

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.PortCellFilter(name='cell_ports')
        f += filters.PortPolygonEdgeFilter(name='edge_ports')
        f += filters.PortPolygonContactFilter(name='contact_ports')

        f['cell_ports'] = True
        f['edge_ports'] = True
        f['contat_ports'] = True

        self.PORTS = f

RDD.FILTERS.OUTPUT = OutputFilterDatabase()
