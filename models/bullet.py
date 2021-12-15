import time

import pygame
from settings import *


class PlayerBullet:
    def __init__(self, screen, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.exist_time = 0.4
        self.time1 = time.time()
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 9
        self.screen = screen
        self.fig = pygame.Rect(self.x, self.y, BULLET_SIZE, BULLET_SIZE)

    def bullet_frame(self):
        if self.mouse_x > self.x:
            self.x += self.speed
        elif self.mouse_x < self.x:
            self.x -= self.speed
        if self.mouse_y > self.y:
            self.y += self.speed
        elif self.mouse_y < self.y:
            self.y -= self.speed

    def shoot(self, screen):
        self.fig = pygame.Rect(self.x, self.y, 5, 5)
        pygame.draw.rect(screen, BLACK, self.fig, 0)
