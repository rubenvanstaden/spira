import pytest as pytest
import spira.all as spira
from spira.core.parameters.processors import ProcessorFloat
from spira.core.parameters.processors import ProcessorInt

class Layer(spira.ParameterInitializer):
   integer = spira.IntegerParameter(default= "abcder", preprocess=spira.ProcessorInt())
   floateger = spira.FloatParameter(default = "2.12", preprocess = spira.ProcessorFloat())

layer = Layer()
print(layer.integer)

def test_int_invalidStr():
    with pytest.raises(ValueError) as e:
        layer.interger = "1.2"

def test_int_float():
    layer.interger = 1.2
    assert layer.interger == 1

def test_int_validStr():
    layer.interger = "4"
    assert layer.interger == 4




