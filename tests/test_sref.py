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
        

class PyCell(spira.Cell):
    def create_elementals(self, elems):
        elems += spira.Polygon(shape=[[[0,0], [3,0], [3,1], [0,1]]], layer=spira.Layer(0))
        return elems


def test_create():
    s = spira.SRef(reference=PyCell())
    assert all([a == b for a, b in zip(s.midpoint, [0,0])])
    assert s.transformation.translation == (0, 0)
    assert s.transformation.rotation == 0
    assert s.transformation.magnification == 1
    assert s.transformation.reflection == False


def test_deepcopy():
    pass


def test_copy():
    pass


def test_expand_transform():
    pass


def test_expand_flat_copy():
    pass


def test_flatten():
    pass


def test_move():
    pass


def test_connect():
    pass


def test_ditance_alignment():
    pass


def test_center_alignment():
    pass


def test_port_alignment():
    pass


def test_stretch_by_factor():
    pass


def test_stretch_p2c():
    pass


def test_stretch_p2p():
    pass



