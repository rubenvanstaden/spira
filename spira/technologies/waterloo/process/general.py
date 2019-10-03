from spira.yevon.process.all import *
from spira.yevon.process import get_rule_deck

RDD = get_rule_deck()

# FIXME: Move a geometry bridge class.
RDD.LCAR_DEVICE = 1
RDD.LCAR_CIRCUIT = 100

# ---------------------------------- GDSII ---------------------------------------

RDD.GDSII = ParameterDatabase()
RDD.GDSII.TEXT = 64
RDD.GDSII.UNIT = 1e-6
RDD.GDSII.GRID = 1e-12
RDD.GDSII.PRECISION = 1e-9

# ---------------------------------- Engines ---------------------------------------

RDD.ENGINE = ParameterDatabase()
RDD.ENGINE.SPICE = 'JOSIM_ENGINE'
RDD.ENGINE.GEOMETRY = 'GMSH_ENGINE'
RDD.ENGINE.IMPEDANCE = 'INDUCTEX_ENGINE'

# ---------------------------------- Process ---------------------------------------

RDD.PROCESS = ProcessLayerDatabase()

RDD.PROCESS.M0 = ProcessLayer(name='Ground Plane', symbol='M0')
RDD.PROCESS.Al = ProcessLayer(name='Metal layer', symbol='Al')
RDD.PROCESS.B0 = ProcessLayer(name='Bosch TSV', symbol='B0')

# ---------------------------------- Layer Purposes ----------------------------------

RDD.PURPOSE = PurposeLayerDatabase()
RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', symbol='GND')
RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', symbol='METAL')
RDD.PURPOSE.VIA = PurposeLayer(name='Via layer', symbol='VIA')
RDD.PURPOSE.JUNCTION = PurposeLayer(name='Junction layer', symbol='JJ')

# ---------------------------------- Text Purposes ------------------------------------

RDD.PURPOSE.TEXT = PurposeLayerDatabase()
RDD.PURPOSE.TEXT.PIN = PurposeLayer(name='PinText', symbol='PT')
RDD.PURPOSE.TEXT.TERMINAL = PurposeLayer(name='PinText', symbol='TT')
RDD.PURPOSE.TEXT.EDGE = PurposeLayer(name='EdgeText', symbol='ET')
RDD.PURPOSE.TEXT.CONTACT = PurposeLayer(name='ContactText', symbol='CT')
RDD.PURPOSE.TEXT.ROUTE = PurposeLayer(name='RouteText', symbol='IT')
RDD.PURPOSE.TEXT.DUMMY = PurposeLayer(name='DummyText', symbol='DT')

# ---------------------------------- Port Purposes ------------------------------------

RDD.PURPOSE.PORT = PurposeLayerDatabase()
RDD.PURPOSE.PORT.PIN = PurposeLayer(name='PinPort', symbol='P')
RDD.PURPOSE.PORT.TERMINAL = PurposeLayer(name='TermPort', symbol='T')
RDD.PURPOSE.PORT.EDGE = PurposeLayer(name='EdgePort', symbol='E')
RDD.PURPOSE.PORT.CONTACT = PurposeLayer(name='ContactPort', symbol='C')
RDD.PURPOSE.PORT.ROUTE = PurposeLayer(name='RoutePort', symbol='I')
RDD.PURPOSE.PORT.BRANCH = PurposeLayer(name='BranchPort', symbol='B')
RDD.PURPOSE.PORT.DUMMY = PurposeLayer(name='DummyPort', symbol='D')
RDD.PURPOSE.PORT.INSIDE_EDGE_ENABLED = PurposeLayer(
    name='Enabled edge', symbol='EDGE_IE', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED = PurposeLayer(
    name='Disabled edge', symbol='EDGE_ID', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED = PurposeLayer(
    name='Enabled edge', symbol='EDGE_OE', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED = PurposeLayer(
    name='Disabled edge', symbol='EDGE_OD', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.TEXT_ENABLED = PurposeLayer(
    name='Enabled text', symbol='TEXT_E', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.TEXT_DISABLED = PurposeLayer(
    name='Disabled text', symbol='TEXT_D', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.PORT.DIRECTION = PurposeLayer(
    name='Arrow', symbol='DIR', doc='Layer that represents the direction of a polygon edge terminal.')

# -------------------------------- Error Purposes ------------------------------------

RDD.PURPOSE.ERROR = PurposeLayerDatabase()
RDD.PURPOSE.ERROR.SPACING = PurposeLayer(name='nTron layer', symbol='SP')
RDD.PURPOSE.ERROR.MIN_WIDTH = PurposeLayer(name='nTron layer', symbol='MAXW')
RDD.PURPOSE.ERROR.MAX_WIDTH = PurposeLayer(name='nTron layer', symbol='MINW')
RDD.PURPOSE.ERROR.ENCLOSURE = PurposeLayer(name='nTron layer', symbol='ENC')
RDD.PURPOSE.ERROR.OVERLAP = PurposeLayer(name='nTron layer', symbol='OVR')
RDD.PURPOSE.ERROR.DENSITY = PurposeLayer(name='nTron layer', symbol='OVR')

# ------------------------------- DEFAULT ----------------------------------

RDD.PLAYER = PhysicalLayerDatabase()

RDD.PORT = ParameterDatabase()
RDD.PORT.WIDTH = 0.5

# --------------------------------- Name Generator -------------------------------------

class TechAdminTree(LazyDatabase):
    """ A technology tree with a name generator. """
    def initialize(self):
        from spira.yevon.gdsii.generators import NameGenerator
        self.NAME_GENERATOR = NameGenerator(
            prefix_attribute='__name_prefix__',
            counter=0,
            process_name=''
        )

RDD.ADMIN = TechAdminTree()

# ----------------------------------- Filters -----------------------------------------

RDD.FILTERS = ParameterDatabase()

class PCellFilterDatabase(LazyDatabase):
    """ Define the filters that will be used when creating a spira.PCell object. """

    def initialize(self):
        from spira.yevon import filters

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.ProcessBooleanFilter(name='boolean', metal_purpose=RDD.PURPOSE.METAL)
        f += filters.SimplifyFilter(name='simplify')
        f += filters.ContactAttachFilter(name='contact_attach')

        f['boolean'] = False
        f['simplify'] = False
        f['contact_attach'] = False

        self.DEVICE = f

        f = filters.ToggledCompositeFilter(filters=[])
        f += filters.ProcessBooleanFilter(name='boolean', metal_purpose=RDD.PURPOSE.METAL)
        f += filters.SimplifyFilter(name='simplify')

        f['boolean'] = False
        f['simplify'] = False

        self.CIRCUIT = f

        f = filters.ToggledCompositeFilter(name='mask_filters', filters=[])
        f += filters.ElectricalAttachFilter(name='erc')
        f += filters.PinAttachFilter(name='pin_attach')
        f += filters.DeviceMetalFilter(name='device_metal')

        f['erc'] = False
        f['pin_attach'] = False
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
        f['edge_ports'] = False
        f['contat_ports'] = False

        self.PORTS = f

RDD.FILTERS.OUTPUT = OutputFilterDatabase()
