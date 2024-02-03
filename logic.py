# IDEAS
# sandbox mode
# multiplayer?
# more fighter abilities

# TODO
# update regex with correct letter range

import re
import json
import math

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
        self.x = x # x in grid units
        self.y = y # y in grid units
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

    def tick(self):
        self.enemy_dx = math.sin(self.time / 6) # x offset for flying animation
        self.time += 1

    def display(self):
        # ALEX SEND HELP
        # Enemy coordinates should probably be (N * (enemy x) + self.enemy_dx, N * (enemy y))
        pass

def main():
    game = Game()
    print(game.level)
    print(game.enemies)
    print(game.player)

if __name__ == "__main__":
    main()