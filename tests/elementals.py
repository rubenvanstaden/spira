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
        layer = param.LayerField()
        violate = param.BoolField()
    a = CellA()
    assert a.layer.number == 0
    assert a.violate == False

    a.layer.number = 10
    assert a.layer.number == 10

def test_default_parameters():
    class CellB(spira.Cell):
        layer = param.LayerField(number=18)
        violate = param.BoolField(default=True)
    b = CellB()
    assert b.layer.number == 18
    assert b.violate == True



# -------------------------------------------- spira.Cell -------------------------------------------

# -------------------------------------------- spira.SRef -------------------------------------------

# -------------------------------------------- spira.Polygon ----------------------------------------

# -------------------------------------------- spira.Label ------------------------------------------

# -------------------------------------------- spira.Port -------------------------------------------

# -------------------------------------------- spira.Path -------------------------------------------







