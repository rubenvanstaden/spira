import os
import gdspy
# import spira.all as spira

from spira import settings
from spira import log as LOG
from spira.yevon.gdsii import *
from spira.yevon.gdsii.polygon import __ShapeElement__
from spira.core.parameters.variables import *
from spira.core.parameters.restrictions import RestrictValueList
from spira.core.mixin import MixinBowl
from spira.core.outputs.base import Outputs
from spira.core.parameters.initializer import ParameterInitializer


class OutputGdsii(ParameterInitializer):
    """ Collects the transformed elements to be send to Gdspy. """

    disabled_ports = DictParameter(default={}, doc='Disabled port categories for viewing.')
    view_type = StringParameter(default='hierarchical', restriction=RestrictValueList(['hierarchical', 'flatten', 'expanded']))

    def __init__(self, cell, **kwargs):

        super().__init__(**kwargs)

        self.__collected_cells__ = {}
        self.__collected_srefs__ = {}
        self.__collected_polygons__ = {}
        self.__collected_labels__ = {}

        self.gdspy_cell = self.collector(cell)

    def collect_labels(self, item, cl, extra_transform=None):
        if item.node_id not in list(cl.keys()):
            L = item.convert_to_gdspy(extra_transform)
            cl[item.id_string()] = L

    def collect_polygons(self, item, cp, extra_transform=None):
        if item.id_string() not in list(cp.keys()):
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
                    # if isinstance(e, __ShapeElement__):
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
                if isinstance(e, __ShapeElement__):
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
                    if e.id_string() not in list(self.__collected_srefs__.keys()):

                        T = e.transformation + spira.Translation(e.midpoint)
                        c = Coord(0,0).transform(T)
                        origin = c.to_numpy_array()

                        rotation = 0
                        reflection = False
                        magnification = 1.0

                        if isinstance(T, CompoundTransform):
                            for t in T.__subtransforms__:
                                if isinstance(t, GenericTransform):
                                    rotation = t.rotation
                                    reflection = t.reflection
                                    magnification = t.magnification
                        else:
                            rotation = T.rotation
                            reflection = T.reflection
                            magnification = T.magnification

                        ref_cell = self.__collected_cells__[e.reference]

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


class GdsiiLayout(ParameterInitializer):
    """
    Class that generates output formates for a layout or library containing layouts.
    If a name is given, the layout is written to a GDSII file.
    """

    def gdsii_output_flat(self, name=None):
        D = self.flat_copy()
        D.gdsii_output(name=name, view_type='flatten')

    def gdsii_output_expanded(self, name=None):
        D = self.expand_transform()
        D.gdsii_output(name=name, view_type='expanded')

    def gdsii_output(self, name=None, view_type='hierarchical', disabled_ports=None, view=True):

        _default = {'cells': True, 'polygons': True, 'arrows': True, 'labels': True}
        # _default = {'cells': True, 'polygons': False, 'arrows': False, 'labels': False}

        if disabled_ports is not None:
            _default.update(disabled_ports)

        G = OutputGdsii(cell=self, view_type=view_type, disabled_ports=_default)

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





# class GdsiiLayout(ParameterInitializer):
#     """
#     Class that generates output formates for a layout or library containing layouts.
#     If a name is given, the layout is written to a GDSII file.
#     """

#     name = StringParameter(allow_none=True, default=None, doc='If not None write to gds file.')
#     view = BoolParameter(default=True, doc='If true the output the layout in gdspy viewer.')
#     disabled_ports = DictParameter(default={}, doc='Disabled port categories for viewing.')
#     view_type = StringParameter(default='hierarchical', restriction=RestrictValueList(['hierarchical', 'flatten', 'expanded']))

#     def output(self):

#         _default = {'cells': True, 'polygons': True, 'arrows': True, 'labels': True}
#         # _default = {'cells': True, 'polygons': False, 'arrows': False, 'labels': False}

#         if disabled_ports is not None:
#             _default.update(disabled_ports)

#         if self.view_type == 'hierarchical':
#             D = self
#         elif self.view_type == 'flatten':
#             D = self.flat_copy()
#         elif self.view_type == 'expanded':
#             D = self.expanded_transform()

#         G = OutputGdsii(cell=D, view_type=self.view_type, disabled_ports=_default)

#         gdspy_library = gdspy.GdsLibrary(name=D.name)
#         G.gdspy_gdsii_output(gdspy_library)

#         if name is not None:
#             writer = gdspy.GdsWriter('{}.gds'.format(name), unit=1.0e-6, precision=1.0e-12)
#             for name, cell in gdspy_library.cell_dict.items():
#                 writer.write_cell(cell)
#                 del cell
#             writer.close()

#         if view is True:
#             gdspy.LayoutViewer(library=gdspy_library)


# def gdsii_output(self, name=None, view_type='hierarchical', disabled_ports=None, view=True):

#     G = GdsiiLayout(name=name, view_type=view_type, disabled_ports=disabled_ports, view=view)
#     G.output()
