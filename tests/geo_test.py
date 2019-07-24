import pytest
import spira.all as spira
from spira.yevon.geometry import shapes
import gdspy
import spira.yevon.io as io

def create_box():
    boxspira = spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=0))
    return boxspira.shape.hash_string
    

def test_rect():
    gds = io.import_gds(filename = "rect.gds",pcell = False)
    hashval = ((gds.elements.polygons[0]).shape.hash_string)
    assert create_box() == hashval

def create_cross():
    crossspira = spira.Cross(layer=spira.Layer(number=0),box_size= 5, center=(0,0), thickness= 1)
    return crossspira.shape.hash_string

def test_cross():
    gds = io.import_gds(filename = "cross.gds",pcell = False)
    hashval = ((gds.elements.polygons[0]).shape.hash_string)
    assert create_cross() == hashval

def create_wedge():
    wedgespira = spira.Wedge(layer= spira.Layer(number=0), begin_coord=(0,0), end_coord=(10,0), begin_width=3)
    return wedgespira.shape.hash_string

def test_wedge():
    gds = io.import_gds(filename = "wedge.gds",pcell = False)
    hashval = ((gds.elements.polygons[0]).shape.hash_string)
    assert create_wedge() == hashval
# FIX ME
#def create_convex():
#    convexspira = spira.Convex(layer= spira.Layer(number=0), radius=1.0, num_sides=4, center=(0,0))
#    return convexspira.shape.hash_string

#def test_convex():
#    gds = io.import_gds(filename = "convex.gds",pcell = False)
#    hashval = ((gds.elements.polygons[0]).shape.hash_string)
#    assert create_convex() == hashval   
# FIX ME
#def create_para():
#    paraspira = spira.Parabolic(layer = spira.Layer(number=0),begin_coord=(0,0),end_coord=(10,0), begin_width=2)
#    return paraspira.shape.hash_string

#def test_parabolic():
#    gds = io.import_gds(filename = "parabolic.gds",pcell= False)
#    hashval = gds.elements.polygons[0].shape.hash_string
#    assert create_para() == hashval


# FIX ME
#def create_round():
#    roundspira = spira.Circle(layer = spira.Layer(number = 0),center=(0,0),angle_step=12,box_size=(1,1))
#    return roundspira.shape.hash_string

#def test_round():
#    gds = io.import_gds(filename = "circle.gds",pcell= False)
#    hashval = gds.elements.polygons[0].shape.hash_string
#    assert create_round() == hashval

