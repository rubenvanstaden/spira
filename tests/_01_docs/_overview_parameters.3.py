import spira.all as spira


class Layer(spira.ParameterInitializer):
    # number = spira.Parameter(default=0, restriction=spira.RestrictRange(2,5))
    number = spira.IntegerParameter(default=0, restriction=spira.RestrictRange(2,5))


layer = Layer()
layer.number = 3
print(layer.number)
layer.number = 6
print(layer.number)
layer.number = 1
print(layer.number)

