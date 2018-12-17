from spira.core.lists import ElementList
import numpy as np


class InspectMixin(object):

    def get_mlayers(self, layer):
        from spira.lpe.layers import MLayer
        from spira.gdsii.elemental.polygons import Polygons
        elems = ElementList()
        for S in self.elementals.sref:
            if isinstance(S.ref, MLayer):
                if S.ref.layer.number == layer:
                    for p in S.ref.elementals:
                        # FIXME!!!
                        # if isinstance(p, ELayers):
                            # raise Errors
                        if isinstance(p, Polygons):
                            elems += p
        return elems


    @property
    def bbox(self):
        bbox = self.get_bounding_box()
        if bbox is None:  bbox = ((0,0),(0,0))
        return np.array(bbox)

    @property
    def polygon_points(self):
        return self.get_polygons()

#     @property
#     def ports(self):
#         return self.elementals.ports

    @property
    def graph(self):
        return self.elementals.graph

    @property
    def subgraphs(self):
        return self.elementals.subgraphs

    @property
    def id(self):
        return self.__id__

    @id.setter
    def id(self, _id):
        self.__id__ = _id

    def metal_polygons(self):

        elems = ElementList()

        for p in self.elementals.polygons:
            if p.gdslayer.number in RDD.METALS.layers:
                elems += p
        return elems

