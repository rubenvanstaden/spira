# import spira.all as spira
import spira.all as spira
# from spira.all import *
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class TranslateReference(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        cell += ply
        S = spira.SRef(cell)
        S._translate((10*1e6, 0))
        return S

    def create_t2(self):
        cell = spira.Cell()
        tf = spira.GenericTransform(translation=Coord(-20*1e6, 0))
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        cell += ply
        S = spira.SRef(cell, transformation=tf)
        return S

    def create_t3(self):
        cell = spira.Cell()
        tf = spira.Translation((10*1e6, 0))
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        cell += ply
        S = spira.SRef(cell, transformation=tf)
        return S

    def create_elementals(self, elems):
        
        # elems += self.t1
        # elems += self.t2
        elems += self.t3
        elems += self.ref_point

        return elems


class RotationReference(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        cell += ply
        S = spira.SRef(cell)
        S._rotate(90)
        return S

    def create_t2(self):
        cell = spira.Cell()
        tf = spira.GenericTransform(rotation=60)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11))
        cell += ply
        S = spira.SRef(cell, transformation=tf)
        return S

    def create_t3(self):
        cell = spira.Cell()
        tf = spira.Rotation(rotation=30)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12))
        cell += ply
        S = spira.SRef(cell, transformation=tf)
        return S

    def create_elementals(self, elems):
        
        elems += self.t1
        elems += self.t2
        elems += self.t3
        elems += self.ref_point

        return elems


class ReflectReference(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        cell += ply
        S = spira.SRef(cell)
        S._reflect(True)
        return S

    def create_t2(self):
        cell = spira.Cell()
        tf = spira.GenericTransform(reflection=True)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11))
        cell += ply
        S = spira.SRef(cell, transformation=tf)
        return S

    def create_t3(self):
        cell = spira.Cell()
        tf = spira.Reflection(True)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12))
        cell += ply
        S = spira.SRef(cell, transformation=tf)
        return S

    def create_elementals(self, elems):
        
        elems += self.t1
        elems += self.t2
        elems += self.t3
        elems += self.ref_point

        return elems


class TransformReference(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')
    t2 = spira.DataField(fdef_name='create_t2')
    t3 = spira.DataField(fdef_name='create_t3')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        cell += ply

        S1 = spira.SRef(cell)
        S1._rotate(rotation=45)
        S1._translate(Coord(15*1e6, 15*1e6))

        S = spira.SRef(cell)
        S._rotate(rotation=45)
        S._translate(Coord(15*1e6, 15*1e6))
        S._reflect(True)
        return [S1, S]

    def create_t2(self):
        cell = spira.Cell()
        tf_1 = spira.GenericTransform(translation=(10*1e6, 10*1e6), rotation=45)
        tf_2 = spira.GenericTransform(translation=Coord(10*1e6, 10*1e6), rotation=45, reflection=True)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11))
        cell += ply
        S1 = spira.SRef(cell, transformation=tf_1)
        S2 = spira.SRef(cell, transformation=tf_2)
        return [S1, S2]

    def create_t3(self):
        cell = spira.Cell()
        tf_1 = spira.Translation(Coord(12.5*1e6, 2.5*1e6)) + spira.Rotation(60)
        tf_2 = spira.Translation(Coord(12.5*1e6, 2.5*1e6)) + spira.Rotation(60) + spira.Reflection(True)
        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12))
        cell += ply
        S1 = spira.SRef(cell, transformation=tf_1)
        S2 = spira.SRef(cell, transformation=tf_2)
        return [S1, S2]
        # return S1

    def create_elementals(self, elems):
        
        elems += self.t1
        # elems += self.t2
        # elems += self.t3
        elems += self.ref_point

        return elems


# -------------------------------------------------------------------------------------------------------------------


cell = spira.Cell(name='Transformations')

t1 = TranslateReference()
t2 = RotationReference()
t3 = ReflectReference()
t4 = TransformReference()

# cell += spira.SRef(t1, midpoint=(0, 0))
# cell += spira.SRef(t2, midpoint=(50*1e6, 0))
# cell += spira.SRef(t3, midpoint=(0*1e6, -100*1e6))
cell += spira.SRef(t4, midpoint=(50*1e6, -100*1e6))

cell.output()


