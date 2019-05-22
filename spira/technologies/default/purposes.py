# from spira.yevon.rdd.layer import PurposeLayer
from spira.yevon.rdd.layer import PurposeLayer
from spira.yevon.rdd.technology import ProcessTree, DynamicDataTree
from spira.yevon.rdd import RULE_DECK_DATABASE as RDD

# ---------------------------------- Purpose Layers ----------------------------------

RDD.PURPOSE = ProcessTree()
RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', datatype=10, symbol='METAL')
RDD.PURPOSE.HOLE = PurposeLayer(name='Polygon holes', datatype=11, symbol='HOLE')
RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', datatype=12, symbol='GND')
RDD.PURPOSE.SKY = PurposeLayer(name='Sky plane polygons', datatype=13, symbol='SKY')
RDD.PURPOSE.DUMMY = PurposeLayer(name='Sky plane polygons', datatype=14, symbol='DUM')
RDD.PURPOSE.KINETIC = PurposeLayer(name='Sky plane polygons', datatype=15, symbol='KIN')
RDD.PURPOSE.TERM = PurposeLayer(name='Terminal ports specified by the designer', datatype=16, symbol='TERM')
RDD.PURPOSE.PROTECTION = PurposeLayer(name='Protection layer for via structures', datatype=17, symbol='PRO')
RDD.PURPOSE.EDGE = PurposeLayer(name='Edge', datatype=18, symbol='PRO', doc='Layer that represents a polygon edge.')
RDD.PURPOSE.ARROW = PurposeLayer(name='Arrow', datatype=19, symbol='PRO', doc='Layer that represents the direction of a polygon edge terminal.')
RDD.PURPOSE.BOUNDARY_BOX = PurposeLayer(name='Bounding Box', datatype=20, symbol='BBOX', doc='Layer that represents the direction of a polygon edge terminal.')

# ---------------------------------- Primitive Layers --------------------------------

RDD.PURPOSE.PRIM = ProcessTree()
RDD.PURPOSE.PRIM.VIA = PurposeLayer(name='Via layer', datatype=20, symbol='VIA')
RDD.PURPOSE.PRIM.JUNCTION = PurposeLayer(name='Junction layer', datatype=21, symbol='JJ')
RDD.PURPOSE.PRIM.NTRON = PurposeLayer(name='nTron layer', datatype=22, symbol='NTRON')

# ---------------------------------- Error Layers ------------------------------------

RDD.PURPOSE.ERROR = ProcessTree()
RDD.PURPOSE.ERROR.SPACING = PurposeLayer(name='nTron layer', datatype=100, symbol='SP')
RDD.PURPOSE.ERROR.MIN_WIDTH = PurposeLayer(name='nTron layer', datatype=101, symbol='MAXW')
RDD.PURPOSE.ERROR.MAX_WIDTH = PurposeLayer(name='nTron layer', datatype=102, symbol='MINW')
RDD.PURPOSE.ERROR.ENCLOSURE = PurposeLayer(name='nTron layer', datatype=103, symbol='ENC')
RDD.PURPOSE.ERROR.OVERLAP = PurposeLayer(name='nTron layer', datatype=104, symbol='OVR')
RDD.PURPOSE.ERROR.DENSITY = PurposeLayer(name='nTron layer', datatype=105, symbol='OVR')


class Default(DynamicDataTree):
    def initialize(self):
        from spira.yevon.rdd.layer import PhysicalLayer

        # RC = ProcessTree()
        # # RC.LAYER = Layer(name='RC', number=9)
        # RC.WIDTH = 0.5
        # RC.M5_METAL = 1.0
        # RC.COLOR = '#B6EBE6'

        # self.PDEFAULT = PhysicalTree()
        self.PDEFAULT = PhysicalLayer(purpose=RDD.PURPOSE.GROUND)

RDD.DEF = Default()



