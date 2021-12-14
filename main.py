import random
import time
import pygame
from pygame.locals import *

SIZE = 600, 600
pygame.init()
screen = pygame.display.set_mode(SIZE)

RED = (255, 0, 0)
GRAY = (150, 150, 150)
GAME_OVER = pygame.transform.scale(pygame.image.load('assets/game_over.jpg').convert_alpha(), SIZE)

pos = []
for x in range(0, 600, 20):
    for y in range(0, 600, 20):
        pos.append((y, x))


class Reward:
    def __init__(self):
        self.current_pos = random.randint(0, 900)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), Rect(pos[self.current_pos][0], pos[self.current_pos][1], 20, 20))


class Player:
    def __init__(self):
        self.current_pos = 430
        self.last_event = K_RIGHT
        self.length = 2
        self.pos_list = [self.current_pos]

    def draw(self):
        for index, position in enumerate(self.pos_list):
            pygame.draw.rect(screen, (255, 255, 255), Rect(pos[position][0], pos[position][1], 20, 20))

    def manage_tail(self):
        if self.length == len(self.pos_list):
            self.pos_list.append(self.current_pos)
            del self.pos_list[0]
        else:
            self.pos_list.append(self.current_pos)
        if len(self.pos_list) != len(set(self.pos_list)):
            print("Game Over")
            time.sleep(1)
            screen.blit(GAME_OVER, (0, 0))
            pygame.display.flip()
            time.sleep(2)
            exit()

    def move_player(self):
        if (self.current_pos - 29) % 30 == 0 and self.last_event == K_RIGHT:
            self.current_pos -= 30
        elif self.current_pos % 30 == 0 and self.last_event == K_LEFT:
            self.current_pos += 30
        events = self.last_event
        if events == K_UP:
            self.current_pos -= 30
        elif events == K_DOWN:
            self.current_pos += 30
        elif events == K_RIGHT:
            self.current_pos += 1
        elif events == K_LEFT:
            self.current_pos -= 1
        if self.current_pos > 900:
            self.current_pos = (900 - self.current_pos) * -1
        elif self.current_pos < 0:
            self.current_pos = (900 + self.current_pos)
        self.last_event = events
        self.manage_tail()


def draw():
    global player, reward
    screen.fill((0, 0, 0))
    player.move_player()
    if reward.current_pos == player.current_pos:
        reward = Reward()
        player.length += 1

    reward.draw()
    player.draw()


player = Player()
reward = Reward()
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(10)
    draw()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if player.last_event in [K_RIGHT, K_LEFT] and event.key in [K_DOWN, K_UP]:
                player.last_event = event.key
            elif player.last_event in [K_DOWN, K_UP] and event.key in [K_RIGHT, K_LEFT]:
                player.last_event = event.key

    pygame.display.flip()

pygame.quit()
