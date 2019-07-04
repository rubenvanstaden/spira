import spira.all as spira

R = spira.Rotation(30)
T = spira.Translation((30, 0))
F = spira.Reflection(True)

G0 = R + T + F
G1 = spira.GenericTransform(translation=spira.Coord(-10, 0), rotation=45)
G2 = spira.GenericTransform(translation=spira.Coord(-10, 0), rotation=45, reflection=True)
G3 = spira.GenericTransform()
G3 += R
G3 += T
G3 += F

print(R)
print(type(R))
print('')

print(T)
print(type(T))
print('')

print(F)
print(type(F))
print('')

print(G0)
print(type(G0))
print('')

print(G1)
print(type(G1))
print('')

print(G2)
print(type(G2))
print('')

print(G3)
print(type(G3))
print('')
