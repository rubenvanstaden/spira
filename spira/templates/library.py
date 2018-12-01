import spira
from spira.templates.devices import *

library = spira.Library(name='MiT-Library')

library.add_pcell(pcell=JunctionModel())
# library += JunctionModel()


if __name__ == '__main__':
    library.output('DRL Library MitLL', collect_elements=True)
