import os
import gdspy
import spira.all as spira

from spira import settings
from spira import log as LOG
from spira.yevon.gdsii import *
from spira.core.mixin import MixinBowl
from spira.core.outputs.base import Outputs
from spira.core.parameters.initializer import FieldInitializer


class OutputGdsii(FieldInitializer):
    """ Collects the transformed elementals to be send to Gdspy. """

    def __init__(self, cell, **kwargs):

        self.__collected_cells__ = {}
        self.__collected_srefs__ = {}
        self.__collected_polygons__ = {}
        self.__collected_labels__ = {}

        self.gdspy_cell = self.collector(cell)

    def collect_labels(self, item, cl, extra_transform=None):
        if item.node_id in list(self.__collected_labels__.keys()):
            # L = self.__collected_labels__[item.node_id]
            pass
        else:
            L = item.convert_to_gdspy(extra_transform)
            cl[item.id_string()] = L
            # self.__collected_labels__.update({item.node_id:L})

    # def collect_polygons(self, item):
    #     """  """
    #     if item.id_string() in list(self.__collected_polygons__.keys()):
    #         # P = self.__collected_polygons__[item.id_string()]
    #         # P = item.convert_to_gdspy()
    #         # self.__collected_polygons__[item.id_string()] = P
    #         pass
    #     else:
    #         P = item.convert_to_gdspy()
    #         self.__collected_polygons__[item.id_string()] = P
    #         # self.__collected_polygons__.update({item.id_string():P})
    #     print(self.__collected_polygons__)

    def collect_polygons(self, item, cp, extra_transform=None):
        """  """
        if item.id_string() in list(cp.keys()):
            pass
        else:
            P = item.convert_to_gdspy(extra_transform)
            cp[item.id_string()] = P

    def collect_ports(self, cell):
        from spira.yevon.visualization.viewer import PortLayout
        for c in cell.dependencies():
            cp, cl = {}, {}
            G = self.__collected_cells__[c]
            _polygon_ports = []
            for e in c.elementals:
                if isinstance(e, Polygon):
                    for p in e.ports:

                        # self.collect_polygons(p.edge, cp, e.transformation)
                        # self.collect_polygons(p.arrow, cp, e.transformation)
                        # self.collect_labels(p.label, cl, e.transformation)

                        p.transform(e.transformation)
                        
                        L = PortLayout(port=p)
                        for e in L.elementals:
                            if isinstance(e, Polygon):
                                self.collect_polygons(e, cp)
                            elif isinstance(e, Label):
                                self.collect_labels(e, cl)

                        # self.collect_polygons(p.edge, cp)
                        # self.collect_polygons(p.arrow, cp)
                        # self.collect_labels(p.label, cl)

                        _polygon_ports.append(p.id_string())
            # for p in c.ports:
            #     if p.id_string() not in _polygon_ports:
            #         self.collect_polygons(p.edge, cp)
            #         self.collect_polygons(p.arrow, cp)
            #         self.collect_labels(p.label, cl)

            for e in cp.values():
                G.add(e)
            for e in cl.values():
                G.add(e)

    def collect_cells(self, cell):
        from spira.yevon.visualization.viewer import PortLayout
        for c in cell.dependencies():
            cp, cl = {}, {}
            G = self.__collected_cells__[c]
            for e in c.elementals:
                if isinstance(e, Polygon):
                    self.collect_polygons(e, cp)
                elif isinstance(e, Label):
                    self.collect_labels(e, cl)

            for p in c.ports:
                # self.collect_polygons(p.edge, cp)
                L = PortLayout(port=p)
                for e in L.elementals:
                    if isinstance(e, Polygon):
                        self.collect_polygons(e, cp)
                    elif isinstance(e, Label):
                        self.collect_labels(e, cl)
                

            for e in cp.values():
                G.add(e)
            for e in cl.values():
                G.add(e)
            
            # for e in self.__collected_polygons__.values():
            #     G.add(e)
            # for e in self.__collected_labels__.values():
            #     G.add(e)

    def collect_srefs(self, cell):
        for c in cell.dependencies():
            G = self.__collected_cells__[c]
            cs = {}
            for e in c.elementals:
                if isinstance(e, SRef):
                    if e.id_string() in list(self.__collected_srefs__.keys()):
                        pass
                    else:
                        # FIXME: Has to be removed for layout transformations.
                        T = e.transformation
                        # T = e.transformation + spira.Translation(e.midpoint)
                        e.midpoint = T.apply_to_coord(e.midpoint)
                        ref_cell = self.__collected_cells__[e.ref]
                        S = gdspy.CellReference(
                            ref_cell=ref_cell,
                            origin=e.midpoint.to_numpy_array(),
                            rotation=T.rotation,
                            magnification=T.magnification,
                            x_reflection=T.reflection)
                        # self.__collected_srefs__.update({e.id_string():S})
                        cs[e.id_string()] = S
        # for e in self.__collected_srefs__.values():
            for e in cs.values():
                G.add(e)

    def collector(self, item):

        for c in item.dependencies():
            G = gdspy.Cell(c.name, exclude_from_current=True)
            self.__collected_cells__.update({c:G})

        # NOTE: First collect all port polygons and labels,
        # before commiting them to a cell instance.
        self.collect_ports(item)
        self.collect_cells(item)

        # for c in item.dependencies():
        #     G = self.__collected_cells__[c]
        #     for e, p in self.__collected_polygons__.items():
        #         print(e)
        #         print(p)
        #         print('')
        #         G.add(e)
        #     # for e in self.__collected_labels__.values():
        #     #     G.add(e)

        # NOTE: Gdspy cells must first be constructed, 
        # before adding them as references.
        self.collect_srefs(item)

    def gdspy_output(self, library):
        """ Writes the SPiRA collected elementals to a gdspy library. """
        for c, G in self.__collected_cells__.items():
            if c.name not in library.cell_dict.keys():
                library.add(G)


class GdsiiLayout(object):
    """ Class that generates output formates
    for a layout or library containing layouts. """

    def output(self, name=None, units=None, grid=None, layer_map=None):
        gdspy_library = gdspy.GdsLibrary(name=self.name)

        # self.construct_gdspy_tree(glib)

        G = OutputGdsii(cell=self)
        G.gdspy_output(gdspy_library)

        gdspy.LayoutViewer(library=gdspy_library)

    # def output(self, name=None, cell=None):
    #     from spira.yevon.gdsii.cell import __Cell__

    #     glib = gdspy.GdsLibrary(name=self.name)

    #     if isinstance(self, spira.Library):
    #         glib = settings.get_library()
    #         glib += self
    #         glib.to_gdspy
    #     elif issubclass(type(self), __Cell__):
    #         self.construct_gdspy_tree(glib)

    #     if cell is None:
    #         gdspy.LayoutViewer(library=glib)
    #     else:
    #         gdspy.LayoutViewer(library=glib, cells=cell)

    #     # gdspy.LayoutViewer(library=glib, cells='Circuit_AiST_CELL_1')
    #     # gdspy.LayoutViewer(library=glib, cells='LayoutConstructor_AiST_CELL_1')

    # # FIXME!
    # def writer(self, name=None, file_type='gdsii'):
    #     if name is None:
    #         file_name = '{}.gds'.format(self.name)
    #     else:
    #         file_name = '{}.gds'.format(name)
    #     glib = gdspy.GdsLibrary(name=self.name)
    #     writer = gdspy.GdsWriter(file_name, unit=1.0e-6, precision=1.0e-6)
    #     cell = self.construct_gdspy_tree(glib)
    #     writer.write_cell(cell)
    #     del cell
    #     writer.close()


Outputs.mixin(GdsiiLayout)



