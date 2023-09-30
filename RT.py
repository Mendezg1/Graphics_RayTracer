import pygame
from pygame.locals import *

from figuras import Sphere
from lights import *
from rtlib import RayTracer
from materials import *

brick = Material(diffuse=(1,0.3,0.2), spec=8, ks=0.01, matType=OPAQUE)
grass = Material(diffuse=(0.2,0.8,0.2), spec=32, ks=0.1, matType=OPAQUE )
water = Material(diffuse=(0.2,0.2,0.8), spec=256, ks=0.5)
snow = Material(diffuse=(0.8,0.8,0.8), spec=64, ks=0.35)
coal = Material(diffuse=(0.2,0.2,0.2), spec=64, ks=0.35)
stone = Material(diffuse=(0.45,0.45,0.45), spec=6, ks=0.05)
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


rayTracer.scene.append(
    Sphere(pos=(-1, -0.5, -3), rad=0.5, material=ruby)
)
rayTracer.scene.append(
    Sphere(pos=(-1, 1, -3), rad=0.5, material=diamond)
)
rayTracer.scene.append(
    Sphere(pos=(0, 1, -3), rad=0.5, material=mirror)
)
rayTracer.scene.append(
    Sphere(pos=(0, -0.5, -3), rad=0.5, material=window)
)
rayTracer.scene.append(
    Sphere(pos=(1, 1, -3), rad=0.5, material=grass)
)
rayTracer.scene.append(
    Sphere(pos=(1, -0.5, -3), rad=0.5, material=brick)
)


rayTracer.lights.append(
    AmbientLight(intensity=0.5)
)
rayTracer.lights.append(
    DirectionalLight(direction=(-1, -1, -1), intensity=0.3)
)
rayTracer.lights.append(
    PointLight(point=(2.5, 0, -5), intensity=1)
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