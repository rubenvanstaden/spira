import spira
import time
from copy import copy, deepcopy
from spira.gdsii.io import current_path
from spira.lpe.circuits import Circuit
from spira.lpe.devices import Device, DeviceLayout
from demo.pdks.process.mitll_pdk.database import RDD


def __wrapper__(c, c2dmap):
    for e in c.elementals.sref:
        # S = deepcopy(e)
        if e.ref in c2dmap.keys():
            e.ref = c2dmap[e.ref]
            # print(S.ref)


def convert_cell(cell):
    c2dmap = {}
    # for key in RDD.DEVICES.keys:
    #     DeviceTCell = deepcopy(RDD.DEVICES[key].PCELL)
    #     DeviceTCell.center = (0,0)
    for C in cell.dependencies():
        if 'jj' in C.name:
            L = DeviceLayout(name=C.name, cell=C, level=1)
            for key in RDD.DEVICES.keys:
                if L.__type__ is not None:
                    if L.__type__ == key:
                        D = RDD.DEVICES[key].PCELL(metals=L.metals, contacts=L.contacts)
                        c2dmap.update({C: D})
        elif 'via' in C.name:
            L = DeviceLayout(name=C.name, cell=C, level=1)
            # for key in RDD.VIAS.keys:
            #     if L.__type__ is not None:
            #         if L.__type__ == key:
            #             D = RDD.VIAS[key].DEFAULT(metals=L.metals, contacts=L.contacts)
            #             c2dmap.update({C: D})
        else:
            c2dmap.update({C: C})
    for c in cell.dependencies():
        __wrapper__(c, c2dmap)
    # for e in c2dmap[cell].elementals:
    #     print(e)
    return c2dmap[cell]
    

    # d = self.dependencies()
    # c2dmap = {}
    # for c in d:
    #     D = c.commit_to_gdspy()
    #     c2dmap.update({c:D})
    # for c in d:
    #     self.__wrapper__(c, c2dmap)
    #     if c.name not in glib.cell_dict.keys():
    #         glib.add(c2dmap[c])
    # for p in self.get_ports():
    #     p.commit_to_gdspy(cell=c2dmap[self])
    # return c2dmap[self]


if __name__ == '__main__':

    start = time.time()

    # name = 'jj_mitll_2'
    # name = 'mitll_jtl_double'
    # name = 'mitll_dsndo_xic'
    # name = 'mitll_SFQDC_draft'
    # name = 'splitt_v0.3'
    # name = 'ex5'
    name = 'LSmitll_DCSFQ_new'

    filename = current_path(name)
    input_cell = spira.import_gds(filename=filename)
    # cell.output()

    cv_cell = convert_cell(cell=input_cell)

    # for e in cv_cell.elementals:
    #     print(e)

    cv_cell.output()

    # layout = Circuit(cell=cell, level=2)
    # layout.netlist
    # layout.mask.output()

    end = time.time()
    print(end - start)

