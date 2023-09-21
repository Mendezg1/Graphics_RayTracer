from math import pi, sin, cos, tan, radians
from mate import *

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
    
    def rtCastRay(self,orig,dir,sceneObj=None):
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
    
    def rtRender(self):
        
        for x in range(self.vpX, self.vpX + self.vpW + 1):
            for y in range(self.vpY, self.vpY + self.vpH + 1):
                if 0 < x < self.width and 0 < y < self.height:
                    Px = ((x + 0.5 - self.vpX) / self.vpW) * 2 - 1
                    Py = ((y + 0.5 - self.vpY) / self.vpH) * 2 - 1
                    Px *= self.rightEdge
                    Py *= self.topEdge
                    
                    direction = (Px, Py, -self.nearPlane)
                    direction = normalizar(direction)
                    
                    intercept = self.rtCastRay(self.camPos, direction)
                    if intercept is not None:

                        surfaceColor = intercept.obj.material.diffuse

                        ambientColor = [0,0,0]
                        diffuseColor = [0,0,0]
                        specularColor = [0,0,0]

                        for light in self.lights:
                            if light.type == "Ambient":
                                color = light.getLightColor()
                                ambientColor = [ambientColor[i] + color[i] for i in range(3)]
                            else:
                                lightdir = None
                                shadowdir = None

                                if light.type == "Directional":
                                    shadowdir = [i*-1 for i in light.direction]

                                if light.type == "Point":
                                    lightdir = [light.point[i] - intercept.impact[i] for i in range(3)]
                                    shadowdir = normalizar(lightdir)
                                    
                                shadowIntersect = self.rtCastRay(intercept.impact, shadowdir, intercept.obj)
                                
                                if shadowIntersect is None:
                                    diffColor = light.getDiffuseColor(intercept)
                                    diffuseColor = [diffuseColor[i] + diffColor[i] for i in range(3)]

                                    specColor = light.getSpecularColor(intercept, self.camPos)
                                    specularColor = [specularColor[i] + specColor[i] for i in range(3)]

                        lightColor = [ambientColor[i] + diffuseColor[i] + specularColor[i] for i in range(3)]
                        finalColor = [min(1, lightColor[i]*surfaceColor[i]) for i in range(3)]

                                
                        self.rtPoint(x,y,finalColor)