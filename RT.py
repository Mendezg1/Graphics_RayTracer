import pygame
from pygame.locals import *

from figuras import Sphere
from lights import *
from rtlib import RayTracer
from materials import *

brick = Material(diffuse=(1,0.3,0.2), spec=8, ks=0.01)
grass = Material(diffuse=(0.2,0.8,0.2), spec=32, ks=0.1)
water = Material(diffuse=(0.2,0.2,0.8), spec=256, ks=0.5)
snow = Material(diffuse=(0.8,0.8,0.8), spec=64, ks=0.35)
coal = Material(diffuse=(0.2,0.2,0.2), spec=64, ks=0.35)
stone = Material(diffuse=(0.45,0.45,0.45), spec=6, ks=0.05)

width = 400
height = 400

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = RayTracer(screen)

#Cabeza
rayTracer.scene.append(
    Sphere(pos=(0, 1.6, -4.5), rad=0.75, material=snow)
)
rayTracer.scene.append(
    Sphere(pos=(-0.3, 1.7, -3.815), rad=0.1, material=coal)
)

#Por la iluminación el color del ladrillo hecho en clase tuvo los tonos anaranjados que se buscaban.
rayTracer.scene.append(
    Sphere(pos=(0, 1.5, -3.835), rad=0.13, material=brick)
)
rayTracer.scene.append(
    Sphere(pos=(0.3, 1.7, -3.815), rad=0.1, material=coal)
)
rayTracer.scene.append(
    Sphere(pos=(0, 1.24, -3.92), rad=0.1, material=stone)
)
rayTracer.scene.append(
    Sphere(pos=(0.2, 1.3, -3.93), rad=0.1, material=stone)
)
rayTracer.scene.append(
    Sphere(pos=(-0.2, 1.3, -3.93), rad=0.1, material=stone)
)
rayTracer.scene.append(
    Sphere(pos=(0.3, 1.45, -3.92), rad=0.1, material=stone)
)
rayTracer.scene.append(
    Sphere(pos=(-0.3, 1.45, -3.92), rad=0.1, material=stone)
)


#Cuerpo de arriba
rayTracer.scene.append(
    Sphere(pos=(0, 0.4, -4.7), rad=1, material=snow)
)

rayTracer.scene.append(
    Sphere(pos=(0,0.45,-3.8), rad=0.2, material=coal)
)

rayTracer.scene.append(
    Sphere(pos=(0,-0.25,-3.8), rad=0.2, material=coal)
)

#Cuerpo de abajo
rayTracer.scene.append(
    Sphere(pos=(0, -1, -5), rad=1.25, material=snow)
)

rayTracer.scene.append(
    Sphere(pos=(0,-1,-3.8), rad=0.25, material=coal)
)





rayTracer.lights.append(
    DirectionalLight(direction=(0, 0, -1), intensity=1)
)


isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rayTracer.rtClear()
    rayTracer.rtRender()
    pygame.display.flip()

pygame.quit()