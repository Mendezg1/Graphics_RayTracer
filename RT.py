import pygame
from pygame.locals import *

from figuras import *
from lights import *
from rtlib import RayTracer
from materials import *

brick = Material(diffuse=(1,0.3,0.2), spec=8, ks=0.01, matType=OPAQUE)
grass = Material(diffuse=(0.2,0.8,0.2), spec=32, ks=0.1, matType=OPAQUE )
water = Material(diffuse=(0.2,0.2,0.8), spec=256, ks=0.5, matType=OPAQUE)
snow = Material(diffuse=(0.8,0.8,0.8), spec=64, ks=0.35, matType=OPAQUE)
coal = Material(diffuse=(0.2,0.2,0.2), spec=64, ks=0.35, matType=OPAQUE)
stone = Material(diffuse=(0.45,0.45,0.45), spec=6, ks=0.05, matType=OPAQUE)
diamond = Material(diffuse=(0.6, 0.6, 0.9), spec=128, ks=0.20, ior=2.417, matType=TRANSPARENT)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.2, matType=REFLECTIVE)
window = Material(diffuse=(0.4, 0.4, 0.4), spec=64, ks=0.2, matType=REFLECTIVE)
glass = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.15, ior=1.5, matType=TRANSPARENT)
ruby = Material(diffuse=(0.9,0.2,0.2), spec=128, ks=0.2, ior=2.417, matType=TRANSPARENT)


width = 400
height = 400

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = RayTracer(screen)

rayTracer.envMap = pygame.image.load("Textures/cielo.bmp")

rayTracer.scene.append(Plane((0,0,-8),(0,0,-1),snow))
rayTracer.scene.append(Disk((0,0,-7.85),(0,0,-1),mirror,2.1))
rayTracer.scene.append(Plane((0,-2.5,0),(0,1,0),grass))
rayTracer.scene.append(Plane((0,2.5,0),(0,-1,0),stone))
rayTracer.scene.append(Plane((2.2,0,0),(-1,0,0),brick))
rayTracer.scene.append(Plane((-2.2,0,0),(1,0,0),water))



rayTracer.scene.append(AABB((-0.5,-1,-2),(0.65,0.65,0.65),diamond))
rayTracer.scene.append(AABB((0.5,-1,-2),(0.65,0.65,0.65),ruby))

rayTracer.lights.append(
    AmbientLight(intensity=0.6)
)
rayTracer.lights.append(
    PointLight(point=(2.2, 2.5, -5), intensity=1)
)
rayTracer.lights.append(
    PointLight(point=(-2.2, 2.5, -5), intensity=1)
)


isRunning = True

rayTracer.rtClear()
rayTracer.rtRender()

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
    pygame.display.flip()

rect = pygame.Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "output.png")

pygame.quit()