import random
from settings import *

import pygame


class Wolf():
    def __init__(self):
        self.speed = WOLF_SPEED
        self.hunger_rate = 0
        self.x = self.random_x()
        self.y = self.random_y()
        self.new_x = self.random_x()
        self.new_y = self.random_y()
        self.vision_area_x = self.x - ((WOLF_VISION_AREA - WOLF_SIZE) / 2)
        self.vision_area_y = self.y - ((WOLF_VISION_AREA - WOLF_SIZE) / 2)

        self.alive = True
        self.agressive = False
        self.sense_radius = 150

        self.body = pygame.Rect(self.x, self.y, WOLF_SIZE, WOLF_SIZE)
        self.vision_area = pygame.Rect(self.vision_area_x, self.vision_area_y, WOLF_VISION_AREA, WOLF_VISION_AREA)

    def draw(self, screen):
        self.body = pygame.Rect(self.x, self.y, WOLF_SIZE, WOLF_SIZE)
        self.vision_area = pygame.Rect(self.vision_area_x, self.vision_area_y, WOLF_VISION_AREA, WOLF_VISION_AREA)
        pygame.draw.rect(screen, GRAY, self.body, 0)
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
            self.hunger_rate += 1
        if self.new_y > self.y:
            self.y += self.speed
            self.vision_area_y += self.speed
        elif self.new_y < self.y:
            self.y -= self.speed
            self.vision_area_y -= self.speed
        elif self.new_y == self.y:
            self.new_y = self.random_y()
