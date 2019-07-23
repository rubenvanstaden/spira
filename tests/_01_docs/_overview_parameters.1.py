import spira.all as spira


class Layer(spira.ParameterInitializer):
    number = spira.Parameter(default=0, restrictions=spira.INTEGER, preprocess=spira.ProcessorInt(), doc='Advanced parameter.')


layer = Layer()
print(layer.number)

layer.number = 9
print(layer.number)

layer.number = 1.2
print(layer.number)

layer.number = '8'
print(layer.number)

layer.number = '1.2'
print(layer.number)

layer.number = 'Hi'
