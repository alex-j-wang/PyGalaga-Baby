# IDEAS
# sandbox mode
# multiplayer?
# more fighter abilities

# TODO
# update regex with correct letter range

import re
import json
import math

import pygame

parse_normal = re.compile('([A-Z]) (\d+) (\d+)')
parse_range = re.compile('([A-Z]) (\d+)-(\d+) (\d+)')

with open('enemy.json', 'r') as f:
    enemy_stats = json.load(f)

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

class Enemy:
    def __init__(self, name, x, y):
        self.name = name
        self.config_x = x # configuration x in grid units
        self.config_y = y # configuration y in grid units
        self.x = 20 - 15 + 30 * self.config_x # x pixel position
        self.y = 20 - 15 + 30 * self.config_y # y pixel position
        self.rot = 270 # rotation in degrees in normal position
        self.health = enemy_stats[name]['health']
        self.abilities = enemy_stats[name]['abilities']
        self.diving = False


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
            if enemy.diving:
                # YIKES
                pass
            else:
                enemy.x = 20 - 15 + enemy.config_x * 30 + self.enemy_dx
                enemy.y = 20 - 15 + enemy.config_y * 30
        self.time += 1


