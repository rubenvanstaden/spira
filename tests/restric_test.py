import pytest as pytest
import spira.all as spira
from spira.core.parameters.processors import ProcessorFloat
from spira.core.parameters.processors import ProcessorInt


class Layer(spira.ParameterInitializer):
    range_int = spira.IntegerParameter(restriction=spira.RestrictRange(lower=1, upper=5))

layer = Layer()

def test_restric_range_correct():
    layer.range_int = 1
    assert 1 == layer.range_int

layer.range_int = 13