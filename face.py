import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
pygame.Surface.fill(screen, (255, 255, 255))

circle(screen, (255, 255, 0), (200, 200), 150)
circle(screen, (0, 0, 0), (200, 200), 150, 1)
rect(screen, (0, 0, 0), (110, 250, 170, 30))

circle(screen, (255, 0, 0), (265, 150), 27)
circle(screen, (0, 0, 0), (265, 150), 27, 1)
circle(screen, (0, 0, 0), (265, 150), 15)
line(screen, (0, 0, 0), [228, 143 ], [330 ,60], 11)

circle(screen, (255, 0, 0), (145, 150), 32)
circle(screen, (0, 0, 0), (145, 150), 32, 1)
circle(screen, (0, 0, 0), (145, 150), 20)
line(screen, (0, 0, 0), [190 , 138], [85, 60], 13)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()