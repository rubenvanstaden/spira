import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from expand_transform import Junction


class Jtl(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation(Coord(0*1e6, 0*1e6))
        t2 = spira.Translation(Coord(150*1e6, 0*1e6))
        return [t1, t2]

    def get_routes(self):
        shape_rectangle = shapes.RectangleShape(p1=(-13*1e6, -60*1e6), p2=(13*1e6, 12*1e6))
        ply = spira.Polygon(alias='M4', shape=shape_rectangle, gds_layer=spira.Layer(number=5))
        return ply

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        s_top = spira.SRef(alias='S1', reference=jj, transformation=t1)
        s_bot = spira.SRef(alias='S2', reference=jj, transformation=t2)

        elems += s_top
        elems += s_bot

        return elems


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    
    jtl= Jtl()
    
    jtl.expand_transform()

    # print('\n--- Original SRef ---')
    # for s in c.elementals:
    #     if isinstance(s, spira.SRef):
    #         print(s)
    #         print(s.ref)
    #         s = s.expand_transform()
    
    # print('\n--- Expanded SRef ---')
    # for s in c.elementals:
    #     if isinstance(s, spira.SRef):
    #         print(s)
    #         print(s.ref)
    #         for e1 in s.ref.elementals:
    #             if isinstance(e1, spira.SRef):
    #                 print(type(e1.transformation))
    #                 print(e1.transformation)
    #                 e1 = e1.expand_transform()

    for k, v in jtl['Junction_S1'].alias_cells.items():
        print(k, v)

    ply = jtl['Junction_S1']['Jj_S0']['J5']
    
    ply.stretch(sx=1, sy=2)
    
    jtl.output()


