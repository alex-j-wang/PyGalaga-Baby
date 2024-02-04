# FUTURE IDEAS
# sandbox mode (infinite lives)
# multiplayer
# more fighter abilities
# have configuration move in y direction
# enemy migration

import re
import math
import random
import os.path

import pygame
from bezier import generate_bezier_x, generate_bezier_y, DIVE_TIME

BUFFER = 20 # Buffer size
PIXELS = 30 # Tile width & height

AMPLITUDE = 15 # Amplitude of x offset for flying animation
PERIOD = 6 # Period multiplier for x offset

DIVE_DY = 15 # Bezier control point y offset
DIVE_DX = 60 # Bezier control point x offset
DIVE_YM = 500 # Bezier lowest control point y
DIVE_ROTS = 3 # Rotations during standard dive
MAX_TARGET_OFFSET = 60 # Maximum x offset for dive target
BOOST_SPEED = 1.5 # Speed multiplier for boost dives
BOOST_CHANCE = 8 # 1 in n chance of boost dive

def dx(t):
    """Returns the x offset for the flying animation at time t."""
    return AMPLITUDE * math.sin(t / PERIOD) # x offset for flying animation

up = lambda y: y - DIVE_DY
down = lambda y: y + DIVE_DY

parse_normal = re.compile('(\d+) (\d+)')
parse_range = re.compile('(\d+)-(\d+) (\d+)')

def parse_level(level):
    """Parses a level string and returns a list of Enemy objects."""
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
    """Stores dive data for an Enemy."""
    def __init__(self, x0, y0, game_time):
        """Initializes the dive."""
        self.speed = BOOST_SPEED if random.randint(1, BOOST_CHANCE) == 1 else 1
        self.origin_x = x0
        self.origin_y = y0
        self.end_x = self.origin_x - dx(game_time) + dx((game_time + DIVE_TIME) / self.speed)
        self.t = 0
        target_offset = random.randint(-MAX_TARGET_OFFSET, MAX_TARGET_OFFSET)

        # Generate x and y tables
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
        self.x = generate_bezier_x(x_conv, self.end_x)
        self.y = generate_bezier_y(y_conv)

    def get_pos(self):
        """Returns the current position of the dive and
        whether the dive is complete."""
        self.t += self.speed
        if self.t >= self.x.size:
            return (self.end_x, self.origin_y, True)
        return (self.x[int(self.t)], self.y[int(self.t)], False)

class Enemy:
    """Stores data for an enemy."""
    def __init__(self, x, y):
        """Initializes the enemy."""
        self.base_x = BUFFER + PIXELS * (x - 1) # Base x
        self.base_y = BUFFER + PIXELS * (y - 1) # Base y
        self.x = self.base_x # Current x
        self.y = self.base_y # Current y
        self.rot = 270 # Rotation in degrees in normal position
        
        self.diving = False # Whether the enemy is diving
        self.dive = None # Dive object

    def move(self, dx):
        """Moves the enemy based on the dx oscillation offset.
        If the enemy is diving, the dive is performed instead."""
        if self.diving:
            self.rot -= DIVE_ROTS * 360 / DIVE_TIME
            self.x, self.y, complete = self.dive.get_pos()
            self.diving = not complete
        else:
            self.rot = 270
            target_x = self.base_x + dx
            self.x = target_x

    def perform_dive(self, game_time):
        """Initiates a dive."""
        self.diving = True
        self.dive = Dive(self.x, self.y, game_time)

class Player():
    """Stores data for the player."""
    def __init__(self, screen):
        """Initializes the player."""
        self.dx = 0 # may need to be updated
        self.dy = 0 # may need to be updated
        self.coords = [[180, 540], [220, 540], [200, 500]] # Triangle
        self.center = self.coords[2]
        self.rect = pygame.draw.polygon(screen, [255, 0, 0], self.coords)
        self.lives = 3

    def move(self, is_right):
        """Moves the player left or right."""
        if is_right and self.coords[1][0] < 400:
            self.dx = 5
        elif (not is_right) and self.coords[0][0] > 0:
            self.dx = -5

    def update(self, screen):
        """Updates the player's position and draws it on the screen."""
        for coord in self.coords:
            coord[0] += self.dx
        self.dx = 0
        self.rect = pygame.draw.polygon(screen, [255, 0, 0], self.coords)

class Game:
    """Stores data for the game."""
    def __init__(self, start=0):
        """Initializes the game."""
        self.level = start
        self.enemies = []
        self.game_time = 0
        self.next_level_time = 80

    def display_enemies(self, screen):
        """Displays the enemies with rotation on the screen."""
        for enemy in self.enemies:
            enemy_rect = pygame.Rect((enemy.x, enemy.y, 25, 25))
            self.draw_rotated_rectangle(screen, (0, 255, 0), enemy_rect, enemy.rot)
    
    def draw_rotated_rectangle(self, surface, color, rect, angle):
        """Draws a rotated rectangle on the given surface."""
        rotated_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(rotated_surface, color, (0, 0, *rect.size), border_radius=5)
        rotated_surface = pygame.transform.rotate(rotated_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=rect.center)
        surface.blit(rotated_surface, rotated_rect.topleft)

    def tick(self, player):
        """Updates the game state by moving enemies, initiating dives,
        initializing levels, and tracking game time."""
        for enemy in self.enemies:
            enemy.move(dx(self.game_time))
            dive_chance = 100 * int(len(self.enemies)**0.5) # 1 in n chance of dive
            if not enemy.diving and random.randint(1, dive_chance) == 1:
                enemy.perform_dive(self.game_time)
        # If all enemies are defeated, set up the next level
        if not self.enemies:
            if self.next_level_time == 0:
                self.next_level_time = self.game_time + 80
            elif self.game_time >= self.next_level_time:
                self.level += 1
                level_file = f'levels/L{self.level}.txt'
                if os.path.isfile(level_file):
                    with open(level_file, 'r') as f:
                        self.enemies = parse_level(f.read())
                    if self.level > 1:
                        player.lives += 1
                    for enemy in self.enemies:
                        enemy.move(dx(self.game_time))
                else:
                    return False
        self.game_time += 1
        return True

def collides(rect1, rect2):
    """Returns whether two given pygame rectangles collide."""
    return rect1.colliderect(rect2)