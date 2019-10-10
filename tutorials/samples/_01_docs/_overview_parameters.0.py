import spira.all as spira


class Layer(spira.ParameterInitializer):
    number = spira.Parameter()


layer = Layer(number=9)
print(layer.number)
