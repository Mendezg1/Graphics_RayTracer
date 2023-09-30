from mate import *
from math import pi, acos, atan2
class Shape(object):
    def __init__(self, pos, material):
        self.position = pos
        self.material = material
        
    def ray_intersect(self, origin, direction):
        return None

class Intercept(object):
    def __init__(self, distance, impact, normal, obj, texcoords):
        self.distance = distance
        self.impact = impact
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj



class Sphere(Shape):
    def __init__(self, pos, rad, material):
        self.radius = rad
        super().__init__(pos,material)

    def ray_intersect(self, origin, direction):
        L = [self.position[i] - origin[i] for i in range(3)]
        magnL = magnitud(L)
        if not direction or not L:
            print(str(L) + " " + str(direction))
        tca = producto_punto(L, direction)
        d = (abs(pow(magnL,2) - pow(tca,2))) ** 0.5
        if d>self.radius:
            return None
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5
            
        t0 = tca - thc
        t1 = tca + thc
            
        if t0 < 0:
            t0 = t1
        if t0 < 0:
                return None
            
        P = [origin[i] + (direction[i] * t0) for i in range(3)]
        normal = restar_vectores(P, self.position)
        normal = normalizar(normal)

        u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
        v = acos(normal[1]) / pi
            
        return Intercept(distance=t0,
                        impact=P,
                        normal=normal,
                        texcoords=(u, v),
                        obj=self)