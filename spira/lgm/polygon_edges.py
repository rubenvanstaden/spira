import spira
import numpy as np
from spira import param, shapes


class PolygonEdges(spira.Cell):

    polygon = param.DataField(fdef_name='create_polygon')

    def create_polygon(self):
        shape = shapes.ConvexPolygon()
        # shape = shapes.RectangleShape()
        # pts = 
        # shape = shapes.Shape(points=pts)
        p = spira.Polygons(shape=shape)
        return p

    def create_elementals(self, elems):

        elems += self.polygon

        return elems

    def create_ports(self, ports):

        points = self.polygon.shape.points

        xpts = list(points[0][:, 0])
        ypts = list(points[0][:, 1])

        n = len(xpts)
        xpts.append(xpts[0])
        ypts.append(ypts[0]) 

        cc = 0
        for i in range(0, n):
            cc += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))
                
        for i in range(0, n):
            midpoint_n = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
            orientation_n = np.arctan2(np.sign(cc) * (xpts[i+1]-xpts[i]), np.sign(cc) * (ypts[i]-ypts[i+1])) * 180/np.pi
            width_n = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))    

            print(width_n)

            ports += spira.Term(
                name=str(i+1),
                midpoint=midpoint_n,
                width=width_n,
                orientation=orientation_n
            )

        return ports



# def polygon_ports(xpts=[-1,-1, 0, 0],
#             ypts = [0, 1, 1, 0],
#             layer = 0):
#     # returns a polygon with ports on all edges
#     P = Device('polygon')
#     P.add_polygon([xpts, ypts], layer = layer)
#     n = len(xpts)
#     xpts.append(xpts[0])
#     ypts.append(ypts[0]) 
#     #determine if clockwise or counterclockwise
#     cc = 0     
#     for i in range(0,n):
#         cc += ((xpts[i+1]-xpts[i])*(ypts[i+1]+ypts[i]))
            
#     for i in range(0,n):
#         midpoint_n = [(xpts[i+1]+xpts[i])/2, (ypts[i+1]+ypts[i])/2]
#         orientation_n = np.arctan2(np.sign(cc)*(xpts[i+1]-xpts[i]),np.sign(cc)*(ypts[i]-ypts[i+1]))*180/np.pi           
#         width_n = np.abs(np.sqrt((xpts[i+1]-xpts[i])**2+(ypts[i+1]-ypts[i])**2))    
#         P.add_port(name = str(i+1), midpoint = midpoint_n, width = width_n, orientation = orientation_n)
    
#     return P


if __name__ == '__main__':

    pe = PolygonEdges()
    pe.output()

