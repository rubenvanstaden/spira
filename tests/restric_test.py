import pytest as pytest
import spira.all as spira
from spira.core.parameters.processors import ProcessorFloat
from spira.core.parameters.processors import ProcessorInt


class Layer(spira.ParameterInitializer):
    range_int = spira.IntegerParameter(restriction=spira.RestrictRange(lower=1, upper=5),preprocess=ProcessorInt())

layer = Layer()

def test_range_correct():
    layer.range_int = 3
    assert 3 == layer.range_int

def test_range_incorrect_bound():
    with pytest.raises(ValueError) as e:
        layer.range_int = 10


def test_range_string_correct():
    layer.range_int = "3"
    assert 3 == layer.range_int
#redundant
def test_int_param_correct():
    layer.range_int = 3.2
    assert 3 == layer.range_int    