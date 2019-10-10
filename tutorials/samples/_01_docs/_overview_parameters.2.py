import spira.all as spira


class Layer(spira.ParameterInitializer):
    number = spira.Parameter(default=0)
    datatype = spira.Parameter(fdef_name='create_datatype')

    def create_datatype(self):
        return 2 + 3


layer = Layer()
print(layer.number)
print(layer.datatype)

