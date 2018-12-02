import pytest
import spira
from spira import param


# ======================================================================================================
# To run tests:
# python -m pytest -v elementals.py 
# ======================================================================================================

# ---------------------------------------------- Test Fiels --------------------------------------------

def test_layerfield():
    class TestCell(spira.Cell):
        layer = param.LayerField()
    p = TestCell()
    assert p.layer.number == 0

    p.layer.number = 10
    assert p.layer.number == 10

    class TestCell(spira.Cell):
        layer = param.LayerField(number=18)
    p = TestCell()
    assert p.layer.number == 18

def test_boolfield():
    class TestCell(spira.Cell):
        violate = param.BoolField()
    p = TestCell()
    assert p.violate == False

    p.violate = True
    assert p.violate == True

    class TestCell(spira.Cell):
        violate = param.BoolField(default=True)
    p = TestCell()
    assert p.violate == True


# ---------------------------------------------- spira.Cell --------------------------------------------

# ---------------------------------------------- spira.SRef --------------------------------------------

# ---------------------------------------------- spira.Polygon -----------------------------------------

# ---------------------------------------------- spira.Label -------------------------------------------

# ---------------------------------------------- spira.Port --------------------------------------------

# ---------------------------------------------- spira.Path --------------------------------------------







