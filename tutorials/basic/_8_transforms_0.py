import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class TranslatePolygon(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

    def create_t1(self):
        T = spira.Translation(Coord(-10, 0))
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))
        ply.transform(T)
        return ply

    def create_t2(self):
        tf = spira.GenericTransform(translation=Coord(-22, 0))
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3), transformation=tf)
        return ply

    def create_t3(self):
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        ply.translate((-34, 0))
        return ply

    def create_elements(self, elems):
        elems += self.ref_point
        elems += self.t1
        elems += self.t2
        elems += self.t3
        return elems


class RotatePolygon(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

    def create_t1(self):
        T = spira.Rotation(rotation=-30)
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))
        ply.transform(T)
        return ply

    def create_t2(self):
        T = spira.GenericTransform(rotation=-60)
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3), transformation=T)
        return ply

    def create_t3(self):
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        ply.rotate(-90)
        return ply

    def create_elements(self, elems):
        elems += self.ref_point
        elems += self.t1
        elems += self.t2
        elems += self.t3
        return elems


class ReflectPolygon(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

    def create_t1(self):
        T = spira.Reflection(True)
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))
        ply.transform(T)
        return ply

    def create_t2(self):
        T = spira.GenericTransform(reflection=True)
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3), transformation=T)
        return ply

    def create_t3(self):
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        ply.reflect(True)
        return ply

    def create_elements(self, elems):
        elems += self.ref_point
        elems += self.t1
        elems += self.t2
        elems += self.t3
        return elems


class TransformPolygon(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

    def create_t1(self):
        T = spira.Rotation(30) + spira.Translation(Coord(10, 0))
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))
        ply.transform(transformation=T)
        return ply

    def create_t2(self):
        T = spira.GenericTransform(translation=(20, 0), rotation=60)
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3), transformation=T)
        return ply

    def create_t3(self):
        ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        ply.translate((30, 0))
        ply.rotate(90)
        # FIXME: Reflection is not working.
        ply.reflect(True)
        return ply

    def create_elements(self, elems):
        elems += self.ref_point
        elems += self.t1
        elems += self.t2
        elems += self.t3
        return elems


# class StretchPolygon(spira.Cell):

#     ref_point = spira.Parameter(fdef_name='create_ref_point')
#     t1 = spira.Parameter(fdef_name='create_t1')
#     t2 = spira.Parameter(fdef_name='create_t2')
#     t3 = spira.Parameter(fdef_name='create_t3')

#     def create_ref_point(self):
#         return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

#     def create_t1(self):
#         ply = spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=10))
#         # c = shape.center_of_mass
#         # print(c)
#         S = spira.Stretch(stretch_factor=(2,1), stretch_center=ply.center)
#         # S = spira.Stretch(stretch_factor=(2,1))
#         ply = S(ply)
#         # print(S)
#         return ply

#     def create_t2(self):
#         tf = spira.GenericTransform(translation=(30, 0), rotation=30)
#         ply = shapes.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=11), transformation=tf)
#         return ply

#     # def create_t3(self):
#     #     tf = spira.Translation(translation=Coord(20, 0)) + spira.Rotation(-45)
#     #     shape = shapes.RectangleShape(p1=(0,0), p2=(10, 50))
#     #     ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=12), transformation=tf)
#     #     return ply

#     def create_elements(self, elems):

#         elems += self.ref_point
#         elems += self.t1
#         # elems += self.t2
#         # elems += self.t3

#         return elems


# -------------------------------------------------------------------------------------------------------------------


cell = spira.Cell(name='Transformations')

t1 = TranslatePolygon()
# t1.gdsii_output(name='Translate')

t2 = RotatePolygon()
# t2.gdsii_output()

t3 = ReflectPolygon()
# t3.gdsii_output()

t4 = TransformPolygon()
t4.gdsii_output(name='Transform')

# t5 = StretchPolygon()
# t5.gdsii_output()

cell += spira.SRef(t1, midpoint=(0, 0))
cell += spira.SRef(t2, midpoint=(100, 0))
cell += spira.SRef(t3, midpoint=(0, -100))
cell += spira.SRef(t4, midpoint=(100, -100))

cell.gdsii_output()


