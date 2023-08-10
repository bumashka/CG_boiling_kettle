import math
import random
import sys

import pygame as pg

# Initialize pygame
pg.init()

# Screen dimensions
WIDTH, HEIGHT = 1050, 535

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

BLUE = (0, 0, 255)
TRANSPARENT_BLUE = (64, 128, 255, 64)  # 50% transparency (128/255)

# Create the screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.image.load('potpot.png')
background = pg.transform.scale(background, (WIDTH, HEIGHT))
pg.display.set_caption("Boiling Kettle")


class Bubble:

    def __init__(self, small):
        self.angle = None
        self.speed, self.speed_x, self.speed_y = None, None, None
        self.x, self.y = None, None
        self.radius = None
        self.size = small
        self.shape_bubble()

    def shape_bubble(self):
        if self.size:
            self.x = 268 + random.randint(1, 450)
            self.y = 425 - random.randint(0, 380)
            self.radius = random.randint(1, 3)
            self.speed_y = -random.randint(2, 10)
            self.speed_x = 0.1 * math.sqrt(abs(self.speed_y))

        else:
            self.x = 268 + random.randint(5, 450)
            self.y = 425
            self.radius = random.randint(10, 20)
            self.speed_y = -random.randint(2, 10)
            self.speed_x = (random.randint(1, 10) / 10) * math.sqrt(abs(self.speed_y))
            self.angle = random.randint(40, 80) / 100

    def update(self, speed):
        if self.size:
            self.x += self.speed_x + speed
            self.y += self.speed_y + speed
            self.speed_x += 0.01  # Simulate gravity

            # If the circle goes above the screen, reset it
            if self.x > 725 or self.radius < 0.5 or self.y < 40:
                self.shape_bubble()
            else:
                self.radius -= self.radius * 0.05
        else:
            self.x += self.speed_x * speed
            self.y += self.speed_y * speed
            self.speed_x += 0.001  # Simulate gravity
            self.angle += 0.001
            self.x = self.x - self.radius * self.angle * math.cos(self.angle)
            self.y = self.y - self.radius * self.angle * math.sin(self.angle)

            if (self.x > 725 or self.x < 270) or self.radius < 1 or self.y < 40 or self.angle > 0.9:
                self.shape_bubble()
            else:
                self.radius -= self.radius * 0.06

    def draw(self):
        surface = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        pg.draw.circle(surface, TRANSPARENT_BLUE, (self.radius, self.radius), self.radius)
        pg.draw.circle(surface, (255, 255, 255, 192), (self.radius / 2, self.radius / 2), self.radius / 2)
        screen.blit(surface, (self.x - self.radius, self.y - self.radius))


big_bubbles_speed = 0.1
small_bubbles_speed = 0

bubbles = []
small_bubbles = []

for bubble in range(0, 100):
    bubbles.append(Bubble(False))

for bubble in range(0, 500):
    small_bubbles.append(Bubble(True))

running = True
clock = pg.time.Clock()

while running:

    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    big_bubbles_speed += 0.001
    small_bubbles_speed += 0.0005

    for bubble in bubbles:
        bubble.update(big_bubbles_speed)
        bubble.draw()

    for bubble in small_bubbles:
        bubble.update(small_bubbles_speed)
        bubble.draw()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    pg.display.flip()
    clock.tick(1000)

pg.quit()
sys.exit()
