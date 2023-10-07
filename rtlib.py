from math import pi, sin, cos, tan, radians, acos, atan2, asin
from mate import *
from lights import reflect, refract, totalInternalReflection as tir, fresnel
from materials import *

MAX_RECURSION_DEPTH = 3

class RayTracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        
        self.scene = []
        self.lights = []
        
        self.camPos = [0,0,0]
        
        self.rtViewPort(0,0,self.width, self.height)
        self.rtProyection()
        
        self.rtColor = (1,1,1)
        self.rtClearColor(0,0,0)
        self.rtClear()

        self.envMap = None
        
    def rtClearColor(self, r,g,b):
        self.ClearColor = (r,g,b)
        
    def rtClear(self):
        self.screen.fill((
            self.ClearColor[0] * 255,
            self.ClearColor[1] * 255,
            self.ClearColor[2] * 255
        ))
    
    def rtViewPort(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpW = width
        self.vpH = height
        
    def rtProyection(self, fov = 60, n = 0.1):
        self.nearPlane = n
        
        aspectRatio = self.vpW / self.vpH
        self.topEdge = tan((fov * pi / 360)) * n
        self.rightEdge = self.topEdge * aspectRatio
        
        
    def rtPoint(self,x,y,clr=None):
        y = self.height - y
        if (0<=x<self.width) and (0<=y<self.height):
            if clr != None:
                clr = (
                    int(clr[0]*255),
                    int(clr[1]*255),
                    int(clr[2]*255)
                )
                
                self.screen.set_at((x,y),clr)
            else:
                self.screen.set_at((x,y),self.rtColor)
    
    def rtCastRay(self,orig,dir,sceneObj=None, recursion=0):
        if recursion >= MAX_RECURSION_DEPTH:
            return None
        
        depth = float('inf')
        hit = None

        for obj in self.scene:
            if sceneObj != obj:
                intercept = obj.ray_intersect(orig,dir)
                if intercept:
                    if intercept.distance < depth:
                        hit = intercept
                        depth = intercept.distance
        return hit
    
    def rtRayColor(self, intercept, rayDirection, recursion=0):
        if intercept is None:
            if self.envMap:
                x = (atan2(rayDirection[2], rayDirection[0]) / (2 * pi)+0.5)*self.envMap.get_width()
                y = acos(rayDirection[1]) / pi * self.envMap.get_height()
                envColor = self.envMap.get_at((int(x), int(y)))
                return [envColor[i]/255 for i in range(3)]
            
            else:
                color = self.clearColor
                return [envColor[i]/255 for i in range(3)]

        material = intercept.obj.material
        surfaceColor = material.diffuse
        if material.texture and intercept.texcoords:
            tx = int(intercept.texcoords[0] * material.texture.get_width() - 1)
            ty = int(intercept.texcoords[1] * material.texture.get_height() - 1)
            texColor = material.texture.get_at((tx, ty))
            texColor = [i / 255 for i in texColor]
            surfaceColor = [surfaceColor[i] * texColor[i] for i in range(3)]

        reflectColor = [0, 0, 0]
        refractColor = [0, 0, 0]
        ambientLightColor = [0, 0, 0]
        diffuseLightColor = [0, 0, 0]
        specularLightColor = [0, 0, 0]
        finalColor = [0, 0, 0]

        if material.matType == OPAQUE:
            for light in self.lights:
                if light.type == "AMBIENT":
                    color = light.getColor()
                    ambientLightColor = [ambientLightColor[i] + color[i] for i in range(3)]
                else:
                    shadowDirection = None
                    if light.type == "DIRECTIONAL":
                        shadowDirection = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDirection = restar_vectores(light.point, intercept.impact)
                        shadowDirection = normalizar(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.impact, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        diffColor = light.getDiffuseColor(intercept)
                        diffuseLightColor = [diffuseLightColor[i] + diffColor[i] for i in range(3)]

                        specColor = light.getSpecularColor(intercept, self.camPos)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]


        elif material.matType == REFLECTIVE:
            reflection = reflect(intercept.normal, multi_vector(rayDirection, -1))
            reflectIntercept = self.rtCastRay(intercept.impact, reflection, intercept.obj, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflection, recursion + 1)

            for light in self.lights:
                if light.type != "AMBIENT":
                    lightDir = None
                    if light.type == "DIRECTIONAL":
                        lightDir = [i * -1 for i in light.direction]
                    if light.type == "POINT":
                        lightDir = restar_vectores(light.point, intercept.impact)
                        lightDir = normalizar(lightDir)
                        
                    shadowIntersect = self.rtCastRay(intercept.impact, lightDir, intercept.obj)
                    if shadowIntersect is None:
                        specColor = light.getSpecularColor(intercept, self.camPos)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]

        elif material.matType == TRANSPARENT:
            outside = producto_punto(rayDirection, intercept.normal) < 0
            bias = multi_vector(intercept.normal, 0.001)

            reflection = reflect(intercept.normal, multi_vector(rayDirection, -1))
            reflectOrig = sumar_vectores(intercept.impact, bias) if outside else restar_vectores(intercept.impact, bias)
            reflectIntercept = self.rtCastRay(reflectOrig, reflection, None, recursion + 1)
            reflectColor = self.rtRayColor(reflectIntercept, reflection, recursion + 1)

            for light in self.lights:
                if light.type != "AMBIENT":
                    shadowDirection = None
                if light.type == "DIRECTIONAL":
                    shadowDirection = [i * -1 for i in light.direction]
                if light.type == "POINT":
                    lightDirection = restar_vectores(light.point, intercept.impact)
                    shadowDirection = normalizar(lightDirection)

                    shadowIntersect = self.rtCastRay(intercept.impact, shadowDirection, intercept.obj)

                    if shadowIntersect is None:
                        specColor = light.getSpecularColor(intercept, self.camPos)
                        specularLightColor = [specularLightColor[i] + specColor[i] for i in range(3)]

            if not tir(intercept.normal, rayDirection, 1.0, material.ior):
                refraction = refract(intercept.normal, rayDirection, 1.0, material.ior)
                refractOrig = restar_vectores(intercept.impact, bias) if outside else sumar_vectores(intercept.impact, bias)
                refractIntercept = self.rtCastRay(refractOrig, refraction, None, recursion + 1)
                refractColor = self.rtRayColor(refractIntercept, refraction, recursion + 1)

                kr, kt = fresnel(intercept.normal, rayDirection, 1.0, intercept.obj.material.ior)
                reflectColor = multi_vector(reflectColor, kr)
                refractColor = multi_vector(refractColor, kt)


        lightColor = [ambientLightColor[i] + diffuseLightColor[i] + specularLightColor[i] + reflectColor[i] + refractColor[i]
                            for i in range(3)]
        finalColor = [surfaceColor[i] * lightColor[i] for i in range(3)]
        finalColor = [min(1, i) for i in finalColor]

        return finalColor
    
    def rtRender(self):
        for x in range(self.vpX, self.vpX + self.vpW + 1):
            for y in range(self.vpY, self.vpY + self.vpH + 1):
                if 0 < x < self.width and 0 < y < self.height:
                    pX = 2 * ((x + 0.5 - self.vpX) / self.vpW) - 1
                    pY = 2 * ((y + 0.5 - self.vpY) / self.vpH) - 1

                    pX *= self.rightEdge
                    pY *= self.topEdge

                    direction = (pX, pY, -self.nearPlane)
                    direction = normalizar(direction)

                    

                    intercept = self.rtCastRay(self.camPos, direction)
                    rayColor = self.rtRayColor(intercept, direction)
                        

                    self.rtPoint(x, y, rayColor)
                    pygame.display.flip()