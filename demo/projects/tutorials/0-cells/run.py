import spira
from spira import param
from spira import LOG

"""
This examples defines the creation of a basic parameterized cell.
This example shows the following:
1. How to create a layout generator by inheriting from Cell.
2. How class attributes are defined as parameters.
3. The three different ways how a cell can be added to a library.
"""

class PCell(spira.Cell):

    layer = param.LayerField(default=4)
    width = param.FloatField(default=1)

# -------------------------- Scripting ---------------------------

# Create a PCell instance.
pcell = PCell()
LOG.section('PCell instance')
print(pcell)

# When a cell is created it is automatically added
# to SPiRA's default library class. The currently
# set library can be retrieved and analyzed.
from spira import settings
lib_default = settings.get_library()
LOG.section('Default library')
print(lib_default)

lib_new = spira.Library(name='New Lib')
lib_new += pcell
LOG.section('Create and add to new library')
print(lib_new)
