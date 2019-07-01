import spira.all as spira


class Layer(spira.ParameterInitializer):
    number = spira.Parameter(default=0, preprocess=spira.ProcessorInt())


layer = Layer()
layer.number = 1
print(layer.number)

layer.number = 2.1
print(layer.number)

layer.number = 'Hi'
print(layer.number)
