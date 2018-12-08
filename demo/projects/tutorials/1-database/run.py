import spira
from spira import param
from spira import LOG
from spira import RDD

"""
This examples defines the creation of a basic parameterized cell.
This example shows the following:
1. How to link process data from the RDD to default parameter values.
2. How to change parameters when creating an instance.
3. How to switch to a different RDD by simply importing a new database file.
"""

class PCell(spira.Cell):

    layer = param.LayerField(number=RDD.BAS.LAYER.number)
    width = param.FloatField(default=RDD.BAS.WIDTH)

# -------------------------- Scripting ---------------------------

LOG.section('PCell paramters')
pcell = PCell()
print(pcell.layer)
print('width: {}'.format(pcell.width))

LOG.section('Update parameters')
pcell = PCell(width=3.4)
print('width: {}'.format(pcell.width))

LOG.section('Switch to different RDD')
print(RDD)
from demo.pdks.process.aist_pdk import database
print(RDD)


