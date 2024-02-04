# IDEAS
# sandbox mode
# multiplayer?
# more fighter abilities
# have configuration move in y direction?
# enemy migration?

# TODO
# update regex with correct letter range

import re
import math
import random
import os.path

import numpy as np
import pygame

DIVE_DY = 15
DIVE_DX = 60
DIVE_YM = 475
DIVE_TIME = 100
DIVE_ROTS = 3
MAX_TARGET_OFFSET = 45

with open('x_pattern.txt', 'r') as f:
    x_pattern = f.read().split('\n')

with open('y_pattern.txt', 'r') as f:
    y_pattern = f.read().split('\n')

t_range = np.arange(0, 1, 5 / DIVE_TIME)
factor_p0 = (1 - t_range)**3
factor_p1 = 3 * (1 - t_range)**2 * t_range
factor_p2 = 3 * (1 - t_range) * t_range**2
factor_p3 = t_range**3

def dx(t):
    return 15 * math.sin(t / 6) # x offset for flying animation

def up(y):
    return y - DIVE_DY
    
def down(y):
    return y + DIVE_DY

def cubic_bezier(c0, c1, c2, c3):
    return factor_p0 * c0 + factor_p1 * c1 + factor_p2 * c2 + factor_p3 * c3

parse_normal = re.compile('(\d+) (\d+)')
parse_range = re.compile('(\d+)-(\d+) (\d+)')

def parse_level(level):
    enemies = []
    for line in level.split('\n'):
        if parse_normal.match(line):
            x, y = parse_normal.match(line).groups()
            enemies.append(Enemy(int(x), int(y)))
        elif parse_range.match(line):
            x1, x2, y = parse_range.match(line).groups()
            for x in range(int(x1), int(x2) + 1):
                enemies.append(Enemy(x, int(y)))
    return enemies

class Dive:
    def __init__(self, x0, y0, game_time):
        self.speed = 1.5 if random.randint(1, 10) == 1 else 1
        self.origin_x = x0
        self.origin_y = y0
        self.end_x = self.origin_x - dx(game_time) + dx((game_time + DIVE_TIME) / self.speed)
        self.t = 0
        target_offset = random.randint(-MAX_TARGET_OFFSET, MAX_TARGET_OFFSET)

        x_conv = {
            '-': self.origin_x - DIVE_DX + target_offset,
            '+': self.origin_x + DIVE_DX + target_offset,
            '0': self.origin_x
        }
        
        y_conv = {
            '0': self.origin_y,
            '1': (self.origin_y + DIVE_YM) // 2,
            '2': DIVE_YM,
            '-': up,
            '+': down,
        }

        bezier_x = []
        for i, line in enumerate(x_pattern):
            x_coords = [x_conv[c] for c in line]
            if i == 4:
                x_coords[2] = x_coords[3] = self.end_x
            bezier_x.append(cubic_bezier(*x_coords))
        self.x = np.concatenate(bezier_x)

        bezier_y = []
        for line in y_pattern:
            y0 = y_conv[line[0]]
            o0 = y_conv[line[1]]
            y1 = y_conv[line[2]]
            o1 = y_conv[line[3]]
            y_coords = [y0, o0(y0), o1(y1), y1]
            bezier_y.append(cubic_bezier(*y_coords))
        self.y = np.concatenate(bezier_y)

    def get_pos(self):
        # Returns x, y, completed?
        self.t += self.speed
        if self.t >= self.x.size:
            return (self.end_x, self.origin_y, True)
        return (self.x[int(self.t)], self.y[int(self.t)], False)

class Enemy:
    def __init__(self, x, y):
        self.base_x = 20 + 30 * (x - 1) # configuration x (pixels)
        self.base_y = 20 + 30 * (y - 1) # configuration y (pixels)
        self.x = self.base_x # position x (pixels)
        self.y = self.base_y # position y (pixels)
        self.rot = 270 # rotation in degrees in normal position
        
        self.diving = False
        self.dive = None

    def move(self, dx):
        if self.diving:
            self.rot -= DIVE_ROTS * 360 / DIVE_TIME
            self.x, self.y, complete = self.dive.get_pos()
            self.diving = not complete
        else:
            self.rot = 270
            target_x = self.base_x + dx
            self.x = target_x

    def perform_dive(self, game_time):
        self.diving = True
        self.dive = Dive(self.x, self.y, game_time)

class Player(pygame.sprite.Sprite):
    def __init__(self, image_sprite):
        self.x = 0 # may need to be updated
        self.y = 0 # may need to be updated
        self.image = image_sprite #the image for player
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*(2)), int(self.size[1]*(2))))
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-71, -11)

    def move(self, is_right):
        if is_right and self.rect.x < 390:
            self.x = 5
        elif (not is_right) and self.rect.x > 0:
            self.x = -5

    def update(self, screen):
        pygame.draw.rect(screen, [0, 0, 0], self.rect)
        self.rect.x += self.x
        self.x = 0
        screen.blit(self.image, (self.rect.x - 35, self.rect.y - 10))

class Game:
    def __init__(self, start=1):
        self.level = start
        with open(f'levels/L{start}.txt') as f:
            self.enemies = parse_level(f.read())
        self.game_time = 0

    def display_enemies(self, screen):
        for enemy in self.enemies:
            enemy_rect = pygame.Rect((enemy.x, enemy.y, 25, 25))  # Adjust size as needed
            self.draw_rotated_rectangle(screen, (0, 255, 0), enemy_rect, enemy.rot)
            # pygame.draw.rect(screen, (0, 255, 0), enemy_rect)
    
    def draw_rotated_rectangle(self, surface, color, rect, angle):
        rotated_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(rotated_surface, color, (0, 0, *rect.size))
        rotated_surface = pygame.transform.rotate(rotated_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=rect.center)
        surface.blit(rotated_surface, rotated_rect.topleft)

    def tick(self):
        for enemy in self.enemies:
            enemy.move(dx(self.game_time))
            if not enemy.diving and random.randint(1, len(self.enemies) * 50) == 1:
                enemy.perform_dive(self.game_time)
        if not self.enemies:
            # level completion animation?
            self.level += 1
            level_file = f'levels/L{self.level}.txt'
            if os.path.isfile(level_file):
                with open(level_file, 'r') as f:
                    self.enemies = parse_level(f.read())
            else:
                return False
        self.game_time += 1
        return True

def collides(rect1, rect2):
    return rect1.colliderect(rect2)