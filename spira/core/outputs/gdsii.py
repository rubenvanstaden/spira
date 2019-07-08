import os
import gdspy
# import spira.all as spira

from spira import settings
from spira import log as LOG
from spira.yevon.gdsii import *
from spira.core.parameters.variables import *
from spira.core.mixin import MixinBowl
from spira.core.outputs.base import Outputs
from spira.core.parameters.initializer import ParameterInitializer


class OutputGdsii(ParameterInitializer):
    """ Collects the transformed elements to be send to Gdspy. """

    disabled_ports = DictParameter(default={}, doc='Disabled port categories for viewing.')

    def __init__(self, cell, **kwargs):

        super().__init__(**kwargs)

        self.__collected_cells__ = {}
        self.__collected_srefs__ = {}
        self.__collected_polygons__ = {}
        self.__collected_labels__ = {}

        self.gdspy_cell = self.collector(cell)

    def collect_labels(self, item, cl, extra_transform=None):
        if item.node_id in list(cl.keys()):
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
            # P = item.convert_to_gdspy(extra_transform)
            P = item.convert_to_gdspy()
            cp[item.id_string()] = P

    def collect_ports(self, cell):
        from spira.yevon.visualization.viewer import PortLayout
        _polygon_ports = []
        for c in cell.dependencies():
            cp, cl, C_ports = {}, {}, {}
            G = self.__collected_cells__[c]

            if self.disabled_ports['cells'] is True:
                for p in c.ports:
                    L = PortLayout(port=p)
                    for e in L.elements:
                        # if isinstance(e, Polygon):
                        if issubclass(type(e), Polygon):
                            self.collect_polygons(e, cp)
                        elif isinstance(e, Label):
                            self.collect_labels(e, cl)

            if self.disabled_ports['polygons'] is True:
                for e in c.elements:
                    if isinstance(e, Polygon):
                        if e.enable_edges is True:
                            for p in e.ports:
                            # Transform ports to polygon transformation.
                            # Required for non-pcell layouts. FIXME!!!
                            # for p in e.ports.transform(e.transformation):
                                if p.id_string() not in _polygon_ports:
    
                                    # L = PortLayout(port=p, transformation=e.transformation)
                                    # for e in L.elements:
                                    #     if isinstance(e, Polygon):
                                    #         self.collect_polygons(e, cp)
                                    #     elif isinstance(e, Label):
                                    #         self.collect_labels(e, cl)
    
                                    _polygon_ports.append(p.id_string())

            for e in cp.values():
                G.add(e)
            for e in cl.values():
                G.add(e)

    def collect_cells(self, cell):
        from spira.yevon.visualization.viewer import PortLayout
        for c in cell.dependencies():
            cp, cl = {}, {}
            G = self.__collected_cells__[c]
            for e in c.elements:
                if isinstance(e, Polygon):
                    self.collect_polygons(e, cp)
                elif isinstance(e, Label):
                    self.collect_labels(e, cl)

            for e in cp.values(): G.add(e)
            for e in cl.values(): G.add(e)

    def collect_srefs(self, cell):

        from spira.core.transformation import CompoundTransform
        from spira.core.transforms.generic import GenericTransform

        for c in cell.dependencies():
            G = self.__collected_cells__[c]
            cs = {}
            for e in c.elements:
                if isinstance(e, SRef):
                    if e.id_string() in list(self.__collected_srefs__.keys()):
                        pass
                    else:
                        # FIXME: Has to be removed for layout transformations.
                        # T = e.transformation + spira.Translation(e.midpoint)

                        T = e.transformation
                        e.midpoint = T.apply_to_coord(e.midpoint)
                        origin = e.midpoint.to_numpy_array()

                        rotation = 0
                        magnification = 1.0
                        reflection = False

                        if isinstance(T, CompoundTransform):
                            for t in T.__subtransforms__:
                                if isinstance(t, GenericTransform):
                                    rotation = t.rotation
                                    magnification = t.magnification
                                    reflection = t.reflection
                        else:
                            rotation = T.rotation
                            magnification = T.magnification
                            reflection = T.reflection

                        ref_cell = self.__collected_cells__[e.ref]

                        S = gdspy.CellReference(
                            ref_cell=ref_cell,
                            origin=origin,
                            rotation=rotation,
                            magnification=magnification,
                            x_reflection=reflection)

                        cs[e.id_string()] = S
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

        # NOTE: Gdspy cells must first be constructed, 
        # before adding them as references.
        self.collect_srefs(item)

    def gdspy_gdsii_output(self, library):
        """ Writes the SPiRA collected elements to a gdspy library. """
        for c, G in self.__collected_cells__.items():
            if c.name not in library.cell_dict.keys():
                library.add(G)


class GdsiiLayout(object):
    """
    Class that generates output formates for a layout or library containing layouts.
    If a name is given, the layout is written to a GDSII file.
    """

    def gdsii_expanded_output(self):
        D = self.expand_flat_copy()
        # print(D.ports)
        # D = self.flat_copy()
        D.gdsii_output()

    def gdsii_output(self, name=None, units=None, grid=None, layer_map=None, disabled_ports=None, view=True):

        _default = {'cells': True, 'polygons': True, 'arrows': True, 'labels': True}
        # _default = {'cells': True, 'polygons': False, 'arrows': False, 'labels': False}

        if disabled_ports is not None:
            _default.update(disabled_ports)

        G = OutputGdsii(cell=self, disabled_ports=_default)

        gdspy_library = gdspy.GdsLibrary(name=self.name)
        G.gdspy_gdsii_output(gdspy_library)

        if name is not None:
            writer = gdspy.GdsWriter('{}.gds'.format(name), unit=1.0e-6, precision=1.0e-12)
            for name, cell in gdspy_library.cell_dict.items():
                writer.write_cell(cell)
                del cell
            writer.close()

        if view is True:
            gdspy.LayoutViewer(library=gdspy_library)


Outputs.mixin(GdsiiLayout)



