import time
import pygame

from settings import *
from models.player import Player
from views.menu_interface import menu_interface
from models.bullet import PlayerBullet
from models.wolf import Wolf
from models.deer import Deer
from models.rabbit import Rabbit


def draw_borders(s, x, y, w, h, bw, c):
    w1 = pygame.Rect(x, y, w, bw)
    w2 = pygame.Rect(x, y + h - bw, w, bw)
    w3 = pygame.Rect(x, y, bw, h)
    w4 = pygame.Rect(x + w - bw, y, bw, h)

    pygame.draw.rect(s, c, w1)
    pygame.draw.rect(s, c, w2)
    pygame.draw.rect(s, c, w3)
    pygame.draw.rect(s, c, w4)

    return [w1, w2, w3, w4]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("wild-hunt")
clock = pygame.time.Clock()

player = Player(screen)
wolfs = [Wolf() for w in range(WOLF_NUMBER)]
deers = [Deer() for d in range(DEER_NUMBER)]
rabbits = [Rabbit() for d in range(RABBIT_NUMBER)]

menu_interface = menu_interface(screen, player, clock)
menu_interface.menu()

PAUSED = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                PAUSED = not PAUSED
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if player.bullets_num > 0:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                    bullet = PlayerBullet(screen, player.x, player.y, mouse_x, mouse_y)
                    player.player_bullets.append(bullet)
                    player.bullets_num -= 1
                else:
                    pass
    if not PAUSED:
        if player.alive:
            menu_interface.menu()
            screen.fill(GREEN)
            player.movement()
            player.draw_player(screen)
            borders_lst = draw_borders(screen, 0, 0, WIDTH, HEIGHT, WIDTH / 60, ORANGE)
            menu_interface.fps(clock)
            menu_interface.show_bullets_num(player.bullets_num)

            for i in borders_lst:
                if player.body.colliderect(i):
                    player.alive = False
                for deer in deers:
                    if deer.vision_area.colliderect(i):
                        deer.new_x, deer.new_y = deer.random_x(), deer.random_y()
                    if deer.body.colliderect(i):
                        deer.alive = False
                for wolf in wolfs:
                    if wolf.vision_area.colliderect(i):
                        wolf.new_x, wolf.new_y = wolf.random_x(), wolf.random_y()
                    if wolf.body.colliderect(i) or wolf.hunger_rate == HUNGER_RATE:
                        wolf.alive = False
                for rabbit in rabbits:
                    if rabbit.vision_area.colliderect(i):
                        rabbit.new_x, rabbit.new_y = rabbit.random_x(), rabbit.random_y()
                    if rabbit.body.colliderect(i):
                        rabbit.alive = False

            for rabbit in rabbits:
                if rabbit.alive:
                    rabbit.draw(screen)
                    rabbit.move()

                    if rabbit.panic_mode == False:
                        if player.body.colliderect(rabbit.vision_area):
                            rabbit.new_x, rabbit.new_y = rabbit.random_x(), rabbit.random_y()
                            # deer.speed+=0.3
                            rabbit.panic_mode = True
            for deer in deers:
                if deer.alive:
                    deer.draw(screen)
                    deer.move()

                    if deer.group_status == False:
                        for deer2 in deers:
                            if deer.body.colliderect(deer2.vision_area):
                                deer.group_status = True
                                deer.new_x, deer.new_y = deer.aliquot_spd(deer2.vision_area_x), deer.aliquot_spd(
                                    deer2.vision_area_y)
                    if deer.panic_mode == False:
                        if player.body.colliderect(deer.vision_area):
                            deer.new_x, deer.new_y = deer.random_x(), deer.random_y()
                            # deer.speed+=0.3
                            deer.panic_mode = True
                else:
                    deers.remove(deer)

            for wolf in wolfs:
                if wolf.alive:
                    wolf.draw(screen)
                    wolf.move()

                    if player.body.colliderect(wolf.body):
                        player.alive = False
                    if player.body.colliderect(wolf.vision_area):
                        wolf.new_x, wolf.new_y = wolf.aliquot_spd(player.pos[0]), wolf.aliquot_spd(player.pos[1])
                    for deer in deers:
                        if deer.body.colliderect(wolf.vision_area):
                            wolf.new_x, wolf.new_y = wolf.aliquot_spd(deer.x), wolf.aliquot_spd(deer.y)
                            deer.new_y, deer.new_y = deer.random_x(), deer.random_y()
                            deer.panic_mode = True
                        if wolf.body.colliderect(deer.body):
                            wolf.hunger_rate -= 2
                            deer.alive = False
                    for rabbit in rabbits:
                        if rabbit.body.colliderect(wolf.vision_area):
                            wolf.new_x, wolf.new_y = wolf.aliquot_spd(rabbit.x), wolf.aliquot_spd(rabbit.y)
                            rabbit.new_y, rabbit.new_y = rabbit.random_x(), rabbit.random_y()
                            rabbit.panic_mode = True
                        if wolf.body.colliderect(deer.body):
                            wolf.hunger_rate -= 2
                            rabbit.alive = False

                else:
                    wolfs.remove(wolf)

            bullet_list_copy = player.player_bullets.copy()
            for blt in bullet_list_copy:

                if (time.time() - blt.time1) < blt.exist_time:
                    for wolf in wolfs:
                        if blt.fig.colliderect(wolf.body):
                            wolfs.remove(wolf)
                            break
                    for deer in deers:
                        if blt.fig.colliderect(deer.body):
                            deers.remove(deer)
                            break
                    for rabbit in rabbits:
                        if blt.fig.colliderect(rabbit.body):
                            rabbits.remove(rabbit)
                            break
                    blt.shoot(screen)
                    blt.bullet_frame()
                else:
                    player.player_bullets.remove(blt)
                break

            pygame.display.flip()
            clock.tick(FPS)
        else:
            button_font = pygame.font.Font('resources\\font\\font.otf', 72)
            start = button_font.render('TRY AGAIN', 1, pygame.Color('lightgray'))
            button_start = pygame.Rect(0, 0, 400, 150)
            button_start.center = HALF_WIDTH, HALF_HEIGHT
            exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
            button_exit = pygame.Rect(0, 0, 400, 150)
            button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

            pygame.draw.rect(screen, BLACK, button_start, border_radius=25, width=10)
            screen.blit(start, (button_start.centerx - 190, button_start.centery - 70))

            pygame.draw.rect(screen, BLACK, button_exit, border_radius=25, width=10)
            screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(screen, BLACK, button_start, border_radius=25)
                screen.blit(start, (button_start.centerx - 190, button_start.centery - 70))
                if mouse_click[0]:
                    player.x = WIDTH / 2
                    player.y = HEIGHT / 2
                    wolfs = [Wolf() for w in range(WOLF_NUMBER)]
                    deers = [Deer() for d in range(DEER_NUMBER)]
                    rabbits = [Rabbit() for d in range(RABBIT_NUMBER)]
                    player.alive = True
                    player.bullets_num = BULLETS_NUM
                    pass

            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(screen, BLACK, button_exit, border_radius=25)
                screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    break

            pygame.display.flip()
            clock.tick(FPS)
    else:
        button_font = pygame.font.Font('resources\\font\\font.otf',
                                       72)
        start = button_font.render('RESUME', 1, pygame.Color('lightgray'))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = HALF_WIDTH, HALF_HEIGHT
        exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = HALF_WIDTH, HALF_HEIGHT + 200

        pygame.draw.rect(screen, BLACK, button_start, border_radius=25, width=10)
        screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))

        pygame.draw.rect(screen, BLACK, button_exit, border_radius=25, width=10)
        screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if button_start.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BLACK, button_start, border_radius=25)
            screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))
            if mouse_click[0]:
                PAUSED = not PAUSED

        elif button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BLACK, button_exit, border_radius=25)
            screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
            if mouse_click[0]:
                pygame.quit()
                break

        pygame.display.flip()
        clock.tick(FPS)
