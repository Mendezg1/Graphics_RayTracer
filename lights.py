from mate import *
from math import acos, asin

def reflectVector(normal, direction):
    reflect = 2 * producto_punto(normal, direction)
    reflect = multi_vector(normal, reflect)
    reflect = restar_vectores(reflect, direction)
    reflect = normalizar(reflect)

    return reflect

class Light(object):
    def __init__(self, intensity = 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.type = lightType

    def getLightColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]
    
    def getDiffuseColor(self, intercept):
        return self.getLightColor()
    
    def getSpecularColor(self, intercept, viewPos):
        return None
    
    def getColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]

class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,1,1)):
        super().__init__(intensity, color, "AMBIENT")

def reflect(normal, direction):
        temp = 2 * producto_punto(normal,direction)
        reflectValue = multi_vector(normal,temp)
        reflectValue = restar_vectores(reflectValue, direction)
        return normalizar(reflectValue)

def refract(normal,incident,n1,n2):
        c1 = producto_punto(normal, incident)
        if c1 < 0:
            c1 = -c1
        else:
            normal = [i*-1 for i in normal]
            n1,n2 = n2,n1
        
        n = n1/n2
        T = restar_vectores(multi_vector(sumar_vectores(incident, multi_vector(normal, c1 )), n ) , multi_vector(normal, (1 - n **2 * (1-c1**2)) ** 0.5 ))
        return normalizar(T)

def fresnel(normal, incident,n1, n2):
        c1 = producto_punto(normal, incident)

        if c1 < 0:
            c1 = -c1
        else:
            n1, n2 = n2, n1

        s2 = (n1 * (1 - c1 ** 2) ** 0.5) / n2
        c2 = (1 - s2 ** 2) ** 0.5

        f1 = ((n2 * c1 - n1 * c2) / (n2 * c1 + n1 * c2)) ** 2
        f2 = ((n1 * c2 - n2 * c1) / (n1 * c2 + n2 * c1)) ** 2

        kr = (f1 + f2) / 2
        kt = 1 - kr
        return kr, kt
    

def totalInternalReflection(incident, normal , n1, n2):
        c1 = producto_punto(normal, incident)
        if c1 < 0:
            c1 = -c1
        else:
            normal = multi_vector(normal, -1)
            n1, n2 = n2, n1
        
        if n1 < n2:
            return False
        
        theta1 = acos(c1)
        thetaC = asin(n2/n1)

        return theta1 >= thetaC

class DirectionalLight(Light):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = normalizar(direction)
        super().__init__(intensity, color, "DIRECTIONAL")
    
    def getDiffuseColor(self, intercept):
        dir = [i * -1 for i in self.direction]

        intensity = producto_punto(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return [i * intensity for i in self.color]
    
    def getSpecularColor(self, intercept, viewPos):
        
        dir = [(i * -1) for i in self.direction]

        reflect = reflectVector(intercept.normal, dir)

        viewDir = normalizar([viewPos[i] - intercept.impact[i] for i in range(3)])

        specIntensity = max(0, min(1, producto_punto(viewDir, reflect))) ** intercept.obj.material.spec
        specIntensity *= self.intensity
        specIntensity *= intercept.obj.material.ks
        

        specColor = [(i * specIntensity) for i in self.color]

        return specColor
    
class PointLight(Light):
    def __init__(self, point=(0,0,0), intensity=1, color=(1,1,1)):
        self.point = point
        super().__init__(intensity, color, "POINT")

    def getDiffuseColor(self,intercept):
        dir = [self.point[i] - intercept.impact[i] for i in range(3)]
        dir = normalizar(dir)
        intensity = producto_punto(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return [i * intensity for i in self.color]
    
    def getSpecularColor(self, intercept, viewPos):
        dir = [self.point[i] - intercept.impact[i] for i in range(3)]
        dir = normalizar(dir)
        rad = magnitud(dir)
        reflect = reflectVector(intercept.normal, dir)

        viewDir = normalizar([viewPos[i] - intercept.normal[i] for i in range(3)])

        specIntensity = max(0, min(1, producto_punto(viewDir, reflect))) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        if rad != 0:
            specIntensity /= rad ** 2
        specIntensity = max(0, min(1, specIntensity))

        specColor = [(i * specIntensity) for i in self.color]

        return specColor


    
    
    

