import spira.all as spira


layer1 = spira.Layer(1)
layer2 = spira.Layer(2)
layer3 = spira.Layer(3)

constructor_layer1 = layer1 & layer2
# layer_and = layer1 & layer2 & layer3

print(constructor_layer1)
print(type(constructor_layer1))

p0 = spira.Rectangle(alias='P0', p1=(0, 0), p2=(10*1e6, 10*1e6), layer=spira.Layer(1))
p1 = spira.Rectangle(alias='P1', p1=(4*1e6, 2*1e6), p2=(6*1e6, 8*1e6), layer=spira.Layer(2))

elems = spira.ElementalList()
elems += p0
elems += p1

mapping = {
    constructor_layer1 : spira.Layer(7),
    # layer2: spira.Layer(6)
}

from spira.yevon.utils.elementals import get_generated_elementals
output_elems = get_generated_elementals(elements=elems, mapping=mapping)

D = spira.Cell(elementals=output_elems)
D.output()



