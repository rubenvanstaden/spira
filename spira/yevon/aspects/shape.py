import numpy as np
from spira.yevon.utils import clipping
from spira.yevon.aspects.clipper import __ClipperAspects__


class ShapeClipperAspects(__ClipperAspects__):
    """

    Examples
    --------
    """

    def __and__(self, other):
        return clipping.boolean(subj=[self.points], clip=[other.points], clip_type='and')

    def __sub__(self, other):
        return clipping.boolean(subj=[self.points], clip=[other.points], clip_type='not')

    def __or__(self, other):
        return clipping.boolean(subj=[self.points], clip=[other.points], clip_type='or')
