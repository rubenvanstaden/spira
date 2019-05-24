import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class A(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.RectangleShape(p1=(0,0), p2=(20*1e6, 20*1e6))
        elems += spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))

        return elems


class B(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.BoxShape(width=8*1e6, height=30*1e6)
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=2))
        elems += ply

        return elems


class C(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.BoxShape(width=8*1e6, height=8*1e6)
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=3))
        elems += ply

        return elems


class D(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.BoxShape(width=6*1e6, height=6*1e6)
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=4))
        elems += ply

        return elems


a = A()
b = B()
c = C()
d = D()

# tf = spira.GenericTransform(translation=Coord(-10*1e6, 0), rotation=45)
# tf = spira.GenericTransform(translation=Coord(-10*1e6, 0), rotation=45, reflection=True)
# tf = spira.Rotation(30) + spira.Translation((30*1e6, 0)) + spira.Reflection(reflection=True)
# tf = spira.Rotation(30) + spira.Translation((30*1e6, 0))

print(tf)
print(type(tf))

S = spira.SRef(b, transformation=tf)
# S._rotate(45)
# S._translate((10*1e6, 0))
S = S.transformation.apply_to_object(S)
a += S

print('\n--- Transformation ---')
print(a.transformation)
print(S.transformation)
print(type(S.transformation))
print(S.rotation)
print(S.translation)

a.output()


