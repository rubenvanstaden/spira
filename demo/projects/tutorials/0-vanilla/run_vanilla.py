import spira
from spira import LOG
from spira import param
from spira import shapes


pcell = spira.Cell(name='PCell')
pcell.layer = 4
pcell.width = 1

LOG.section('PCell instance')
print(pcell)
print(pcell.layer)
print(pcell.width)

pcell = spira.Cell(name='PCell')
pcell.width = 1
pcell.layer = spira.Layer(number=4)

LOG.section('PCell instance')
print(pcell)
print(pcell.width)
print(pcell.layer)
print(pcell.layer.number)
print(pcell.layer.datatype)


LOG.section('Creating shapes')
shape = shapes.BoxShape(center=(5,0), width=1, height=1)


# -------------------------------------------------------------------------


cell = spira.Cell(name='Multi-cell')
cell += spira.SRef(pcell)
cell.output()