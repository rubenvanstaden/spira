import spira.all as spira


ll = spira.LayerList()
ll += spira.Layer(1)
ll += spira.Layer(2)
print(ll)
# lf = spira.LayerFilterDelete(layers=ll)
lf = spira.LayerFilterAllow(layers=ll)
print(lf.layers)
print(len(lf.layers))

print(lf)

p1 = spira.Rectangle(layer=spira.Layer(1))
p2 = spira.Rectangle(layer=spira.Layer(3))

F = lf([p1, p2])
print(F)

