from mate import *

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

class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,1,1)):
        super().__init__(intensity, color, "Ambient")

class DirectionalLight(Light):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = normalizar(direction)
        super().__init__(intensity, color, "Directional")
    
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
        super().__init__(intensity, color, "Point")

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


    
    
    

