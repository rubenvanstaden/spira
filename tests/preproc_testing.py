import pytest as pytest
import spira.all as spira
from spira.core.parameters.processors import ProcessorFloat
from spira.core.parameters.processors import ProcessorInt

class Layer(spira.ParameterInitializer):
   integer = spira.IntegerParameter(default= 1, preprocess=spira.ProcessorInt())
   floateger = spira.FloatParameter(default = 2.12, preprocess = spira.ProcessorFloat())

layer = Layer()

def test_int_invalidStr():
    with pytest.raises(ValueError) as e:
            layer.integer = "1.2"

def test_int_float():
    layer.interger = 1.2
    print(layer.integer)
    assert layer.integer == 1

def test_int_validStr():
    layer.integer = "4"
    assert layer.integer == 4

def test_float_float():
    layer.floateger = 1.2
    assert layer.floateger == 1.2

def test_float_validStr():
    layer.floateger = "4.2"
    assert layer.floateger == 4.2


