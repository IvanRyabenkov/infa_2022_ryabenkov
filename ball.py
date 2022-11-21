import numpy as np
import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 20
x_pixels = 1200
y_pixels = 600
screen = pygame.display.set_mode((x_pixels, y_pixels))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
points = 0
x_circle = []
y_circle = []
r_circle = []
c_circle = []
t_circle = []
v_x = []
v_y = []
font = pygame.font.SysFont('comicsansms', 32)
follow = font.render('Score: 0', 1, WHITE, BLACK)

def new_balls(): #генерация шариков
    n = randint(0, 1)
    for i in range(n):
        x = randint(50, x_pixels-50)
        x_circle.append(x)
        y = randint(50, y_pixels-50)
        y_circle.append(y)
        r = randint(10, 50)
        r_circle.append(r)
        color = COLORS[randint(0, 5)]
        c_circle.append(color)
        t = randint(0, 90)
        t_circle.append(t)
        vx = randint(-5, 5)
        v_x.append(vx)
        vy = randint(-5, 5)
        v_y.append(vy)

def draw(): # функция рисует шарики
    for i in range(len(r_circle)):
        if t_circle[i] <= 100:
            circle(screen, c_circle[i], (x_circle[i], y_circle[i]), r_circle[i])

def motion(): # движение шариков
    for i in range(len(x_circle)):
        x_circle[i] += v_x[i]
        y_circle[i] += v_y[i]

def lifetime(): # увеличение времени нахождения шарика на экране
    for i in range(len(t_circle)):
        t_circle[i] += 1

def collision(): # столкновение шариков с границами экрана
    for i in range(len(x_circle)):
        if x_circle[i] - r_circle[i] <= 0:
            v_x[i] = -v_x[i]
        if x_circle[i] >= x_pixels - r_circle[i] and v_x[i] >= 0:
            v_x[i] = -v_x[i]
        if y_circle[i] - r_circle[i] <= 0:
            v_y[i] = -v_y[i]
        if y_circle[i] >= y_pixels - r_circle[i] and v_y[i] >= 0:
            v_y[i] = -v_y[i]

def distanсe(x1, y1, x2, y2): # определяет расстояние между двумя точками
    dist = np.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist

def is_in_circle(x, y, x0, y0, r): # определяет, попадает ли точка в круг
    if distanсe(x, y, x0, y0) <= r:
        return True
    else:
        return False

def delete(i):
    t_circle[i] = 101

def points_counter(i, points): # подсчет очков за попадание по шарику
    points += 1000 // r_circle[i]
    return points

def click(event, x_circle, y_circle, r_circle, points): #функция определяет, попадает ли мышка по шарику с координатами x_circle[i], y_circle[i]
                                                        # и радиусом r_circle[i], и определяет кол-во очков за попадание
    x, y = event.pos[0], event.pos[1]
    for i in range(len(r_circle)):
        if is_in_circle(x, y, x_circle[i], y_circle[i], r_circle[i]):
            points = points_counter(i, points)
            delete(i)
    return points

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            points = click(event, x_circle, y_circle, r_circle, points)
            follow = font.render(str('Score:') + str(points) , 1, WHITE, BLACK)
    motion()
    collision()
    screen.blit(follow, (10, 10))
    new_balls()
    draw()
    lifetime()
    pygame.display.update()
    screen.fill(BLACK)


print(points)

pygame.quit()