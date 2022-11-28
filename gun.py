import math
from random import choice
from random import randint as rnd
import pygame
from pygame import draw

FPS = 30
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

score = 0
pi = math.pi

class Ball:
    def __init__(self, screen: pygame.Surface):
        """
        Конструктор класса Ball.
        """
        self.screen = screen
        self.x = gun.x1
        self.y = gun.y1
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.max_lifetime = 60
        self.current_lifetime = 0

    def move(self):
        """
        Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx
            self.x = WIDTH - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r
        if self.y + self.r >= HEIGHT:
            self.vy = -self.vy * 0.5
            self.y = HEIGHT - self.r
        self.vy -= 3
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """
        Рисует мяч по его координатам.
        """
        draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Если да, то убирает объект и цель из соответсвующих массивов.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        global bullets, targets
        if (self in bullets) and (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            bullets.remove(self)
            targets.remove(obj)
            return True
        else:
            return False

    def lifetime(self):
        """
        Если время мяча на экране больше заданного, то он удаляется из массива.
        """
        global bullets
        self.current_lifetime += 1
        if self.current_lifetime > self.max_lifetime:
            bullets = bullets[1:]

class Gun:
    def __init__(self, screen):
        """
        Конструктор класса Gun.
        """
        self.screen = screen
        self.f2_power = 20
        self.f2_on = False
        self.an = pi
        self.color = GREY
        self.x1 = 40
        self.y1 = 570
        self.r = 30
        self.x2 = 70
        self.y2 = 550

    def move(self):
        """
        Движение пушки с помощью стрелочек вправо и влево.
        """
        global left_key_down, right_key_down
        if left_key_down and self.x1 >= self.r:
            self.x1 -= 10
        if right_key_down and self.x1 <= WIDTH - self.r:
            self.x1 += 10

    def fire_start(self):
        self.f2_on = True

    def fire_end(self, event):
        """
        Выстрел мячом при отпускании кнопки мыши
        """
        global bullets, bullet_count
        bullet_count += 1
        new_ball = Ball(self.screen)
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        bullets.append(new_ball)
        self.f2_on = False
        self.f2_power = 20

    def targetting(self, event):
        """
        Прицеливание. Зависит от положения мыши.
        """
        if event.pos[0] == self.x1:
            if event.pos[1] < self.y1:
                self.an = 3*pi/2
            else:
                self.an = pi/2
        elif event.pos[0] > self.x1:
            self.an = math.atan((event.pos[1] - self.y1) / (event.pos[0] - self.x1))
        else:
            self.an = pi + math.atan((event.pos[1]-self.y1) / (event.pos[0]-self.x1))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        draw.line(screen,
                  self.color,
                  (self.x1, self.y1),
                  (self.x1 + self.r * math.cos(self.an), self.y1 + self.r * math.sin(self.an)),
                  10)

    def power_up(self):
        """
        Изменяет длину и цвет пушки пока она заряжается
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.r += 1
            self.color = RED
        else:
            self.color = GREY
            self.r = 30


class Target:
    def __init__(self):
        """
        Конструктор класса Target
        """
        self.alive = True
        self.screen = pygame.Surface
        self.x = rnd(0, WIDTH)
        self.y = rnd(0, 300)
        self.r = rnd(20, 40)
        self.vx = rnd(3, 5) * choice([-1, 1])
        self.vy = rnd(3, 5) * choice([-1, 1])
        self.color = RED

    def move(self):
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx
            self.x = WIDTH - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r
        if self.y + self.r >= 400:
            self.vy = -self.vy
            self.y = 400 - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy
            self.y = self.r
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        draw.circle(screen, self.color, (self.x, self.y), self.r, 0)
        draw.circle(screen, BLACK, (self.x, self.y), self.r, 1)

    def hit(self, points=1):
        global score
        score += points

    def spawn_bomb(self):
        global bombs
        if not rnd(0,99):
            new_bomb = Bomb()
            new_bomb.x = self.x
            new_bomb.y = self.y
            bombs.append(new_bomb)



class Tank:
    def __init__(self):
        """
        Конструктор класса Tank.
        """
        self.alive = True
        self.screen = pygame.Surface
        self.r = 15
        self.x = gun.x1
        self.y = gun.y1

    def draw(self):
        """
        Рисует корпус и башню танка по его координатам.
        """
        draw.circle(screen, GREY, (self.x, self.y), self.r)
        draw.rect(screen, GREY, (self.x-30, self.y, 60, 30))

    def pos_update(self):
        self.x = gun.x1
        self.y = gun.y1


class Bomb:
    def __init__(self):
        """
        Конструктор класса Bomb.
        """
        self.r = 10
        self.vy = 4
        self.color = BLACK

    def move(self):
        """
        Бомба равномерно двигается вертикально вниз, пока не достигнет нижней границы, и удаляется из массива.
        """
        global bombs
        self.y += self.vy
        if len(bullets) > 0 and self.y >= HEIGHT:
            bombs.remove(self)

    def draw(self):
        draw.circle(screen, self.color, (self.x, self.y), self.r, 0)

    def hit_tank(self, obj):
        """
        Проверяет, столкнулась ли бомба с танком.
        """
        if abs(self.x - obj.x) < 25 and abs(self.y - obj.y) < 25:
            obj.alive = False


def new_target():
    global targets
    new_target = Target()
    targets.append(new_target)



def show_score():
    """ Отображает текущий счёт."""
    font = pygame.font.SysFont('comicsansms', 26)
    text = font.render('Score: ' + str(score) + '', True, (10, 10, 10))
    textpos = text.get_rect(centerx=50, y=30)
    screen.blit(text, textpos)


def show_results():
    """ Если бомба попала в танк, останавливает игру и выводит надпись о конце игры"""
    font = pygame.font.SysFont('comicsansms', 36)
    text = font.render('GAME OVER', True, (10, 10, 10))
    textpos = text.get_rect(centerx=WIDTH/2, y=HEIGHT/2 -50)
    screen.blit(text, textpos)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet_count = 0
targets = []
bullets = []
bombs = []
left_key_down = False
right_key_down = False
clock = pygame.time.Clock()
gun = Gun(screen)
tank = Tank()
for i in range(6):
    new_target()


finished = False

while not finished:
    if not tank.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        show_results()
        pygame.display.update()
    else:
        screen.fill(WHITE)
        gun.move()
        gun.draw()
        tank.pos_update()
        tank.draw()
        show_score()
        for target in targets:
            target.spawn_bomb()
            target.move()
            target.draw()
        for bomb in bombs:
            bomb.hit_tank(tank)
            bomb.move()
            bomb.draw()
        for bullet in bullets:
            bullet.lifetime()
            bullet.draw()
        pygame.display.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_key_down = True
                if event.key == pygame.K_RIGHT:
                    right_key_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key_down = False
                if event.key == pygame.K_RIGHT:
                    right_key_down = False
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)

        for bullet in bullets:
            bullet.move()
            for target in targets:
                if bullet.hittest(target) and target.alive:
                    target.alive = False
                    target.hit()
                    new_target()

        gun.power_up()

pygame.quit()