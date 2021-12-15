import random
from settings import *

import pygame


class Rabbit():
    def __init__(self):
        self.speed = RABBIT_SPEED
        self.x = self.random_x()
        self.y = self.random_y()
        self.new_x = self.random_x()
        self.new_y = self.random_y()
        self.panic_mode = False
        self.vision_area_x = self.x - ((RABBIT_VISION_AREA - RABBIT_SIZE) / 2)
        self.vision_area_y = self.y - ((RABBIT_VISION_AREA - RABBIT_SIZE) / 2)

        self.alive = True
        self.body = pygame.Rect(self.x, self.y, RABBIT_SIZE, RABBIT_SIZE)
        self.vision_area = pygame.Rect(self.vision_area_x, self.vision_area_y, RABBIT_VISION_AREA, RABBIT_VISION_AREA)

    def draw(self, screen):
        self.body = pygame.Rect(self.x, self.y, RABBIT_SIZE, RABBIT_SIZE)
        self.vision_area = pygame.Rect(self.vision_area_x, self.vision_area_y, RABBIT_VISION_AREA, RABBIT_VISION_AREA)
        pygame.draw.rect(screen, WHITE, self.body, 0)
        pygame.draw.rect(screen, BLACK, self.vision_area, 1)

    def aliquot_spd(self, val):
        if val % self.speed == 0:
            return val
        else:
            while True:
                val += 1
                if val % self.speed == 0:
                    return val

    def random_x(self):
        rand = random.randint((WIDTH / 60) + 5, WIDTH - ((WIDTH / 60) - 5))
        return self.aliquot_spd(rand)

    def random_y(self):
        rand = random.randint((WIDTH / 60) + 3, HEIGHT - ((WIDTH / 60) - 3))
        return self.aliquot_spd(rand)

    def move(self):
        if self.new_x > self.x:
            self.x += self.speed
            self.vision_area_x += self.speed
        elif self.new_x < self.x:
            self.x -= self.speed
            self.vision_area_x -= self.speed
        elif self.new_x == self.x:
            self.new_x = self.random_x()
            self.panic_mode = False
        if self.new_y > self.y:
            self.y += self.speed
            self.vision_area_y += self.speed
        elif self.new_y < self.y:
            self.y -= self.speed
            self.vision_area_y -= self.speed
        elif self.new_y == self.y:
            self.new_y = self.random_y()
            self.panic_mode = False
