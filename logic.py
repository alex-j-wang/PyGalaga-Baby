# IDEAS
# sandbox mode
# multiplayer?
# more fighter abilities

# TODO
# update regex with correct letter range

import re
import json
import math

import numpy as np
import matplotlib.pyplot as plt
import pygame

DIVE_DY = 30
DIVE_DX = 45
DIVE_YM = 500

with open('x_pattern.txt', 'r') as f:
    x_pattern = f.read().split('\n')

with open('y_pattern.txt', 'r') as f:
    y_pattern = f.read().split('\n')

with open('enemy.json', 'r') as f:
    enemy_stats = json.load(f)

t = np.arange(0, 1, 0.05)
factor_p0 = (1 - t)**3
factor_p1 = 3 * (1 - t)**2 * t
factor_p2 = 3 * (1 - t) * t**2
factor_p3 = t**3

def up(y):
    return y - DIVE_DY
    
def down(y):
    return y + DIVE_DY

def cubic_bezier(c0, c1, c2, c3):
    return factor_p0 * c0 + factor_p1 * c1 + factor_p2 * c2 + factor_p3 * c3

parse_normal = re.compile('([A-Z]) (\d+) (\d+)')
parse_range = re.compile('([A-Z]) (\d+)-(\d+) (\d+)')

def parse_level(level):
    enemies = []
    for line in level.split('\n'):
        if parse_normal.match(line):
            name, x, y = parse_normal.match(line).groups()
            enemies.append(Enemy(name, int(x), int(y)))
        elif parse_range.match(line):
            name, x1, x2, y = parse_range.match(line).groups()
            for x in range(int(x1), int(x2) + 1):
                enemies.append(Enemy(name, x, int(y)))
    return enemies

class Dive:
    def __init__(self, x0, y0):
        self.origin_x = x0 # necessary?
        self.origin_y = y0 # necessary?
        self.t = 0

        x_conv = {
            '-': self.origin_x - DIVE_DX,
            '+': self.origin_x + DIVE_DX,
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
        all_x = []
        for line in x_pattern:
            x_coords = [x_conv[c] for c in line]
            all_x.extend(x_coords)
            bezier_x.append(cubic_bezier(*x_coords))
        self.x = np.concatenate(bezier_x)

        bezier_y = []
        all_y = []
        for line in y_pattern:
            y0 = y_conv[line[0]]
            o0 = y_conv[line[1]]
            y1 = y_conv[line[2]]
            o1 = y_conv[line[3]]
            y_coords = [y0, o0(y0), o1(y1), y1]
            all_y.extend(y_coords)
            bezier_y.append(cubic_bezier(*y_coords))
        self.y = np.concatenate(bezier_y)
        print(list(zip(all_x, all_y)))

    def get_pos(self):
        # Returns x, y, completed?
        self.t += 1
        if t == self.x.size():
            return (self.origin_x, self.origin_y, False)
        return (self.x[t], self.y[t], True)

class Enemy:
    def __init__(self, name, x, y):
        self.name = name
        self.base_x = 20 + 30 * (x - 1) # configuration x (pixels)
        self.base_y = 20 + 30 * (y - 1) # configuration y (pixels)
        self.x = self.base_x # position x (pixels)
        self.y = self.base_y # position y (pixels)
        self.rot = 270 # rotation in degrees in normal position
        
        self.health = enemy_stats[name]['health']
        self.abilities = enemy_stats[name]['abilities']
        
        self.diving = False
        self.dive = Dive()

    def move(self, dx):
        if self.diving:
            self.x, self.y, complete = self.dive.get_pos()
            self.diving = not complete
        else:
            self.x = self.base_x + dx

class Player:
    def __init__(self):
        self.health = 3
        self.x = 50 # may need to be updated
        self.y = 10 # may need to be updated

class Game:
    def __init__(self, start=1):
        self.level = start
        with open(f'levels/L{start}.txt') as f:
            self.enemies = parse_level(f.read())
        self.player = Player()
        self.time = 0

    def display_enemies(self, screen):
        for enemy in self.enemies:
            enemy_rect = pygame.Rect((enemy.x, enemy.y, 25, 25))  # Adjust size as needed
            pygame.draw.rect(screen, (0, 255, 0), enemy_rect)

    def tick(self):
        self.enemy_dx = 15 * math.sin(self.time / 6) # x offset for flying animation
        for enemy in self.enemies:
            enemy.move(self.enemy_dx)
        self.time += 1

def collides(rect1, rect2):
    return rect1.colliderect(rect2)

d = Dive(200, 300)
plt.scatter(d.x, d.y)
plt.show()