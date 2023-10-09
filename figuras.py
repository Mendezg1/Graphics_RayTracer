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

class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = normal
        super().__init__(position, material)

    def ray_intersect(self, origin, direction):
        
        direction = normalizar(direction)
        den = producto_punto(direction, self.normal)
        if abs(den) <= 0.0001:
            return None
        
        num = producto_punto(restar_vectores(self.position, origin), self.normal)
        t = num / den

        if t < 0:
            return None

        P = sumar_vectores(origin, multi_vector(direction, t))
        
        return Intercept(distance=t,
                        impact=P,
                        normal=self.normal,
                        texcoords=None,
                        obj=self)

class Disk(Plane):
    def __init__(self, position, normal, material, rad):
        self.radius = rad
        super().__init__(position, normal, material)

    def ray_intersect(self, origin, direction):
        planeIntersect = super().ray_intersect(origin, direction)

        if not planeIntersect:
            return None
        
        contactD = restar_vectores(planeIntersect.impact, self.position)
        contactD = magnitud(contactD)

        if contactD > self.radius:
            return None
        return Intercept(distance=contactD,
                    impact=planeIntersect.impact,
                    normal=planeIntersect.normal,
                    texcoords=None,
                    obj=self)

class AABB(Shape):
    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)

        self.planes = []

        self.size = size

        leftPlane = Plane(sumar_vectores(position, (-size[0] / 2, 0, 0)), (-1, 0, 0), material)
        rightPlane = Plane(sumar_vectores(position, (size[0] / 2, 0, 0)), (1, 0, 0), material)

        topPlane = Plane(sumar_vectores(position, (0, size[1] / 2, 0)), (0, 1, 0), material)
        bottomPlane = Plane(sumar_vectores(position, (0, -size[1] / 2, 0)), (0, -1, 0), material)

        frontPlane = Plane(sumar_vectores(position, (0, 0, size[2]/ 2)), (0, 0, 1), material)
        backPlane = Plane(sumar_vectores(position, (0, 0, -size[2]/ 2)), (0, 0, -1), material)

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(topPlane)
        self.planes.append(bottomPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        self.boundsMin =[0,0,0]
        self.boundsMax =[0,0,0]

        bias = 0.0001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (self.size[i] / 2 + bias)
            self.boundsMax[i] = self.position[i] + self.size[i] / 2 + bias

    def ray_intersect(self, origin, direction):
        intersect = None
        t = float("inf")

        u=0
        v=0

        for plane in self.planes:

            planeIntersect = plane.ray_intersect(origin, direction)

            if planeIntersect is not None:

                planePoint = planeIntersect.impact

                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                if abs(plane.normal[0])>0:
                                    u= (planePoint[1]-self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v= (planePoint[2]-self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[1])>0:
                                    u= (planePoint[0]-self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[2]-self.boundsMin[2]) / (self.size[2] + 0.002)
                                elif abs(plane.normal[2])>0:
                                    u= (planePoint[0]-self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[1]-self.boundsMin[1]) / (self.size[1] + 0.002)


        if intersect is None:
            return None

        return Intercept(distance=t,
                            impact=intersect.impact,
                            normal=intersect.normal,
                            texcoords=(u,v),
                            obj=self)

             



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