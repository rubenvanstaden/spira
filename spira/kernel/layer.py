from spira.kernel.parameters.initializer import BaseElement
from spira.kernel import parameters as param


class __Layer__(BaseElement):
    pass


class Layer(__Layer__):

    name = param.StringField()
    number = param.IntegerField()
    datatype = param.IntegerField()

    def __init__(self, **kwargs):
        BaseElement.__init__(self, **kwargs)

    def __repr__(self):
        string = '[SPiRA: Layer] (\'{}\', layer {}, datatype {})'
        return string.format(self.name, self.number, self.datatype)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return self.key != other.key

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


from spira.kernel.parameters.descriptor import DataFieldDescriptor
def LayerField(name='', number=0, datatype=0):
    F = Layer(name=name, number=number, datatype=datatype)
    return DataFieldDescriptor(default=F)




    
