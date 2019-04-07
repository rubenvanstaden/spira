import spira
from spira.core import param
from spira.lgm.coord import Coord


class TestCoord(spira.Cell):

    midpoint = param.CoordField(default=(1,4))


if __name__ == '__main__':

    c = Coord(1,0)
    print(c)

    c1 = TestCoord()
    print(c1.midpoint)
    
    c2 = TestCoord(midpoint=(2,0))
    print(c2.midpoint)





