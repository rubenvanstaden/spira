import spira
from spira import param

class PCell(spira.Cell):

    width = param.FloatField(default=1)
    lenght = param.FloatField(default=3)

pcell = PCell()

print(pcell)
print(pcell.name)

from spira import settings
lib = settings.get_library()
print(lib.cells)

library = spira.Library(name='New Lib')
library += pcell

print(library)