import pygame
from pygame.locals import *

from figuras import *
from lights import *
from rtlib import RayTracer
from materials import *

brick = Material(diffuse=(1,0.3,0.2), spec=8, ks=0.01, matType=OPAQUE)
grass = Material(diffuse=(0.2,0.8,0.2), spec=32, ks=0.1, matType=OPAQUE )
water = Material(diffuse=(0.2,0.2,0.8), spec=256, ks=0.5, matType=OPAQUE)
snow = Material(diffuse=(0.9,0.9,0.9), spec=64, ks=0.35, matType=OPAQUE)
coal = Material(diffuse=(0.2,0.2,0.2), spec=64, ks=0.35, matType=TRANSPARENT)
stone = Material(diffuse=(0.45,0.45,0.45), spec=6, ks=0.05, matType=TRANSPARENT)
diamond = Material(diffuse=(0.6, 0.6, 0.9), spec=128, ks=0.20, ior=2.417, matType=TRANSPARENT)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.2, matType=REFLECTIVE)
window = Material(diffuse=(0.4, 0.4, 0.4), spec=64, ks=0.2, matType=REFLECTIVE)
glass = Material(diffuse=(0.9, 0.9, 0.9), spec=64, ks=0.15, ior=1.5, matType=REFLECTIVE)
ruby = Material(diffuse=(0.9,0.2,0.2), spec=128, ks=0.2, ior=2.417, matType=TRANSPARENT)
sun = Material(diffuse=(1,1,0),spec=120,ks=0.3,ior=3,matType=REFLECTIVE)
pyramid = Material(texture=pygame.image.load("Textures/texture.jpg"))
rpyramid = Material(texture=pygame.image.load("Textures/texture.jpg"), matType=TRANSPARENT)


width = 550
height = 550

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = RayTracer(screen)

rayTracer.envMap = pygame.image.load("Textures/desierto.bmp")


rayTracer.scene.append(
    Sphere(pos=(-13.5,13.5,-25),rad=2.5,material=sun)
)

rayTracer.scene.append(
    Pyramid(position=(-3.5,-3,-9),width=1.5,height=1.5,depth=1.5,rotation=(0,45,0), material=pyramid)
)

rayTracer.scene.append(
    Pyramid(position=(-1.5,-3,-9),width=1.5,height=1.5,depth=1.5,rotation=(0,45,0), material=pyramid)
)

rayTracer.scene.append(
    Pyramid(position=(0.5,-3,-9),width=1.5,height=1.5,depth=1.5,rotation=(0,45,0), material=pyramid)
)
rayTracer.scene.append(
    Pyramid(position=(-5.5,-5.5,-19),width=5,height=5,depth=5,rotation=(0,45,0), material=pyramid)
)
rayTracer.scene.append(
    Pyramid(position=(-0.5,-5,-19),width=6,height=6,depth=6,rotation=(0,45,0), material=pyramid)
)
rayTracer.scene.append(
    Pyramid(position=(5.5,-5,-19),width=5,height=5,depth=5,rotation=(0,45,0), material=pyramid)
)

rayTracer.scene.append(
    Donut(position=(-1,3,-10.7),normal=(0,-1,-0),material=stone,major_radius=2, minor_radius=1.5)
)
rayTracer.scene.append(
    Donut(position=(-1,3.1,-10.7),normal=(0,-1,-0),material=stone,major_radius=2, minor_radius=1.5)
)
rayTracer.scene.append(
    Donut(position=(-1,3.2,-10.7),normal=(0,-1,-0),material=stone,major_radius=2, minor_radius=1.5)
)

rayTracer.scene.append(
    Sphere(pos=(-0.35,1.32,-3.65),rad=0.55,material=snow)
)



rayTracer.lights.append(
    AmbientLight(intensity=0.4)
)
rayTracer.lights.append(
    DirectionalLight(direction=(1,-1,1),intensity=3,color=(1,1,0.3))
)
rayTracer.lights.append(
    PointLight(point=(-13.5,13.5,-25), intensity=5,color=(1,1,0))
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