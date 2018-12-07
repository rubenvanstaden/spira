from spira.rdd import get_rule_deck
from spira.rdd.technology import DataTree
from spira.rdd.technology import ProcessTree
from spira.kernel.layer import PurposeLayer
from spira.rdd import RULE_DECK_DATABASE as RDD

# ---------------------------------- Purpose Layers ----------------------------------

RDD.PURPOSE = ProcessTree()
RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', datatype=20, symbol='METAL')
RDD.PURPOSE.HOLE = PurposeLayer(name='Polygon holes', datatype=21, symbol='HOLE')
RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', datatype=21, symbol='GND')
RDD.PURPOSE.SKY = PurposeLayer(name='Sky plane polygons', datatype=21, symbol='SKY')
RDD.PURPOSE.DUMMY = PurposeLayer(name='Sky plane polygons', datatype=21, symbol='DUM')
RDD.PURPOSE.KINETIC = PurposeLayer(name='Sky plane polygons', datatype=21, symbol='KIN')
RDD.PURPOSE.TERM = PurposeLayer(name='Terminal ports specified by the designer', datatype=21, symbol='TERM')
RDD.PURPOSE.PROTECTION = PurposeLayer(name='Protection layer for via structures', datatype=21, symbol='PRO')

# ---------------------------------- Primitive Layers --------------------------------

RDD.PURPOSE.PRIM = ProcessTree()
RDD.PURPOSE.PRIM.VIA = PurposeLayer(name='Via layer', datatype=21, symbol='VIA')
RDD.PURPOSE.PRIM.JUNCTION = PurposeLayer(name='Junction layer', datatype=21, symbol='JJ')
RDD.PURPOSE.PRIM.NTRON = PurposeLayer(name='nTron layer', datatype=21, symbol='NTRON')

# ---------------------------------- Error Layers ------------------------------------

RDD.PURPOSE.ERROR = ProcessTree()
RDD.PURPOSE.ERROR.SPACING = PurposeLayer(name='nTron layer', datatype=21, symbol='SP')
RDD.PURPOSE.ERROR.MIN_WIDTH = PurposeLayer(name='nTron layer', datatype=21, symbol='MAXW')
RDD.PURPOSE.ERROR.MAX_WIDTH = PurposeLayer(name='nTron layer', datatype=21, symbol='MINW')
RDD.PURPOSE.ERROR.ENCLOSURE = PurposeLayer(name='nTron layer', datatype=21, symbol='ENC')
RDD.PURPOSE.ERROR.OVERLAP = PurposeLayer(name='nTron layer', datatype=21, symbol='OVR')
RDD.PURPOSE.ERROR.DENSITY = PurposeLayer(name='nTron layer', datatype=21, symbol='OVR')




