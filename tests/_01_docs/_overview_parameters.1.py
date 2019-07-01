import spira.all as spira


class Layer(spira.ParameterInitializer):
    number = spira.Parameter(default=0, restrictions=spira.INTEGER, preprocess=spira.ProcessorInt(), doc='Advanced parameter.')


# layer = Layer()
# layer.number
# 0
# layer.number = 9
# layer.number
# 9
# layer.number = '8'
# layer.number
# 8
# layer.number = 'Hi'
