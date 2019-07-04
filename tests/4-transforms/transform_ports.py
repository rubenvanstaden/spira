import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class ProcessLayer(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')
    t1 = spira.DataField(fdef_name='create_t1')

    width = spira.NumberField(default=10)
    length = spira.NumberField(default=50)

    def get_transforms(self):
        # T = spira.Translation(Coord(10, 0)) + spira.Rotation(rotation=60)
        T = spira.Translation(Coord(10, 0))
        T += spira.Rotation(rotation=0)
        return T

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5, -2.5), p2=(2.5, 2.5))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_t1(self):
        shape = shapes.RectangleShape(p1=(0,0), p2=(self.width, self.length))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=10))
        T = self.get_transforms()
        ply.transform(transformation=T)
        return ply

    def create_elementals(self, elems):

        # elems += self.ref_point
        elems += self.t1

        return elems

    def create_ports(self, ports):

        T = self.get_transforms()

        p1 = spira.Terminal(midpoint=(self.width/2, 0), orientation=-90, width=self.width)
        p2 = spira.Terminal(midpoint=(self.width/2, self.length), orientation=90, width=self.width)

        # ports += [p1, p2]

        ports += p1.transform_copy(T)
        ports += p2.transform_copy(T)

        return ports


class HorizontalConnections(spira.Cell):

    ref_point = spira.DataField(fdef_name='create_ref_point')

    def create_ref_point(self):
        shape = shapes.RectangleShape(p1=(-2.5, -2.5), p2=(2.5, 2.5))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        return ply

    def create_elementals(self, elems):

        pc = ProcessLayer()
        elems += self.ref_point

        T = spira.Rotation(0)
        # T += spira.vector_match_transform(v1=pc.ports[0], v2=self.ports[0])
        S = spira.SRef(pc, midpoint=(10,0), transformation=T)

        # print(S.ports)
        S.ports
        print(S.transformation)
        S.connect(port=S.ports[0], destination=self.ports[0])
        S.ports
        print(S.transformation)
        # print(S.ports)

        elems += S

        return elems

    def create_ports(self, ports):

        p1 = spira.Terminal(midpoint=(50, 0), orientation=135, width=10)

        ports += p1

        return ports


class HorizontalAlignment(spira.Cell):

    def create_elementals(self, elems):

        pc = ProcessLayer()

        S = spira.SRef(pc, midpoint=(0,0))

        S.align(port=pc.ports[0], destination=self.ports[0], distance=20)

        elems += S

        return elems

    def create_ports(self, ports):

        p1 = spira.Terminal(midpoint=(50, 0), orientation=330, width=10)

        ports += p1

        return ports


# -------------------------------------------------------------------------------------------------------------------


# cell = spira.Cell(name='Transformations')

# D = ProcessLayer()
D = HorizontalConnections()
# D = HorizontalAlignment()
D.output()

# cell.output()


