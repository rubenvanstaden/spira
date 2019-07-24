import pytest
import spira.all as spira
from spira.yevon.geometry import shapes
import gdspy
import spira.yevon.io as io

roundspira = spira.BasicTriangle()
cell = spira.Cell(name="triangle")
cell += roundspira
cell.gdsii_output(name='triangle')