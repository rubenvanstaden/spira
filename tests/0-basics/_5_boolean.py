import spira.all as spira
from spira.yevon.geometry import shapes


# Boolean operations on the shapes
# --------------------------------

s1 = shapes.CircleShape(box_size=(2*1e6,2*1e6))
s2 = shapes.CircleShape(box_size=(2*1e6,2*1e6), center=(1*1e6,0))

p1 = spira.Polygon(shape=s1, layer=spira.Layer(1))
p2 = spira.Polygon(shape=s2, layer=spira.Layer(1))

elems = [p1, p2]
for bs in s1 & s2:
    elems.append(spira.Polygon(shape=bs, layer=spira.Layer(2)))
for bs in s1 - s2:
    elems.append(spira.Polygon(shape=bs, layer=spira.Layer(3)))
for bs in s2 - s1:
    elems.append(spira.Polygon(shape=bs, layer=spira.Layer(4)))
for bs in s1 | s2:
    elems.append(spira.Polygon(shape=bs, layer=spira.Layer(5)))

c1 = spira.Cell(elementals=elems)
# c1.output()


# Boolean operations on the polygons
# ----------------------------------

b_and = p1 & p2
for b in b_and:
    b.layer = spira.Layer(2)

b_sub1 = p1 - p2
for b in b_sub1:
    b.layer = spira.Layer(3)

b_sub2 = p2 - p1
for b in b_sub2:
    b.layer = spira.Layer(4)

b_or = p1 | p2
for b in b_or:
    b.layer = spira.Layer(5)

c2 = spira.Cell(elementals=b_and + b_sub1 + b_sub2 + b_or)
c2.output()


