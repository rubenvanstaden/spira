# import spira.all as spira
import spira.all as spira
# from spira.all import *
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class TranslatePolygon(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        ply.transform(transformation=spira.Translation(Coord(10*1e6, 0)))
        return ply

    def create_t2(self):
        # tf = spira.GenericTransform(translation=Coord(0, 0))
        tf = spira.GenericTransform(translation=Coord(-20*1e6, 0))
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10), transformation=tf)
        return ply

    def create_t3(self):
        tf = spira.Translation((10*1e6, 0))
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10), transformation=tf)
        return ply

    def create_elementals(self, elems):

        elems += self.ref_point
        elems += self.t1
        # elems += self.t2
        # elems += self.t3

        return elems


class RotatePolygon(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        ply.transform(transformation=spira.Rotation(rotation=30))
        # ply._rotate(30)
        return ply

    def create_t2(self):
        # tf = spira.GenericTransform(translation=Coord(0, 0))
        tf = spira.GenericTransform(rotation=45)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11), transformation=tf)
        return ply

    def create_t3(self):
        tf = spira.Rotation(60)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12), transformation=tf)
        return ply

    def create_elementals(self, elems):

        elems += self.ref_point
        elems += self.t1
        # elems += self.t2
        # elems += self.t3

        return elems


class ReflectPolygon(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        ply._reflect(True)
        return ply

    def create_t2(self):
        # tf = spira.GenericTransform(translation=Coord(0, 0))
        tf = spira.GenericTransform(reflection=True)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11), transformation=tf)
        return ply

    def create_t3(self):
        tf = spira.Reflection(True)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12), transformation=tf)
        return ply

    def create_elementals(self, elems):

        # elems += self.t1
        # elems += self.t2
        elems += self.t3
        elems += self.ref_point

        return elems


class TransformPolygon(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        tf = spira.Rotation(30) + spira.Translation(Coord(10*1e6, 0))
        ply.transform(transformation=tf)
        # ply._translate((10*1e6, 0))
        # ply._rotate(30)
        # ply._reflect(True)
        return ply

    def create_t2(self):
        tf = spira.GenericTransform(translation=(30*1e6, 0), rotation=30)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11), transformation=tf)
        return ply

    def create_t3(self):
        tf = spira.Translation(translation=Coord(20*1e6, 0)) + spira.Rotation(-45)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12), transformation=tf)
        return ply

    def create_elementals(self, elems):

        elems += self.ref_point
        elems += self.t1
        # elems += self.t2
        # elems += self.t3

        return elems


class StretchPolygon(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        c = shape.center_of_mass
        # print(c)
        # S = spira.Stretch(stretch_factor=(2,1), stretch_center=c)
        S = spira.Stretch(stretch_factor=(2,1))
        ply = S(ply)
        # print(S)
        return ply

    def create_t2(self):
        tf = spira.GenericTransform(translation=(30*1e6, 0), rotation=30)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11), transformation=tf)
        return ply

    def create_t3(self):
        tf = spira.Translation(translation=Coord(20*1e6, 0)) + spira.Rotation(-45)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12), transformation=tf)
        return ply

    def create_elementals(self, elems):

        elems += self.ref_point
        elems += self.t1
        # elems += self.t2
        # elems += self.t3

        return elems


# -------------------------------------------------------------------------------------------------------------------


cell = spira.Cell(name='Transformations')

# t1 = TranslatePolygon()
# t1.output()

# t2 = RotatePolygon()
# t2.output()

# t3 = ReflectPolygon()
# t3.output()

# t4 = TransformPolygon()
# t4.output()

t5 = StretchPolygon()
t5.output()

# cell += spira.SRef(t1, midpoint=(0, 0))
# cell += spira.SRef(t2, midpoint=(50*1e6, 0))
# cell += spira.SRef(t3, midpoint=(0*1e6, -100*1e6))
# cell += spira.SRef(t4, midpoint=(50*1e6, -100*1e6))

# cell.output()


