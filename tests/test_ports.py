import pytest
import numpy as np
import spira.all as spira


class PyCellA(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_elements(self, elems):
        elems += spira.Box(width=self.length, height=self.width, center=(0,0), layer=spira.RDD.PLAYER.R1.METAL)
        return elems


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_elements(self, elems):
        elems += spira.Box(width=self.length, height=self.width, center=(0,0), layer=spira.RDD.PLAYER.R1.METAL)
        return elems

    def create_ports(self, ports):
        w, l = self.width, self.length
        ports += spira.Port(name='R1:P1', midpoint=(-l/2,0), orientation=180, width=self.width)
        ports += spira.Port(name='P2', midpoint=(l/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)
        return ports


def test_ports():
    D = Resistor()
    p1 = D.ports[0]
    p2 = D.ports['R1:E0']
    assert str(p1.key) == "('R1:E0', 'R1', 'E', (0.0, 0.15))"
    assert p2.process.symbol == 'R1'
    assert p2.purpose.symbol == 'E'
    assert p2.midpoint == (0, 0.15)


test_ports()


def test_port_names():
    D = Resistor()

    edge_ports = D.ports.get_ports_by_purpose(spira.RDD.PURPOSE.PORT.EDGE)

    assert edge_ports[0].name == 'R1:E0'
    assert edge_ports[1].name == 'R1:E1'
    assert edge_ports[2].name == 'R1:E2'
    assert edge_ports[3].name == 'R1:E3'
    assert D.ports[-2].name == 'R1:P1'
    assert D.ports[-1].name == 'R1:P2'


def test_port_directions():
    D = Resistor()

    east_ports = D.ports.east_ports
    assert east_ports[0].orientation == 0
    assert east_ports[1].orientation == 0

    north_ports = D.ports.north_ports
    assert north_ports[0].orientation == 90

    west_ports = D.ports.west_ports
    assert west_ports[0].orientation == 180
    assert west_ports[1].orientation == 180

    south_ports = D.ports.south_ports
    assert south_ports[0].orientation == 270
    

def test_unlcok_ports():
    D = PyCellA()

    locked_ports = D.ports

    assert locked_ports[0].name == 'R1:E0'
    assert locked_ports[1].name == 'R1:E1'
    assert locked_ports[2].name == 'R1:E2'
    assert locked_ports[3].name == 'R1:E3'

    unlocked_ports = D.ports.unlock

    assert locked_ports[0].name == 'R1:P0'
    assert locked_ports[1].name == 'R1:P1'
    assert locked_ports[2].name == 'R1:P2'
    assert locked_ports[3].name == 'R1:P3'


def test_get_port_names():
    D = Resistor()
    names = ['R1:E0', 'R1:E1', 'R1:E2', 'R1:E3', 'R1:P1', 'R1:P2']
    np.testing.assert_array_equal(D.ports.get_names(), names)


def test_sort_ports():
    D = Resistor()

    unsorted_ports = D.ports

    assert unsorted_ports[0].orientation == 90
    assert unsorted_ports[1].orientation == 180
    assert unsorted_ports[2].orientation == 270
    assert unsorted_ports[3].orientation == 0
    assert unsorted_ports[4].orientation == 180
    assert unsorted_ports[5].orientation == 0

    sorted_ports = D.ports.angle_sorted(reference_angle=180)
    
    assert sorted_ports[0].orientation == 180
    assert sorted_ports[1].orientation == 180
    assert sorted_ports[2].orientation == 270
    assert sorted_ports[3].orientation == 0
    assert sorted_ports[4].orientation == 0
    assert sorted_ports[5].orientation == 90


def test_move():
    D = Resistor()

    # Move a single port.
    p1 = D.ports[0]
    assert p1.midpoint == (0, 0.15)
    p1.move(coordinate=(10,0))
    assert p1.midpoint == (10, 0.15)

    # Move a list of ports.
    ports = D.ports
    assert ports[0].midpoint == (10, 0.15)
    assert ports[1].midpoint == (-0.5, 0)
    assert ports[2].midpoint == (0, -0.15)

    moved_ports = D.ports.move(coordinate=(10, 0))
    assert moved_ports[0].midpoint == (20, 0.15)
    assert moved_ports[1].midpoint == (9.5, 0)
    assert moved_ports[2].midpoint == (10, -0.15)


def test_connect():
    pass


def test_distance_alignment():
    pass

