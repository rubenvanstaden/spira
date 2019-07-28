from spira.core.parameters.initializer import ParameterInitializer

 
class BasicInput(ParameterInitializer):
    i_stream = DefinitionProperty(default = sys.stdin) # add limitation

    def __init__(self, i_stream = sys.stdin, **kwargs):
        super(BasicInput, self).__init__(
            i_stream = i_stream,
            **kwargs)

    def read(self, size = None):
        if size is None:
            return self.parse(self.i_stream.read())
        else:
            return self.parse(self.i_stream.read(size))

    def parse(self, item):
        return item


class InputBasic(BasicInput):
    scaling = PositiveNumberProperty(default = 1.0)
    layer_map = DefinitionProperty()
    prefix = StringProperty(default = "")
    
    def __init__(self, i_stream = sys.stdin, **kwargs):
        super(InputBasic, self).__init__(
            i_stream = i_stream,
            **kwargs)
        self.library = None

    def read(self):
        return self.parse()        

    def parse(self):
        return self.parse_library()

    def parse_library(self):
        self.library = Library("IMPORT")
        self.__parse_library__()
        return self.library

    def map_layer(self, layer):
        L = self.layer_map.get(layer, None)
        if isinstance(L, __Layer__):
            return L
        elif L is None:
            return L
        else:
            return Layer(L)

    def make_structure_name(self, name):
        return self.prefix + name
    
    def define_layer_map(self):
        return TECH.GDSII.IMPORT_LAYER_MAP #FIXME : using 'default' for the property would be better, but that gives an exception ...



