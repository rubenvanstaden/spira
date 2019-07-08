import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord


class ProcessLayer(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')
    t1 = spira.Parameter(fdef_name='create_t1')

    width = spira.NumberParameter(default=10)
    length = spira.NumberParameter(default=50)

    def get_transforms(self):
        # T = spira.Translation(Coord(10, 0)) + spira.Rotation(rotation=60)
        T = spira.Translation(Coord(10, 0))
        T += spira.Rotation(rotation=20)
        return T

    def create_ref_point(self):
        return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

    def create_t1(self):
        T = self.get_transforms()
        ply = spira.Rectangle(p1=(0,0), p2=(self.width, self.length), layer=spira.Layer(number=2))
        ply.transform(transformation=T)
        return ply

    def create_elements(self, elems):
        # elems += self.ref_point
        elems += self.t1
        return elems

    def create_ports(self, ports):
        T = self.get_transforms()
        p1 = spira.Port(name='P1_M1', midpoint=(self.width/2, 0), orientation=-90, width=self.width)
        p2 = spira.Port(name='P2_M1', midpoint=(self.width/2, self.length), orientation=90, width=self.width)
        ports += p1.transform_copy(T)
        ports += p2.transform_copy(T)
        return ports


class HorizontalConnections(spira.Cell):

    ref_point = spira.Parameter(fdef_name='create_ref_point')

    def create_ref_point(self):
        return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

    def get_ports(self):
        p1 = spira.Port(name='P1_M1', midpoint=(50, 0), orientation=135, width=10)
        return [p1]

    def create_elements(self, elems):
        elems += self.ref_point
        pc = ProcessLayer()
        T = spira.Rotation(0)
        S = spira.SRef(pc, midpoint=(10,0), transformation=T)
        p1 = self.get_ports()[0]
        S.connect(port=S.ports[0], destination=p1)
        elems += S
        return elems

    def create_ports(self, ports):
        ports += self.get_ports()
        return ports


class HorizontalAlignment(spira.Cell):
    
    ref_point = spira.Parameter(fdef_name='create_ref_point')
    
    def create_ref_point(self):
        return spira.Rectangle(p1=(-2.5, -2.5), p2=(2.5, 2.5), layer=spira.Layer(number=1))

    def get_ports(self):
        p1 = spira.Port(name='P1_M1', midpoint=(50, 0), orientation=330, width=10)
        return [p1]

    def create_elements(self, elems):
        elems += self.ref_point
        pc = ProcessLayer()
        S = spira.SRef(pc, midpoint=(0,0))
        p1 = self.get_ports()[0]
        S.distance_alignment(port=pc.ports[0], destination=p1, distance=20)
        elems += S
        return elems

    def create_ports(self, ports):
        ports += self.get_ports()
        return ports


# -------------------------------------------------------------------------------------------------------------------


# cell = spira.Cell(name='Transformations')

# D = ProcessLayer()
# D = HorizontalConnections()
D = HorizontalAlignment()
D.gdsii_output()

# cell.output()


