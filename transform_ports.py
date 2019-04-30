import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class ProcessLayer(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')

    width = spira.NumberField(default=10)
    length = spira.NumberField(default=50)

    def get_transforms(self):
        # T = spira.Translation(Coord(10*1e6, 0)) + spira.Rotation(rotation=60)
        T = spira.Translation(Coord(10*1e6, 0))
        T += spira.Rotation(rotation=60)
        return T

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5*1e6, -2.5*1e6), p2=(2.5*1e6, 2.5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        shape = shapes.RectangleShape(p1=(0,0), p2=(self.width*1e6, self.length*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        T = self.get_transforms()
        ply.transform(transformation=T)
        return ply

    def create_elementals(self, elems):

        elems += self.ref_point
        elems += self.t1

        return elems

    def create_ports(self, ports):

        T = self.get_transforms()

        p1 = spira.Terminal(midpoint=(self.width/2*1e6, 0), orientation=180, width=self.width*1e6)
        p2 = spira.Terminal(midpoint=(self.width/2*1e6, self.length*1e6), orientation=0, width=self.width*1e6)

        ports += p1.transform_copy(T)
        ports += p2.transform_copy(T)

        return ports


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


class HorizontalConnections(spira.Cell):

    def create_elementals(self, elems):

        pc = ProcessLayer()

        S = spira.SRef(pc, midpoint=(0,0))

        S.connect(port=pc.ports[0], destination=self.ports[0])

        elems += S

        return elems

    def create_ports(self, ports):
        
        p1 = spira.Terminal(midpoint=(50*1e6, 0), orientation=90, width=10*1e6)

        ports += p1

        return ports


# -------------------------------------------------------------------------------------------------------------------


cell = spira.Cell(name='Transformations')

# t1 = ProcessLayer()
# t1.output()

D = HorizontalConnections()
D.output()

# cell.output()


