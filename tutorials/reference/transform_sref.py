import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class TranslateReference(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        ply = spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))
        T = spira.Translation(Coord(10, 0))
        S = spira.SRef(cell, transformation=T)
        return S

    def create_t2(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3))
        T = spira.GenericTransform(translation=Coord(22, 0))
        S = spira.SRef(cell, transformation=T)
        return S

    def create_t3(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        S = spira.SRef(cell)
        S.translate((34, 0))
        return S

    def create_elements(self, elems):
        elems += self.ref_point
        elems += self.t1
        elems += self.t2
        elems += self.t3
        return elems


class RotationReference(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        ply = spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))
        T = spira.Rotation(-30)
        S = spira.SRef(cell, transformation=T)
        return S

    def create_t2(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3))
        T = spira.GenericTransform(rotation=-60)
        S = spira.SRef(cell, transformation=T)
        return S

    def create_t3(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        S = spira.SRef(cell)
        S.rotate(-90)
        return S

    def create_elements(self, elems):
        elems += self.ref_point
        elems += self.t1
        elems += self.t2
        elems += self.t3
        return elems


class ReflectReference(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        ply = spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))
        T = spira.Reflection(True)
        S = spira.SRef(cell, transformation=T)
        return S

    def create_t2(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3))
        T = spira.GenericTransform(reflection=True)
        S = spira.SRef(cell, transformation=T)
        return S

    def create_t3(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        S = spira.SRef(cell)
        S.reflect(True)
        return S

    def create_elements(self, elems):
        elems += self.ref_point
        elems += self.t1
        elems += self.t2
        elems += self.t3
        return elems


class TransformReference(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')
    t2 = spira.Parameter(fdef_name='create_t2')
    t3 = spira.Parameter(fdef_name='create_t3')

    def create_ref_point(self):
        ply = spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        cell = spira.Cell()
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=2))

        S1 = spira.SRef(cell)
        S1.rotate(rotation=45)
        S1.translate(Coord(15, 15))

        S = spira.SRef(cell)
        S.rotate(rotation=45)
        S.translate(Coord(15, 15))
        S.reflect(True)

        return [S1, S]

    def create_t2(self):
        cell = spira.Cell()
        tf_1 = spira.GenericTransform(translation=(10, 10), rotation=45)
        tf_2 = spira.GenericTransform(translation=Coord(10, 10), rotation=45, reflection=True)
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=3))
        S1 = spira.SRef(cell, transformation=tf_1)
        S2 = spira.SRef(cell, transformation=tf_2)
        return [S1, S2]

    def create_t3(self):
        cell = spira.Cell()
        tf_1 = spira.Translation(Coord(12.5, 2.5)) + spira.Rotation(60)
        tf_2 = spira.Translation(Coord(12.5, 2.5)) + spira.Rotation(60) + spira.Reflection(True)
        cell += spira.Rectangle(p1=(0,0), p2=(10, 50), layer=spira.Layer(number=4))
        S1 = spira.SRef(cell, transformation=tf_1)
        S2 = spira.SRef(cell, transformation=tf_2)
        return [S1, S2]

    def create_elements(self, elems):
        elems += self.ref_point
        # elems += self.t1
        # elems += self.t2
        elems += self.t3
        return elems


# -------------------------------------------------------------------------------------------------------------------


cell = spira.Cell(name='Transformations')

t1 = TranslateReference()
# t1.gdsii_output()

t2 = RotationReference()
# t2.gdsii_output()

t3 = ReflectReference()
# t3.gdsii_output()

t4 = TransformReference()
t4.gdsii_output()

# cell += spira.SRef(t1, midpoint=(0, 0))
# cell += spira.SRef(t2, midpoint=(50, 0))
# cell += spira.SRef(t3, midpoint=(0, -100))
# cell += spira.SRef(t4, midpoint=(50, -100))

# cell.gdsii_output()


