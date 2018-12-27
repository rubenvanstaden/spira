from spira import param
from spira.core.initializer import ElementalInitializer


class __Layer__(ElementalInitializer):
    pass


class Layer(__Layer__):

    doc = param.StringField()
    name = param.StringField()
    number = param.IntegerField()
    datatype = param.IntegerField()

    def __init__(self, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

    # def __repr__(self):
    #     string = '[SPiRA: Layer] (\'{}\', layer {}, datatype {})'
    #     return string.format(self.name, self.number, self.datatype)

    # def __str__(self):
    #     return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, Layer):
            return self.key == other.key
        elif isinstance(other, PurposeLayer):
            return self.number == other.datatype
        else:
            raise ValueError('Not Implemented!')

    def __neq__(self, other):
        if isinstance(other, Layer):
            return self.key != other.key
        elif isinstance(other, PurposeLayer):
            return self.number != other.datatype
        else:
            raise ValueError('Not Implemented!')

    def __add__(self, other):
        assert isinstance(other, int)
        self.number = self.number + other
        return self

    def __deepcopy__(self, memo):
        return Layer(name=self.name,
                     number=self.number,
                     datatype=self.datatype)

    @property
    def key(self):
        return (self.number, self.datatype)



