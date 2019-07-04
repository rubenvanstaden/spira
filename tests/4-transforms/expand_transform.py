import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class Jj(spira.Cell):

    def create_elementals(self, elems):

        shape_hexagon = shapes.ConvexShape(radius=7)
        ply = spira.Polygon(alias='J5', shape=shape_hexagon, gds_layer=spira.Layer(number=11))
        ply.center = (0,0)
        elems += ply

        return elems


class ResVia(spira.Cell):

    def create_elementals(self, elems):

        shape_rectangle = shapes.RectangleShape(p1=(-7.5, -13.2), p2=(7.5, -8.2))
        ply = spira.Polygon(shape=shape_rectangle, gds_layer=spira.Layer(number=11))
        ply.center = (0,0)
        elems += ply

        shape_rectangle = shapes.RectangleShape(p1=(-4, -12), p2=(4.1, -10))
        ply = spira.Polygon(shape=shape_rectangle, gds_layer=spira.Layer(number=10))
        ply.center = (0,0)
        elems += ply

        return elems


class Top(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((0, -8))
        return [t1, t2]

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        s_jj = spira.SRef(Jj(), transformation=t1)
        s_res = spira.SRef(ResVia(), transformation=t2)

        shape_rectangle = shapes.RectangleShape(p1=(-10, -23), p2=(10, 10))
        ply = spira.Polygon(shape=shape_rectangle, gds_layer=spira.Layer(number=7))
        elems += ply

        elems += s_jj
        elems += s_res

        return elems


class Bot(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((0, -30))
        return [t1, t2]

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        s_res = spira.SRef(ResVia(), transformation=t2)

        shape_rectangle = shapes.RectangleShape(p1=(-10, -55), p2=(10, -35))
        ply = spira.Polygon(shape=shape_rectangle, gds_layer=spira.Layer(number=7))
        elems += ply

        elems += s_res

        return elems


class Junction(spira.Cell):
    """ Hypres Josephson junction. """

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((0, -5))
        return [t1, t2]

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        shape_rectangle = shapes.RectangleShape(p1=(-13, -60), p2=(13, 12))
        ply = spira.Polygon(alias='M4', shape=shape_rectangle, gds_layer=spira.Layer(number=5))
        elems += ply

        s_top = spira.SRef(alias='S1', reference=Top(), transformation=t1)
        s_bot = spira.SRef(alias='S2', reference=Bot(), transformation=t2)

        elems += s_top
        elems += s_bot

        return elems



if __name__ == '__main__':
    
    
    junction = Junction()
    
    # junction = junction.expand_transform()

    C = spira.Cell(name='TestingCell')

    S = spira.SRef(junction)
    T = spira.Stretch(stretch_factor=(2,1))
    S = T(S)
    C += S
    C.output()

    # print('\n--- Original SRef ---')
    # for s in junction.elementals:
    #     if isinstance(s, spira.SRef):
    #         print(s)
    #         print(s.ref)
    #         s = s.expand_transform()
    
    # print('\n--- Expanded SRef ---')
    # for s in junction.elementals:
    #     if isinstance(s, spira.SRef):
    #         print(s)
    #         print(s.ref)
    #         for e1 in s.ref.elementals:
    #             if isinstance(e1, spira.SRef):
    #                 print(type(e1.transformation))
    #                 print(e1.transformation)
    #                 e1 = e1.expand_transform()
    
    # print('\n--- Expanded SRef Level 2 ---')
    # for s in junction.elementals:
    #     if isinstance(s, spira.SRef):
    #         for e1 in s.ref.elementals:
    #             if isinstance(e1, spira.SRef):
    #                 print(type(e1.transformation))
    #                 print(e1.transformation)
    
    # print('\n--- Elementals ---')
    # for e1 in junction.elementals:
    #     print(e1)
    
    
    print('\n=========================================================================================\n')
    
    
    # c1 = spira.Cell(name='ExpandedCell')
    
    # def flat_polygons(subj, cell):
    #     for e1 in cell.elementals:
    #         if isinstance(e1, spira.Polygon):
    #             subj += e1
    #         elif isinstance(e1, spira.SRef):
    #             flat_polygons(subj=subj, cell=e1.ref)
    #     return subj
    
    # cell = flat_polygons(c1, junction)
    
    
    # c2 = spira.Cell(name='Stretch')
    
    # p1 = junction.top.ref.elementals[1].ref.elementals[0]
    # p2 = junction.bot.ref.elementals[1]
    
    # p1.stretch(sx=1, sy=2)
    
    # c2 += p1
    # c2 += p2
    
    # ply = junction['Jj_S0']['J5']
    
    # ply.stretch(sx=1, sy=2, center=(0, 6))
    
    # junction.output()
    # cell.output()
    # c2.output()


