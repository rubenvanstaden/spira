import pytest
import numpy as np
import spira.all as spira


class Resistor(spira.PCell):

    width = spira.FloatParameter(default=0.3, doc='Width of the shunt resistance.')
    length = spira.FloatParameter(default=1.0, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True


def test_parameters():
    D = Resistor()
    assert D.width == 0.3
    assert D.length == 1.0

    D.width = 0.5
    assert D.width == 0.5


def test_add_polygon():
    c1 = spira.Cell(name='CellA')

    assert len(c1.elements) == 0

    c1 += spira.Polygon(shape=[[[0,0], [1,0], [1,1], [0,1]]], layer=spira.Layer(0))
    assert len(c1.elements) == 1

    c1.elements += spira.Polygon(shape=[[[0,0], [1,0], [1,1], [0,1]]], layer=spira.Layer(0))
    assert len(c1.elements) == 2
    

def test_move():
    c1 = spira.Cell(name='CellA')
    
    c1 += spira.Polygon(shape=[[0,0], [1,0], [1,1], [0,1]], layer=spira.Layer(1))

    c1.center = (0,0)
    np.testing.assert_array_equal(c1.center.to_numpy_array(), [0,0])

    c1.move(midpoint=c1.center, destination=(5,0))
    np.testing.assert_array_equal(c1.center.to_numpy_array(), [5,0])


def test_stretch_p2p():
    pass


def test_name_generator():
    pass


def test_deepcopy():
    pass


def test_copy():
    pass



