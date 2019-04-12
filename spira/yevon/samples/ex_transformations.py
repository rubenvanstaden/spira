import spira
from spira import shapes


class A(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.RectangleShape(p1=(0,0), p2=(20*1e6, 20*1e6))
        elems += spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))

        return elems


class B(spira.Cell):

    def create_elementals(self, elems):
        
        shape = shapes.BoxShape(width=8*1e6, height=8*1e6)
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

# b += spira.SRef(d)

# a += spira.SRef(b, midpoint=(5*1e6, 10*1e6))
S = spira.SRef(b)
S._translate((10*1e6, 0))
a += S
# a += spira.SRef(c)

print(a.transformation)

a.output()


