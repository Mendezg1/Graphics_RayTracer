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


"""
    Pregunta a ChatGPT: Tengo la clase Disk y Plane. Plane dibuja un plano infinito utilizando lógica de RayTracer y Pygame.
    Disk genera un disco delimitado por un radio que utiliza la clase Plane. Con ellas, ¿cómo puedo generar una clase 
    que genere una figura similar a una dona?
"""
class Donut(Shape):
    def __init__(self, position, material, major_radius, minor_radius, normal):
        super().__init__(position, material)
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.normal = normalizar(normal)

    def ray_intersect(self, origin, direction):
        # Calcula la intersección con el plano central de la dona
        central_plane = Plane(self.position, self.normal, self.material)
        central_intercept = central_plane.ray_intersect(origin, direction)

        if central_intercept is None:
            return None

        # Calcula la distancia al centro del toro
        center_to_impact = restar_vectores(central_intercept.impact, self.position)
        distance_to_center = magnitud(center_to_impact)

        point = central_intercept.impact

        # Comprueba si el punto de intersección está dentro del toro
        if (distance_to_center >= self.minor_radius and
                distance_to_center <= self.major_radius + self.minor_radius):
            u = (1 + math.atan2(point[1], point[0]) / (2 * math.pi)) % 1
            v = (magnitud(center_to_impact) - self.minor_radius) / (self.major_radius - self.minor_radius)

            return Intercept(distance=distance_to_center,
                            impact=central_intercept.impact,
                            normal=central_intercept.normal,
                            texcoords=(u,v),
                            obj=self)


        else:
            return None
             



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
    """
        Conversación con ChatGPT: ¿Con la clase Plano, como puedo crear una clase Triángulo y, después, una Pirámide?
    """
class Triangle(Shape):
        def __init__(self, vertices, material):
            super().__init__(pos=vertices[0], material=material)
            self.vertices = vertices

        def ray_intersect(self, origin, direction):
            v0, v1, v2 = self.vertices

            edge1 = restar_vectores(v1, v0)
            edge2 = restar_vectores(v2, v0)
            normal = normalizar(producto_cruz(edge1, edge2))

            d = producto_punto(normal, v0)

            den= producto_punto(normal, direction)
            if abs(den) < 0.0001:
                return None

            t = (d - producto_punto(normal, origin)) / den
            if t < 0:
                return None

            point = sumar_vectores(origin, multi_vector(direction,t))

            edge0 = restar_vectores(v0, v2)
            edge2 = restar_vectores(v2, v1)

            if producto_punto(normal, producto_cruz(edge0, restar_vectores(point, v2))) < 0:
                return None
            
            if producto_punto(normal, producto_cruz(edge1, restar_vectores(point, v0))) < 0:
                return None
            
            if producto_punto(normal, producto_cruz(edge2, restar_vectores(point, v1))) < 0:
                return None


            c0 = producto_punto(edge0, restar_vectores(point, v2))
            c1 = producto_punto(edge1, restar_vectores(point, v0))
            c2 = producto_punto(edge2, restar_vectores(point, v1))
            total = c0 + c1 + c2
            u = c1 / total
            v = c2 / total

            u *= 1.8
            v *= 1.3

            return Intercept(distance=t,
                            impact=point,
                            normal=normal,
                            texcoords=(u, 1-v),
                            obj=self)


class Pyramid(Shape):
    def __init__(self, position, width, height, depth, rotation, material):
        super().__init__(pos=position, material=material)
        self.W = width
        self.H = height
        self.depth = depth
        self.rot = rotation

    def ray_intersect(self, origin, direction):
        v0 = (-self.W / 2, 0, -self.depth / 2)
        v1 = (-self.W / 2, 0, self.depth / 2)
        v2 = (self.W / 2, 0, self.depth / 2)
        v3 = (self.W / 2, 0, -self.depth / 2)

        apex = (0, self.H, 0)

        v0 = rotacion_vector(v0, self.rot)
        v1 = rotacion_vector(v1, self.rot)
        v2 = rotacion_vector(v2, self.rot)
        v3 = rotacion_vector(v3, self.rot)
        apex = rotacion_vector(apex, self.rot)

        v0 = sumar_vectores(v0, self.position)
        v1 = sumar_vectores(v1, self.position)
        v2 = sumar_vectores(v2, self.position)
        v3 = sumar_vectores(v3, self.position)
        apex = sumar_vectores(apex, self.position)

        triangles = []
        triangles.append(Triangle((v0, v1, v2), self.material))
        triangles.append(Triangle((v0, v2, v3), self.material))
        triangles.append(Triangle((v0, v1, apex), self.material))
        triangles.append(Triangle((v1, v2, apex), self.material))
        triangles.append(Triangle((v2, v3, apex), self.material))
        triangles.append(Triangle((v3, v0, apex), self.material))

        nearIntercept = None
        for triangle in triangles:
            intercept = triangle.ray_intersect(origin, direction)
            if intercept is not None:
                if nearIntercept is None or intercept.distance < nearIntercept.distance:
                    nearIntercept = intercept

        if nearIntercept:
            return Intercept(distance=nearIntercept.distance,
                            impact=nearIntercept.impact,
                            normal=nearIntercept.normal,
                            texcoords=nearIntercept.texcoords,
                            obj=self)
        return None