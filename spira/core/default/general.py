from spira.rdd.layer import PurposeLayer
from spira.rdd.technology import ProcessTree, DynamicDataTree
from spira.rdd import RULE_DECK_DATABASE as RDD

# ---------------------------------- Purpose Layers ----------------------------------

RDD.PURPOSE = ProcessTree()
RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', datatype=20, symbol='METAL')
RDD.PURPOSE.HOLE = PurposeLayer(name='Polygon holes', datatype=21, symbol='HOLE')
RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', datatype=21, symbol='GND')
RDD.PURPOSE.SKY = PurposeLayer(name='Sky plane polygons', datatype=21, symbol='SKY')
RDD.PURPOSE.DUMMY = PurposeLayer(name='Sky plane polygons', datatype=21, symbol='DUM')
RDD.PURPOSE.KINETIC = PurposeLayer(name='Sky plane polygons', datatype=21, symbol='KIN')
RDD.PURPOSE.TERM = PurposeLayer(name='Terminal ports specified by the designer', datatype=63, symbol='TERM')
RDD.PURPOSE.PROTECTION = PurposeLayer(name='Protection layer for via structures', datatype=21, symbol='PRO')

# ---------------------------------- Primitive Layers --------------------------------

RDD.PURPOSE.PRIM = ProcessTree()
RDD.PURPOSE.PRIM.VIA = PurposeLayer(name='Via layer', datatype=21, symbol='VIA')
RDD.PURPOSE.PRIM.JUNCTION = PurposeLayer(name='Junction layer', datatype=21, symbol='JJ')
RDD.PURPOSE.PRIM.NTRON = PurposeLayer(name='nTron layer', datatype=21, symbol='NTRON')

# ---------------------------------- Error Layers ------------------------------------

RDD.PURPOSE.ERROR = ProcessTree()
RDD.PURPOSE.ERROR.WIDTH = PurposeLayer(name='Minimum or maximum layer width rule broken', datatype=100, symbol='WID')
RDD.PURPOSE.ERROR.SPACING = PurposeLayer(name='Spacing rule broken', datatype=101, symbol='SP')
RDD.PURPOSE.ERROR.ENCLOSURE = PurposeLayer(name='Enclosure rule', datatype=102, symbol='ENC')
RDD.PURPOSE.ERROR.OVERLAP = PurposeLayer(name='Overlap rule', datatype=103, symbol='OVR')
RDD.PURPOSE.ERROR.DENSITY = PurposeLayer(name='Density rule', datatype=104, symbol='OVR')

# ---------------------------------- Physical Layer ----------------------------------

class Default(DynamicDataTree):
    def initialize(self):
        from spira.rdd.layer import PhysicalLayer

        # RC = ProcessTree()
        # # RC.LAYER = Layer(name='RC', number=9)
        # RC.WIDTH = 0.5
        # RC.M5_METAL = 1.0
        # RC.COLOR = '#B6EBE6'

        # self.PDEFAULT = PhysicalTree()
        self.PDEFAULT = PhysicalLayer(purpose=RDD.PURPOSE.GROUND)

RDD.DEF = Default()



