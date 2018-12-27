import pytest
import spira
from spira import param

# ===================================================================================================
# To run tests:
# python -m pytest -v elementals.py 
# ===================================================================================================

# -------------------------------------------- Test Fiels -------------------------------------------

def test_parameters():
    class CellA(spira.Cell):
        layer = param.LayerField(number=18, datatype=1)
        boolean = param.BoolField(default=False)
        fvalue = param.FloatField(default=0.0)

    a = CellA()

    assert a.layer.number == 18
    assert a.layer.datatype == 1
    assert a.boolean == False
    assert a.fvalue == 0.0

    a.layer.number = 10
    assert a.layer.number == 10







