import spira.all as spira


class Layer(spira.ParameterInitializer):
    number = spira.Parameter(default=0, preprocess=spira.ProcessorInt())
    int_number = spira.IntegerParameter(default=1, preprocess=spira.ProcessorInt())


# --- Test number

# layer = Layer()
# layer.number = 1
# print(layer.number)

# layer.number = 2.1
# print(layer.number)

# layer.number = 'Hi'
# print(layer.number)

# --- Test int_number

layer = Layer()
layer.int_number = 2
print(layer.int_number)

layer.int_number = 2.1
print(layer.int_number)

layer.int_number = "2"
print(layer.int_number)

# Still thows an error, but cannot be fixed right away,
# since we will have to apply compound casting like this: int(float(int_number))
layer.int_number = "2.1"
print(layer.int_number)

