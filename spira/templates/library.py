import spira
from spira.templates.templates import *

library = spira.Library(name='MiT-Library')

library.add_pcell(pcell=JunctionTemplate())


if __name__ == '__main__':
    library.output('DRL Library MitLL', collect_elements=True)
