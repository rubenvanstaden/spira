import spira
from spira.core import param
from spira.lrc.rules import __SingleLayerDesignRule__
from copy import deepcopy


RDD = spira.get_rule_deck()


class Width(__SingleLayerDesignRule__):
    minimum = param.FloatField(allow_none=True, default=None)
    maximum = param.FloatField(allow_none=True, default=None)

    def __repr__(self):
        return "'{}' must have a width between: min={} max={}".format(self.layer1, self.minimum, self.maximum)

    def edge_to_minimum_width(self, e1):
        ports = spira.ElementList()
        for p in e1.edge_ports:
            p.length = 2*self.minimum*self.um
            ports += p
        return ports

    def apply(self, e1):
        adjusted_edges = self.edge_to_minimum_width(e1=e1)
        for e in adjusted_edges:
            clip = e.edge
            subj = e1.polygon
            overlap = clip & subj
            if overlap:
                clip_area = round(clip.ply_area)
                overlap_area = round(overlap.ply_area)
                pct = 100*(1 - (clip_area-overlap_area)/clip_area)
                if pct < 50:
                    return False
                print(pct)
        return True


    

            

