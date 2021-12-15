from settings import *
import pygame


class Player:
    def __init__(self, screen):
        self.alive = True
        self.x, self.y = player_pos
        self.angle = player_angle
        self.body = pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)
        self.player_bullets = []
        self.screen = screen
        self.bullets_num = BULLETS_NUM
        self.iter = 0

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= player_speed
        if keys[pygame.K_s]:
            self.y += player_speed
        if keys[pygame.K_a]:
            self.x -= player_speed
        if keys[pygame.K_d]:
            self.x += player_speed
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        if keys[pygame.K_r]:
            self.bullets_num = BULLETS_NUM

    def draw_player(self, screen):
        self.body = pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)
        pygame.draw.rect(screen, BLUE, self.body, 0)
        self.traectory = pygame.draw.line(screen, DARK_RED, [self.x + (PLAYER_SIZE / 2), self.y + (PLAYER_SIZE / 2)],
                                          pygame.mouse.get_pos())
